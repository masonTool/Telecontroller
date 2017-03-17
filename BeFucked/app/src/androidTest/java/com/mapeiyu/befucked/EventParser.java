package com.mapeiyu.befucked;

import android.app.Instrumentation;
import android.os.SystemClock;
import android.support.test.uiautomator.UiDevice;
import android.util.Log;
import android.view.InputDevice;
import android.view.MotionEvent;

/**
 * Created by mapeiyu on 17-3-15.
 */

public class EventParser {
    public static final String TAG = "EventParser";

    private static long downtime = 0;

    public static void parseEvent(Instrumentation instrumentation, String eventStr) {
        String[] values = eventStr.split(",");
        int type = Integer.parseInt(values[0]);
        int action = Integer.parseInt(values[1]);
        int data1 = Integer.parseInt(values[2]);
        int data2 = Integer.parseInt(values[3]);

        if (type == EventConstant.MOUSE_TYPE) {
            if (action == EventConstant.MOUSE_ACTION_LEFT_DOWN) {
                Log.e(TAG, "down action");
                downtime = SystemClock.uptimeMillis();
                MotionEvent event = MotionEvent.obtain(downtime, downtime, MotionEvent.ACTION_DOWN, data1, data2, 0);
                event.setSource(InputDevice.SOURCE_TOUCHSCREEN);
                instrumentation.getUiAutomation().injectInputEvent(event, true);
            } else if (action == EventConstant.MOUSE_ACTION_LEFT_UP) {
                MotionEvent event = MotionEvent.obtain(downtime, SystemClock.uptimeMillis(), MotionEvent.ACTION_UP, data1, data2, 0);
                event.setSource(InputDevice.SOURCE_TOUCHSCREEN);
                instrumentation.getUiAutomation().injectInputEvent(event, true);
                Log.e(TAG, "up action");
                downtime = 0;
            } else if (action == EventConstant.MOUSE_ACTION_MOVE) {
                int width = UiDevice.getInstance(instrumentation).getDisplayWidth();//TODO
                int height = UiDevice.getInstance(instrumentation).getDisplayHeight();//TODO
                MouseManager.getInstance(instrumentation.getTargetContext()).move(data1 - width/2, data2 - height/2);
                if (downtime > 0) {
                    Log.e(TAG, "move action");
                    MotionEvent event = MotionEvent.obtain(downtime, SystemClock.uptimeMillis(), MotionEvent.ACTION_MOVE, data1, data2, 0);
                    event.setSource(InputDevice.SOURCE_TOUCHSCREEN);
                    instrumentation.getUiAutomation().injectInputEvent(event, true);
                }
            }
            //TODO

        }
    }

}
