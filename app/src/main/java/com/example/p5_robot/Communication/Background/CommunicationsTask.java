package com.example.p5_robot.Communication.Background;

import android.app.ProgressDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.os.AsyncTask;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.io.IOException;
import java.util.UUID;


public class CommunicationsTask extends AsyncTask<Void, Void, Void> {

    private boolean connected = true;
    private ProgressDialog progressDialog;
    public BluetoothSocket socket = null;
    private AppCompatActivity currentActivity;
    private String address;

    private static final UUID myUUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");

    public CommunicationsTask(AppCompatActivity activity, String address) {
        this.currentActivity = activity;
        this.address =  address;
    }

    @Override
    protected void onPreExecute()     {
        progressDialog = ProgressDialog.show(this.currentActivity, "Connecting...", "Please wait!!!");  //show a progress dialog
    }

    @Override
    protected Void doInBackground(Void... devices) { //while the progress dialog is shown, the connection is done in background

        try {
            if (socket == null || !connected) {
                BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();   //get the mobile bluetooth device
                BluetoothDevice device = mBluetoothAdapter.getRemoteDevice(address);         //connects to the device's address and checks if it's available
                socket = device.createInsecureRfcommSocketToServiceRecord(myUUID);           //create a RFCOMM (SPP) connection
                BluetoothAdapter.getDefaultAdapter().cancelDiscovery();
                socket.connect(); //start connection
            }
        }
        catch (IOException e) {
            connected = false;      //if the try failed, you can check the exception here
        }
        return null;
    }

    @Override
    protected void onPostExecute(Void result) {     //after the doInBackground, it checks if everything went fine

        super.onPostExecute(result);

        if (!connected){
            message("Connection Failed. Is it a SPP Bluetooth running a server? Try again.");
            this.currentActivity.finish();

        }
        else {
            message("Connected.");
        }
        progressDialog.dismiss();
    }

    public void write(byte b) {

        try {
            socket.getOutputStream().write((int)b);
        }
        catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }

    public void disconnect() {
        if (socket !=null) //If the btSocket is busy
        {
            try  {
                socket.close(); //close connection
            }
            catch (IOException e) {
                message("Error");
            }
        }

        message("Disconnected");

        this.currentActivity.finish();
    }


    private void message(String s) {
        Toast.makeText(this.currentActivity.getApplicationContext(),s, Toast.LENGTH_SHORT).show();
    }

}
