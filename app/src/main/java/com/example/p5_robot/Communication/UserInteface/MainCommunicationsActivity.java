package com.example.p5_robot.Communication.UserInteface;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.example.p5_robot.Agent.CameraPageActivity;
import com.example.p5_robot.R;

import java.io.IOException;
import java.io.InputStream;


public class MainCommunicationsActivity extends CommunicationsActivity {

    private static final String TAG = "MainCommActivity";
    private InputStream in;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_communications);

        try {
            this.in = btConnection.socket.getInputStream();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Starts the camera activity
        CameraPageActivity cameraPageActivity = new CameraPageActivity();
        Intent i = new Intent(MainCommunicationsActivity.this, CameraPageActivity.class); // Make an intent to start next activity.
        Log.d(TAG, "Starting camera activity");
        startActivity(i);                       //Change the activity.


        Button button = findViewById(R.id.send_button);
        final EditText userText = findViewById(R.id.send_to_server_text);

        final TextView serverMsg = findViewById(R.id.server_messages);
        String srv = "Messages from the server will appear here:\n";
        serverMsg.setText(srv);

        button.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View view) {
                for (byte b : userText.getText().toString().getBytes()) {
                    btConnection.write(b);
                    userText.setText("");
                }
                btConnection.write((byte) '.');
                msgFromServer(serverMsg);
            }
        });
    }

    public void msgFromServer(TextView srvText) {
        StringBuilder msgBuilder = new StringBuilder();
        char c;

        // Receives messages from server and displays in textView
        try {
            while(btConnection.socket.isConnected()){
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