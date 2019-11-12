package com.example.p5_robot.Communication.UserInteface;

import android.os.Bundle;
import android.widget.TextView;

import com.example.p5_robot.R;

import java.io.IOException;
import java.io.InputStream;


public class AutomaticCommunicationsActivity extends CommunicationsActivity{

    private InputStream in;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_autocomm);

        try {
            this.in = btConnection.socket.getInputStream();
        } catch (IOException e) {
            e.printStackTrace();
        }

        final TextView headline = findViewById(R.id.headline);
        String hl = "Messages from the server will appear here:\n";
        headline.setText(hl);

        final TextView serverMsg = findViewById(R.id.server_msg);
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

}

