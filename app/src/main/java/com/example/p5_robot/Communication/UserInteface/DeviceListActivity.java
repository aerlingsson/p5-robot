package com.example.p5_robot.Communication.UserInteface;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.p5_robot.R;

import java.util.ArrayList;
import java.util.Set;
import java.util.concurrent.TimeUnit;


public class DeviceListActivity extends AppCompatActivity {
    private static final String TAG = "DeviceListActivity";

    ListView mDeviceList;
    private BluetoothAdapter mBluetoothAdapter = null;
    public static String EXTRA_ADDRESS = "device_address";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_device_list);

        mDeviceList = findViewById(R.id.listView);

        mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        if(mBluetoothAdapter == null) {
            Toast.makeText(getApplicationContext(), "Bluetooth Device Not Available", Toast.LENGTH_LONG).show();
            finish();
        }
        else {
            checkBluetoothAndConnect();
        }
    }

    private void checkBluetoothAndConnect(){
        if (mBluetoothAdapter.isEnabled()){
            connectToEv3();
        } else {
            Intent turnBTon = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            //Ask the user to turn bluetooth on
            startActivityForResult(turnBTon, 1);
        }
    }

    private void connectToEv3(){
        String ev3Name = "ev3dev";
        boolean isEv3Paired = false;
        for (BluetoothDevice device : mBluetoothAdapter.getBondedDevices()){
            if (device.getName().equals(ev3Name)){
                isEv3Paired = true;
                Log.d(TAG, "Found " + device.getName());
                String address = device.getAddress();   //MAC Address
                Log.d(TAG, "Got MAC " + address);
                Intent i = new Intent(DeviceListActivity.this, MainCommunicationsActivity.class); // Make an intent to start next activity.
                Log.d(TAG, "Starting comm activity");
                i.putExtra(EXTRA_ADDRESS, address);     //this will be received at CommunicationsActivity
                startActivity(i);                       //Change the activity.
            }
        }
        
        if (!isEv3Paired) {
            Toast.makeText(this, ev3Name + " was not found. Make sure the device is paired", Toast.LENGTH_SHORT).show();

        }
        
    }

    private void listPairedDevices() {
        Set<BluetoothDevice> mPairedDevices = mBluetoothAdapter.getBondedDevices();
        ArrayList<String> list = new ArrayList<>();

        if (mPairedDevices.size() > 0)
        {
            for(BluetoothDevice bt : mPairedDevices)
            {
                list.add(bt.getName() + "\n" + bt.getAddress());
            }
        }
        else
        {
            Toast.makeText(getApplicationContext(), "No Paired Bluetooth Devices Found.", Toast.LENGTH_LONG).show();
        }

        final ArrayAdapter<String> adapter = new ArrayAdapter<>(this,android.R.layout.simple_list_item_1, list);
        mDeviceList.setAdapter(adapter);
        try {
            TimeUnit.MILLISECONDS.sleep(500);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        mDeviceList.setOnItemClickListener(myListClickListener);    //Method called when the device from the list is clicked
    }

    //Necessary, as AdapterView.OnItemClickListener is abstract
    private AdapterView.OnItemClickListener myListClickListener = new AdapterView.OnItemClickListener()
    {
        public void onItemClick (AdapterView av, View v, int arg2, long arg3)
        {
            // Get the device MAC address, the last 17 chars in the View
            String info = ((TextView) v).getText().toString();
            String address = info.substring(info.length() - 17);
            // Make an intent to start next activity.
            Intent i = new Intent(DeviceListActivity.this, MainCommunicationsActivity.class);
            //Change the activity.
            i.putExtra(EXTRA_ADDRESS, address);     //this will be received at CommunicationsActivity
            startActivity(i);
        }
    };

}
