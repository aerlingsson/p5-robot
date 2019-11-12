package com.example.p5_robot.Communication.UserInteface;

import android.content.Intent;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;

import com.example.p5_robot.Communication.Background.CommunicationsTask;
import com.example.p5_robot.R;


public abstract class CommunicationsActivity extends AppCompatActivity {

    protected CommunicationsTask btConnection;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_communications);

        // Retrieve the address of the bluetooth device from the BluetoothListDeviceActivity
        Intent newIntent = getIntent();
        String mDeviceAddress = newIntent.getStringExtra(DeviceListActivity.EXTRA_ADDRESS);

        // Create a connection to this device
        btConnection = new CommunicationsTask(this, mDeviceAddress);
        btConnection.execute();
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        btConnection.disconnect();
    }
}
