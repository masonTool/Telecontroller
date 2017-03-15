package com.mapeiyu.befucked;

import android.content.Context;
import android.graphics.PixelFormat;
import android.os.Handler;
import android.os.Looper;
import android.view.LayoutInflater;
import android.view.View;
import android.view.WindowManager;
import android.view.WindowManager.LayoutParams;

/**
 * Created by mapeiyu on 17-3-15.
 */

public class MouseManager {
    private static MouseManager instance = null;

    public static MouseManager getInstance(Context context) {
        if (instance == null) {
            synchronized (MouseManager.class) {
                if (instance == null) {
                    instance = new MouseManager(context);
                }
            }
        }
        return instance;
    }

    private WindowManager windowManager = null;
    private LayoutParams params = null;
    private View contentView = null;
    private View circleView = null;
    private Handler handler = null;

    private MouseManager(Context context) {
        handler = new Handler(Looper.getMainLooper());
        windowManager =  (WindowManager)context.getApplicationContext().getSystemService(Context.WINDOW_SERVICE);
        params = new LayoutParams();
        params.type = LayoutParams.TYPE_PHONE;
        params.flags = LayoutParams.FLAG_NOT_FOCUSABLE | LayoutParams.FLAG_NOT_TOUCHABLE | LayoutParams.FLAG_LAYOUT_IN_SCREEN;
        params.format = PixelFormat.RGBA_8888;
        params.x = 0;
        params.y = 0;
        params.width = 100;
        params.height = 100;
        contentView = LayoutInflater.from(context).inflate(R.layout.mouse_layout, null);
        circleView = contentView.findViewById(R.id.circle_view);

        handler.post(new Runnable() {
            @Override
            public void run() {
                windowManager.addView(contentView, params);
            }
        });
    }

    public void move(final int x, final int y) {
        handler.post(new Runnable() {
            @Override
            public void run() {
                params.x = x;
                params.y = y;
                windowManager.updateViewLayout(contentView, params);
            }
        });

    }

    public void anim() {
        //TODO  anim action
        if (circleView.getVisibility() != View.VISIBLE) {
            circleView.setVisibility(View.VISIBLE);
        } else {
            circleView.setVisibility(View.GONE);
        }
    }
}
