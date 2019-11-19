package com.example.p5_robot.Communication.Background;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.example.p5_robot.Communication.UserInterface.CommunicationsActivity;
import com.example.p5_robot.R;

import java.io.IOException;
import java.io.InputStream;

public class CommunicationManager extends CommunicationsActivity {

    private static final String TAG = "CommunicationManager";
    private InputStream in;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.camera_activity);

        try {
            this.in = super.btConnection.socket.getInputStream();
            Log.d(TAG, "InputStream set");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void msgFromServer(TextView srvText) {
        StringBuilder msgBuilder = new StringBuilder();
        char c;

        // Receives messages from server and displays in textView
        try {
            while(super.btConnection.socket.isConnected()){
                String messageFromServer = msgBuilder.toString();
                c = (char) in.read();
                if (c == '.') {
                    if (messageFromServer.length() > 0) {
                        srvText.append("\n" + messageFromServer);
                        msgBuilder.setLength(0);
                        break;
                    }
                } else {
                    msgBuilder.append(c);
                }
            }
        } catch (IOException e){
            e.printStackTrace();
        }
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
    }
}
