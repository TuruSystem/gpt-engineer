package com.gorqai.chat;

import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import okhttp3.*;
import java.io.IOException;

public class MainActivity extends AppCompatActivity {
    private EditText input;
    private Button sendBtn;
    private TextView chatView;
    private final OkHttpClient client = new OkHttpClient();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        input = findViewById(R.id.input);
        sendBtn = findViewById(R.id.sendBtn);
        chatView = findViewById(R.id.chatView);
        sendBtn.setOnClickListener(v -> sendMessage());
    }
    private void sendMessage() {
        String message = input.getText().toString();
        RequestBody body = RequestBody.create(MediaType.parse("application/json"), "{\"message\":\"" + message + "\"}");
        Request request = new Request.Builder().url("http://10.0.2.2:7860/api/chat").post(body).build();
        client.newCall(request).enqueue(new Callback() {
            @Override public void onFailure(Call call, IOException e) { }
            @Override public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    String resp = response.body().string();
                    runOnUiThread(() -> chatView.append("Bot: " + resp + "\n"));
                }
            }
        });
        chatView.append("You: " + message + "\n");
        input.setText("");
    }
}
