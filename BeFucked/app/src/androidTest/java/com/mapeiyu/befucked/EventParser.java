package com.mapeiyu.befucked;

import android.content.Context;

/**
 * Created by mapeiyu on 17-3-15.
 */

public class EventParser {

    public static void parseEvent(Context context, String eventStr) {
        String[] values = eventStr.split(",");
        if (Integer.parseInt(values[0]) == 0 && Integer.parseInt(values[1]) == 0) {
            int x = Integer.parseInt(values[2]);
            int y = Integer.parseInt(values[3]);
            MouseManager.getInstance(context).move(x, y);
        }
    }

}
