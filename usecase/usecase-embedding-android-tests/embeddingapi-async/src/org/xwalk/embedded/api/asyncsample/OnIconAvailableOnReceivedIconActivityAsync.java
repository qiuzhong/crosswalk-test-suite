package org.xwalk.embedded.api.asyncsample;

import android.app.AlertDialog;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.os.Message;
import android.widget.ImageView;
import android.widget.TextView;

import android.app.Activity;
import org.xwalk.core.XWalkInitializer;
import org.xwalk.core.XWalkPreferences;
import org.xwalk.core.XWalkView;
import org.xwalk.core.XWalkUIClient;

public class OnIconAvailableOnReceivedIconActivityAsync extends Activity implements XWalkInitializer.XWalkInitListener {
    private XWalkView mXWalkView;
    private XWalkInitializer mXWalkInitializer;
    private TextView mTitleText1;
    private TextView mTitleText2;
    private ImageView mFavicon1;
    private ImageView mFavicon2;
    private int count1;
    private int count2;

    class TestXWalkUIClientBase extends XWalkUIClient {

        public TestXWalkUIClientBase(XWalkView arg0) {
            super(arg0);
        }

        @Override
        public void onIconAvailable(XWalkView view, String url, Message msg) {
            count1++;
            mTitleText1.setText("onIconAvailable " + count1 + " times");
            msg.sendToTarget();
            super.onIconAvailable(view, url, msg);
        }

        @Override
        public void onReceivedIcon(XWalkView view, String url, Bitmap icon) {
            count2++;
            if(count2 % 2 == 1) {
                mFavicon1.setImageBitmap(icon);
            } else {
                mFavicon2.setImageBitmap(icon);
            }
            mTitleText2.setText("onReceivedIcon " + count2 + " times");
            super.onReceivedIcon(view, url, icon);
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        mXWalkInitializer = new XWalkInitializer(this, this);
        mXWalkInitializer.initAsync();
    }

    @Override
    public final void onXWalkInitStarted() {
        // It's okay to do nothing
    }

    @Override
    public final void onXWalkInitCancelled() {
        // It's okay to do nothing
    }

    @Override
    public final void onXWalkInitFailed() {
        // Do crash or logging or anything else in order to let the tester know if this method get called
    }

    @Override
    public final void onXWalkInitCompleted() {
        StringBuffer mess = new StringBuffer();
        mess.append("Test Purpose: \n\n")
        .append("Verifies onIconAvailable and onReceivedIcon methods can be triggered when icon is available.\n\n")
        .append("Expected Result:\n\n")
        .append("1. Test passes if app show 'onIconAvailable' and the times.\n")
        .append("2. Test passes if app show 'onReceivedIcon'. and the times\n")
        .append("3. Test passes if app show 2 images of cat.");
        new  AlertDialog.Builder(this)
        .setTitle("Info" )
        .setMessage(mess.toString())
        .setPositiveButton("confirm" ,  null )
        .show();

        setContentView(R.layout.embedding_main);
        mXWalkView = (XWalkView) findViewById(R.id.xwalkview_embedding);
        mXWalkView.setUIClient(new TestXWalkUIClientBase(mXWalkView));

        XWalkPreferences.setValue(XWalkPreferences.SUPPORT_MULTIPLE_WINDOWS, true);
        XWalkPreferences.setValue(XWalkPreferences.REMOTE_DEBUGGING, true);
        XWalkPreferences.setValue(XWalkPreferences.JAVASCRIPT_CAN_OPEN_WINDOW, true);
        mTitleText1 = (TextView) findViewById(R.id.titletext1);
        mTitleText2 = (TextView) findViewById(R.id.titletext2);
        mFavicon1 = (ImageView) findViewById(R.id.imageView1);
        mFavicon2 = (ImageView) findViewById(R.id.imageView2);
        mXWalkView.load("file:///android_asset/window_icon.html", null);
    }
}
