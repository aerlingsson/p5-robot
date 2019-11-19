package com.example.p5_robot.Communication.Background;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;

import androidx.appcompat.app.AppCompatActivity;

import com.example.p5_robot.Communication.Background.CommunicationsTask;
import com.example.p5_robot.MainActivity;
import com.example.p5_robot.R;


public abstract class CommunicationsActivity extends AppCompatActivity {

    private static final String TAG = "CommunicationsActivity";

    protected CommunicationsTask btConnection;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.camera_activity);

        // Retrieve the address of the bluetooth device from the MainActivity
        Intent newIntent = getIntent();
        String mDeviceAddress = newIntent.getStringExtra(MainActivity.EXTRA_ADDRESS);

        // Create a connection to this device
        btConnection = new CommunicationsTask(this, mDeviceAddress);
        Log.d(TAG, "Comm task with address " + mDeviceAddress);
        btConnection.execute();
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        btConnection.disconnect();
    }
}
