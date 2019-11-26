package com.example.p5_robot.Agent;

import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.LoaderCallbackInterface;
import org.opencv.android.OpenCVLoader;
import org.opencv.android.Utils;
import org.opencv.core.Mat;
import org.opencv.core.Point;
import org.opencv.core.Size;
import org.opencv.imgproc.*;

import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.os.Handler;
import android.os.HandlerThread;
import android.util.Log;
import android.util.Rational;
import android.view.TextureView;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.camera.core.CameraX;
import androidx.camera.core.ImageAnalysis;
import androidx.camera.core.ImageAnalysisConfig;
import androidx.camera.core.ImageProxy;
import androidx.camera.core.Preview;
import androidx.camera.core.PreviewConfig;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.lifecycle.LifecycleOwner;

import com.example.p5_robot.Communication.Background.CommunicationsActivity;
import com.example.p5_robot.R;

import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

public class CameraPageActivity extends CommunicationsActivity {
    private static final String MODEL_PATH = "models/model_test.tflite";
    private static final String LABEL_PATH = "labels.txt";
    private static final int INPUT_SIZE = 80;
    private static final String TAG = "CameraPageActivity";

    private TensorflowModel model;
    private Executor executor = Executors.newSingleThreadExecutor();

    private int REQUEST_CODE_PERMISSIONS = 10; //arbitrary number, can be changed accordingly
    private final String[] REQUIRED_PERMISSIONS = new String[]{"android.permission.CAMERA", "android.permission.WRITE_EXTERNAL_STORAGE"}; //array w/ permissions from manifest
    private TextureView txView;
    private TextView text1;
    private TextView text2;
    private String labelText = "";
    private long start;

    private BaseLoaderCallback mLoaderCallback = new BaseLoaderCallback(this) {
        @Override
        public void onManagerConnected(int status) {
            switch (status) {
                case LoaderCallbackInterface.SUCCESS: {
                    Log.i(TAG, "OpenCV loaded successfully");
                }
                break;
                default: {
                    super.onManagerConnected(status);
                }
                break;
            }
        }
    };


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);

        setContentView(R.layout.camera_activity);
        Log.d(TAG, "Starting camera activity");

        txView = findViewById(R.id.view_finder);
        text1 = findViewById(R.id.textView1);
        text2 = findViewById(R.id.textView2);

        if (!allPermissionsGranted()) {
            ActivityCompat.requestPermissions(this, REQUIRED_PERMISSIONS, REQUEST_CODE_PERMISSIONS);
        }
        start = System.currentTimeMillis();
        startCamera();
        initTensorflowModel();
    }

    private void startCamera() {
        CameraX.unbindAll();

        Preview preview = buildPreview();
        ImageAnalysis analysis = buildAnalyzer();

        CameraX.bindToLifecycle((LifecycleOwner) this, analysis, preview);
    }



    private Preview buildPreview(){
        /* connect preview */
        int aspRatioW = txView.getWidth();  //get width of screen
        int aspRatioH = txView.getHeight();  //get height
        android.util.Size screen = new android.util.Size(aspRatioW, aspRatioH); //size of the screen

        PreviewConfig pConfig = new PreviewConfig.Builder().setTargetResolution(screen).build();
        Preview preview = new Preview(pConfig);

        preview.setOnPreviewOutputUpdateListener(
                new Preview.OnPreviewOutputUpdateListener() {
                    //to update the surface texture we have to destroy it first, then re-add it
                    @Override
                    public void onUpdated(Preview.PreviewOutput output) {
                        ViewGroup parent = (ViewGroup) txView.getParent();
                        parent.removeView(txView);
                        parent.addView(txView, 0);
                        txView.setSurfaceTexture(output.getSurfaceTexture());

                    }
                });
        return preview;
    }

    private ImageAnalysis buildAnalyzer(){
        HandlerThread analyzerThread = new HandlerThread("OpenCVAnalysis");
        analyzerThread.start();

        ImageAnalysisConfig imgAConfig = new ImageAnalysisConfig.Builder()
                .setImageReaderMode(ImageAnalysis.ImageReaderMode.ACQUIRE_LATEST_IMAGE)
                .setCallbackHandler(new Handler(analyzerThread.getLooper()))
                .setImageQueueDepth(1).build();
        ImageAnalysis analysis = new ImageAnalysis(imgAConfig);

        analysis.setAnalyzer(
                new ImageAnalysis.Analyzer() {
                    @Override
                    public void analyze(ImageProxy image, int rotationDegrees) {
                        Bitmap bitmap = txView.getBitmap();

                        Mat mat = new Mat();
                        Utils.bitmapToMat(bitmap, mat);

                        Imgproc.resize(mat, mat, new Size(INPUT_SIZE, INPUT_SIZE));
                        Mat rotationMatrix = Imgproc.getRotationMatrix2D(new Point(INPUT_SIZE/2, INPUT_SIZE/2), 90, 1);

                        //Rotating the given image
                        Imgproc.warpAffine(mat, mat, rotationMatrix, new Size(INPUT_SIZE, INPUT_SIZE));

                        Bitmap img = Bitmap.createBitmap(INPUT_SIZE, INPUT_SIZE, Bitmap.Config.ARGB_8888);

                        Utils.matToBitmap(mat, img);

                        labelText = model.runInference(img);


                        final String msg = labelText + "_10";

                        new Handler().post(new Runnable() {
                            @Override
                            public void run() {
                                try {
                                    btConnection.write(msg);
                                } catch (Exception e) {
                                    Log.d(TAG, "Tried to write while not connected to BT");
                                    e.printStackTrace();
                                }
                            }
                        });

                        text1.post(new Runnable() {
                            public void run() {
                                int fps = getFps();
                                String fpsString = "Fps: " + fps;
                                text1.setText(fpsString);
                            }
                        });
                        text2.post(new Runnable() {
                            public void run() {
                                text2.setText(labelText);
                            }
                        });

                    }
                });
        return analysis;
    }

    private int getFps(){
        long end = System.currentTimeMillis();
        float sec = (end - start) / 1000F;
        start = System.currentTimeMillis();
        return (int)(1/sec);
    }


    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        //connect camera when permissions have been granted otherwise exit app
        if (requestCode == REQUEST_CODE_PERMISSIONS) {
            if (allPermissionsGranted()) {
                Toast.makeText(this, "Permissions not granted by the user.", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(this, "Permissions not granted by the user.", Toast.LENGTH_SHORT).show();
                finish();
            }
        }
    }

    private boolean allPermissionsGranted() {
        //check if req permissions have been granted
        for (String permission : REQUIRED_PERMISSIONS) {
            if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                return false;
            }
        }
        return true;
    }

    @Override
    public void onResume() {
        super.onResume();
        if (!OpenCVLoader.initDebug()) {
            Log.d(TAG, "Internal OpenCV library not found. Using OpenCV Manager for initialization");
            OpenCVLoader.initAsync(OpenCVLoader.OPENCV_VERSION_3_0_0, this, mLoaderCallback);
        } else {
            Log.d(TAG, "OpenCV library found inside package. Using it!");
            mLoaderCallback.onManagerConnected(LoaderCallbackInterface.SUCCESS);
        }
    }


    private void initTensorflowModel() {
        executor.execute(new Runnable() {
            @Override
            public void run() {
                try {
                    model = new TensorflowModel(
                            getAssets(),
                            MODEL_PATH,
                            LABEL_PATH,
                            INPUT_SIZE);
                } catch (final Exception e) {
                    throw new RuntimeException("Error initializing TensorFlow!", e);
                }
            }
        });
    }


}