package com.mapeiyu.befucked;

import android.content.Context;
import android.support.test.InstrumentationRegistry;
import android.support.test.runner.AndroidJUnit4;
import android.util.Log;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.ServerSocket;
import java.net.Socket;

@RunWith(AndroidJUnit4.class)
public class SocketServer {
    public static final String TAG = "SocketServer";
    public static int PORT = 9000;

    private ServerSocket serverSocket;
    private boolean loop = true;
    private Context context;

    @Before
    public void init() {
        context = InstrumentationRegistry.getTargetContext();
    }

    @Test
    public void acceptFromPC() throws IOException {
        serverSocket = new ServerSocket(PORT);
        while(loop) {
            Log.e(TAG, "socket server waiting ...");
            try {
                Socket server = serverSocket.accept();
//                Log.e(TAG, "connected: " + server.getRemoteSocketAddress());

                InputStream inputStream = server.getInputStream();
                byte[] bytes = new byte[1024];
                int len;
                StringBuilder builder = new StringBuilder();
                if ((len = inputStream.read(bytes)) != -1) {
                    builder.append(new String(bytes, 0, len));
                }
                String received = builder.toString();
                Log.e(TAG, "received: " + received);

                EventParser.parseEvent(context, received);


//                if ("stop".equals(received)) {
//                    loop = false;
//                }
//                DataOutputStream out = new DataOutputStream(server.getOutputStream());
//                String response = "response for: " + received;
//                out.write(response.getBytes());
//                out.flush();
                server.close();
            } catch(Exception e) {
                Log.e(TAG, "error: " + e.toString());
                e.printStackTrace();
            }
        }

        try {
            serverSocket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        Log.e(TAG, "socket server stopped");

    }
}
