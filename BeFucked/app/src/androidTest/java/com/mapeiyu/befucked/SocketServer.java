package com.mapeiyu.befucked;

import android.content.Context;
import android.support.test.InstrumentationRegistry;
import android.support.test.runner.AndroidJUnit4;
import android.util.Log;

import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.runner.RunWith;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketTimeoutException;

import static org.junit.Assert.*;

@RunWith(AndroidJUnit4.class)
public class SocketServer {
    public static final String TAG = "SocketServer";
    public static int PORT = 9000;

    private ServerSocket serverSocket;
    private boolean loop = true;

    @Before
    public void init() throws Exception{
        serverSocket = new ServerSocket(PORT);
    }

    @Test
    public void acceptFromPC() {
        while(loop) {
            Log.e(TAG, "socket server waiting ...");
            try {
                Socket server = serverSocket.accept();
                Log.e(TAG, "connected: " + server.getRemoteSocketAddress());

                InputStream inputStream = server.getInputStream();
                byte[] bytes = new byte[1024];
                int len;
                StringBuilder builder = new StringBuilder();
                if ((len = inputStream.read(bytes)) != -1) {
                    builder.append(new String(bytes, 0, len));
                }
                String received = builder.toString();

                Log.e(TAG, "received: " + received);

                if ("stop".equals(received)) {
                    loop = false;
                }

                DataOutputStream out = new DataOutputStream(server.getOutputStream());
                String response = "response for: " + received;
                out.write(response.getBytes());
                out.flush();
                server.close();
            } catch(Exception e) {
                Log.e(TAG, "error: " + e.toString());
                e.printStackTrace();
                break;
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
