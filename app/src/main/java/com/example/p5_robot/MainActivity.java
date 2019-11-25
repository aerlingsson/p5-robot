package com.example.p5_robot;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.p5_robot.Agent.CameraPageActivity;
import com.example.p5_robot.Communication.Background.ConnectionActivity;

public class MainActivity extends AppCompatActivity {
    public static final String TAG = "MainActivity";
    public static String EXTRA_ADDRESS = "device_address";
    private BluetoothAdapter mBluetoothAdapter = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.camera_activity);

        this.mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        if (mBluetoothAdapter == null) {
            Toast.makeText(getApplicationContext(), "Bluetooth device not available", Toast.LENGTH_LONG).show();
            Log.d(TAG, "Bluetooth device not available");
            finish();

        } else {
            checkBluetoothAndConnect();

            // Start CameraPageActivity on new thread
            new Handler().post(new Runnable() {
                @Override
                public void run() {
                    Log.d(TAG, "Launcing camera activity");
                    Intent camInt = new Intent(MainActivity.this, CameraPageActivity.class);
                    startActivity(camInt);

                }
            });
        }
    }

    private void checkBluetoothAndConnect(){

        if (!mBluetoothAdapter.isEnabled()){
            // Run it on another thread, otherwise the action gets overwritten
            new Handler().post(new Runnable() {
                @Override
                public void run() {
                    Intent turnBTon = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                    //Ask the user to turn bluetooth on
                    startActivityForResult(turnBTon, 1);
                }
            });
        }

        connectToBtDevice();

    }

    private void connectToBtDevice(){
        String deviceName = "ev3dev";
        boolean isEv3Paired = false;
        for (BluetoothDevice device : mBluetoothAdapter.getBondedDevices()){
            if (device.getName().equals(deviceName)){
                isEv3Paired = true;
                Log.d(TAG, "Found " + device.getName());
                String btDeviceAddress = device.getAddress();         //MAC Address
                Log.d(TAG, "Got MAC " + btDeviceAddress);
                Log.d(TAG, "Starting conn activity");
                Intent ConnInt = new Intent(MainActivity.this, ConnectionActivity.class); // Make an intent to connect next activity.
                ConnInt.putExtra(EXTRA_ADDRESS, btDeviceAddress);     //this will be received at CommunicationsActivity
                startActivity(ConnInt);                               //Change the activity.
                Log.d(TAG, "Done with conn activity");
            }
        }

        if (!isEv3Paired) {
            Toast.makeText(this, deviceName + " was not found. Make sure the device is paired", Toast.LENGTH_SHORT).show();
        }
    }

}
