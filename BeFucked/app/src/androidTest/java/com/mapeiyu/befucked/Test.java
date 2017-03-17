package com.mapeiyu.befucked;

import android.app.Instrumentation;
import android.os.SystemClock;
import android.support.test.InstrumentationRegistry;
import android.support.test.runner.AndroidJUnit4;
import android.view.InputDevice;
import android.view.MotionEvent;

import org.junit.runner.RunWith;

/**
 * Created by meizu on 2017/3/18.
 */

@RunWith(AndroidJUnit4.class)
public class Test {

    @org.junit.Test
    public void testClick() {
        Instrumentation instrumentation = InstrumentationRegistry.getInstrumentation();
        long time = SystemClock.uptimeMillis();

        MotionEvent down = MotionEvent.obtain(time, time, MotionEvent.ACTION_DOWN, 300, 300, 0);
        down.setSource(InputDevice.SOURCE_TOUCHSCREEN);
        instrumentation.getUiAutomation().injectInputEvent(down, true);

        MotionEvent up = MotionEvent.obtain(time, time+ 10, MotionEvent.ACTION_UP, 300, 300, 0);
        up.setSource(InputDevice.SOURCE_TOUCHSCREEN);
        instrumentation.getUiAutomation().injectInputEvent(up, true);
    }

}
