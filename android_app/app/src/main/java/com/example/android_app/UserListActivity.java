package com.example.android_app;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;

public class UserListActivity extends AppCompatActivity {

    private ListView listUsers;
    private ArrayAdapter<String> adapter;
    private ArrayList<String> items = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_list);

        listUsers = findViewById(R.id.listUsers);
        adapter = new ArrayAdapter<>(
                this,
                android.R.layout.simple_list_item_1,
                items
        );
        listUsers.setAdapter(adapter);

        loadUsers();
    }

    private void loadUsers() {
        new Thread(() -> {
            HttpURLConnection conn = null;
            try {
                URL url = new URL(ApiConfig.BASE_URL + "/get_users");
                conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(5000);

                int code = conn.getResponseCode();
                InputStream is = (code >= 200 && code < 300)
                        ? conn.getInputStream()
                        : conn.getErrorStream();

                BufferedReader br = new BufferedReader(new InputStreamReader(is));
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = br.readLine()) != null) {
                    sb.append(line);
                }
                br.close();

                if (code == 200) {
                    JSONArray arr = new JSONArray(sb.toString());
                    items.clear();
                    for (int i = 0; i < arr.length(); i++) {
                        JSONObject obj = arr.getJSONObject(i);
                        String cardId = obj.getString("card_id");
                        String name   = obj.getString("name");
                        int level     = obj.getInt("access_level");

                        String row = cardId + " | " + name + " | lvl " + level;
                        items.add(row);
                    }

                    runOnUiThread(() -> adapter.notifyDataSetChanged());
                } else {
                    String error = sb.toString();
                    runOnUiThread(() ->
                            Toast.makeText(this,
                                    "Ошибка загрузки: " + error,
                                    Toast.LENGTH_LONG).show());
                }

            } catch (Exception e) {
                String msg = e.getMessage();
                runOnUiThread(() ->
                        Toast.makeText(this,
                                "Сетевая ошибка: " + msg,
                                Toast.LENGTH_LONG).show());
            } finally {
                if (conn != null) conn.disconnect();
            }
        }).start();
    }
}
