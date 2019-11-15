package com.example.p5_robot.Agent;

import android.content.res.AssetFileDescriptor;
import android.content.res.AssetManager;
import android.graphics.Bitmap;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.util.ArrayList;
import java.util.List;

import org.tensorflow.lite.Interpreter;
import org.tensorflow.lite.gpu.GpuDelegate;

public class TensorflowModel {
    private static final int IMAGE_MEAN = 128;
    private static final int BATCH_SIZE = 1;
    private static final int CHANNELS = 3;
    private static final float NORMALIZATION_VALUE = 255.0f;

    private int inputSize;
    private Interpreter interpreter;
    private GpuDelegate delegate;
    private List<String> labels = new ArrayList<>();


    public TensorflowModel(AssetManager assetManager, String modelPath, String labelPath, int inputSize) {
        this.inputSize = inputSize;

        try {
            labels = loadLabelList(assetManager, labelPath);
            MappedByteBuffer modelFile = loadModelFile(assetManager, modelPath);
            this.delegate = new GpuDelegate();
            Interpreter.Options options = new Interpreter.Options();
            //options.addDelegate(this.delegate); TODO: get this to work, you probably need to optimize the model for this to work
            this.interpreter = new Interpreter(modelFile, options);
        } catch (IOException e) {
            System.out.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Failed to load model file!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
        }

    }


    private MappedByteBuffer loadModelFile(AssetManager assetManager, String modelPath) throws IOException {
        AssetFileDescriptor fileDescriptor = assetManager.openFd(modelPath);
        FileInputStream inputStream = new FileInputStream(fileDescriptor.getFileDescriptor());
        FileChannel fileChannel = inputStream.getChannel();
        long startOffset = fileDescriptor.getStartOffset();
        long declaredLength = fileDescriptor.getDeclaredLength();
        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declaredLength);
    }

    private List<String> loadLabelList(AssetManager assetManager, String labelPath) throws IOException {
        List<String> labelList = new ArrayList<>();
        BufferedReader reader = new BufferedReader(new InputStreamReader(assetManager.open(labelPath)));
        String line;
        while ((line = reader.readLine()) != null) {
            labelList.add(line);
        }
        reader.close();
        return labelList;
    }

    public String runInference(Bitmap bitmap) {
        System.out.println(bitmap);
        ByteBuffer buffer = convertBitmapToByteBuffer(bitmap);

        float[][] result = new float[1][labels.size()];
        this.interpreter.run(buffer, result);
        int index = decodeResult(result);

        return labels.get(index);
    }

    private int decodeResult(float[][] result) {
        float max = -1;
        int maxIndex = 0;
        for (int i = 0; i < result[0].length; i++){
            float confidence = result[0][i];
            if (confidence > max){
                max = confidence;
                maxIndex = i;
            }
        }

        return maxIndex;
    }


    private ByteBuffer convertBitmapToByteBuffer(Bitmap bitmap) {
        ByteBuffer byteBuffer;

        byteBuffer = ByteBuffer.allocateDirect(4 * BATCH_SIZE * inputSize * inputSize * CHANNELS);

        byteBuffer.order(ByteOrder.nativeOrder());
        int[] intValues = new int[inputSize * inputSize];
        bitmap.getPixels(intValues, 0, bitmap.getWidth(), 0, 0, bitmap.getWidth(), bitmap.getHeight());
        int pixel = 0;
        for (int i = 0; i < inputSize; ++i) {
            for (int j = 0; j < inputSize; ++j) {
                final int val = intValues[pixel++];
                byteBuffer.putFloat(( (val >> 16) & 0xFF) / NORMALIZATION_VALUE);
                byteBuffer.putFloat(( (val >> 8) & 0xFF) / NORMALIZATION_VALUE);
                byteBuffer.putFloat(( (val) & 0xFF) / NORMALIZATION_VALUE);
            }
        }
        return byteBuffer;
    }


    public void close() {
        this.delegate.close();
        this.interpreter.close();
    }

}
