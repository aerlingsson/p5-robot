package com.example.p5_robot.Communication.UserInteface;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.example.p5_robot.R;

import java.io.IOException;
import java.io.InputStream;


public class MainCommunicationsActivity extends CommunicationsActivity {

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

        Button button = findViewById(R.id.button);
        final EditText userText = findViewById(R.id.editText);

        final TextView serverMsg = findViewById(R.id.textView);
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