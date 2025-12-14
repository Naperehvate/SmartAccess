package com.example.android_app;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.text.InputType;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class AdminMenuActivity extends AppCompatActivity {

    private Button btnAddUser, btnDeleteUser, btnEditUser;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_admin_menu);

        btnAddUser    = findViewById(R.id.btnAddUser);
        btnDeleteUser = findViewById(R.id.btnDeleteUser);
        btnEditUser   = findViewById(R.id.btnEditUser);

        btnAddUser.setOnClickListener(v -> showAddUserDialog());
        btnDeleteUser.setOnClickListener(v -> showDeleteUserDialog());
        btnEditUser.setOnClickListener(v -> showEditUserDialog());
    }

    private void showAddUserDialog() {
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        int pad = (int) (16 * getResources().getDisplayMetrics().density);
        layout.setPadding(pad, pad, pad, pad);

        EditText etCardId = new EditText(this);
        etCardId.setHint("ID карты");
        layout.addView(etCardId);

        EditText etName = new EditText(this);
        etName.setHint("Имя пользователя");
        layout.addView(etName);

        EditText etLevel = new EditText(this);
        etLevel.setHint("Уровень доступа (1/2/3)");
        etLevel.setInputType(InputType.TYPE_CLASS_NUMBER);
        layout.addView(etLevel);

        new AlertDialog.Builder(this)
                .setTitle("Добавить пользователя")
                .setView(layout)
                .setPositiveButton("OK", (dialog, which) -> {
                    String cardId = etCardId.getText().toString().trim();
                    String name   = etName.getText().toString().trim();
                    String level  = etLevel.getText().toString().trim();

                    if (cardId.isEmpty() || name.isEmpty() || level.isEmpty()) {
                        Toast.makeText(this, "Все поля обязательны", Toast.LENGTH_SHORT).show();
                        return;
                    }
                    int accessLevel;
                    try {
                        accessLevel = Integer.parseInt(level);
                    } catch (NumberFormatException e) {
                        Toast.makeText(this, "Уровень доступа должен быть числом", Toast.LENGTH_SHORT).show();
                        return;
                    }

                    sendAddUser(cardId, name, accessLevel);
                })
                .setNegativeButton("Отмена", null)
                .show();
    }

    private void showDeleteUserDialog() {
        EditText etCardId = new EditText(this);
        etCardId.setHint("ID карты");

        int pad = (int) (16 * getResources().getDisplayMetrics().density);
        etCardId.setPadding(pad, pad, pad, pad);

        new AlertDialog.Builder(this)
                .setTitle("Удалить пользователя")
                .setView(etCardId)
                .setPositiveButton("OK", (dialog, which) -> {
                    String cardId = etCardId.getText().toString().trim();
                    if (cardId.isEmpty()) {
                        Toast.makeText(this, "Введите ID карты", Toast.LENGTH_SHORT).show();
                        return;
                    }
                    sendDeleteUser(cardId);
                })
                .setNegativeButton("Отмена", null)
                .show();
    }

    private void showEditUserDialog() {
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        int pad = (int) (16 * getResources().getDisplayMetrics().density);
        layout.setPadding(pad, pad, pad, pad);

        EditText etCardId = new EditText(this);
        etCardId.setHint("ID карты");
        layout.addView(etCardId);

        EditText etNewName = new EditText(this);
        etNewName.setHint("Новое имя");
        layout.addView(etNewName);

        new AlertDialog.Builder(this)
                .setTitle("Редактировать пользователя")
                .setView(layout)
                .setPositiveButton("OK", (dialog, which) -> {
                    String cardId   = etCardId.getText().toString().trim();
                    String newName  = etNewName.getText().toString().trim();

                    if (cardId.isEmpty() || newName.isEmpty()) {
                        Toast.makeText(this, "Заполните оба поля", Toast.LENGTH_SHORT).show();
                        return;
                    }
                    sendEditUser(cardId, newName);
                })
                .setNegativeButton("Отмена", null)
                .show();
    }

    private void sendAddUser(String cardId, String name, int accessLevel) {
        new Thread(() -> {
            HttpURLConnection conn = null;
            try {
                URL url = new URL(ApiConfig.BASE_URL + "/add_user");
                conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
                conn.setDoOutput(true);

                JSONObject body = new JSONObject();
                body.put("card_id", cardId);
                body.put("name", name);
                body.put("access_level", accessLevel);

                OutputStream os = conn.getOutputStream();
                os.write(body.toString().getBytes("UTF-8"));
                os.flush();
                os.close();

                int code = conn.getResponseCode();
                InputStream is = (code >= 200 && code < 300)
                        ? conn.getInputStream()
                        : conn.getErrorStream();

                String resp = readStream(is);

                runOnUiThread(() -> {
                    if (code == 200) {
                        Toast.makeText(this, "Пользователь добавлен", Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(this, "Ошибка добавления: " + resp, Toast.LENGTH_LONG).show();
                    }
                });

            } catch (Exception e) {
                String msg = e.getMessage();
                runOnUiThread(() ->
                        Toast.makeText(this, "Сетевая ошибка: " + msg, Toast.LENGTH_LONG).show());
            } finally {
                if (conn != null) conn.disconnect();
            }
        }).start();
    }

    private void sendDeleteUser(String cardId) {
        new Thread(() -> {
            HttpURLConnection conn = null;
            try {
                URL url = new URL(ApiConfig.BASE_URL + "/delete_user");
                conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
                conn.setDoOutput(true);

                JSONObject body = new JSONObject();
                body.put("card_id", cardId);

                OutputStream os = conn.getOutputStream();
                os.write(body.toString().getBytes("UTF-8"));
                os.flush();
                os.close();

                int code = conn.getResponseCode();
                InputStream is = (code >= 200 && code < 300)
                        ? conn.getInputStream()
                        : conn.getErrorStream();

                String resp = readStream(is);

                runOnUiThread(() -> {
                    if (code == 200) {
                        Toast.makeText(this, "Пользователь удалён", Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(this, "Ошибка удаления: " + resp, Toast.LENGTH_LONG).show();
                    }
                });

            } catch (Exception e) {
                String msg = e.getMessage();
                runOnUiThread(() ->
                        Toast.makeText(this, "Сетевая ошибка: " + msg, Toast.LENGTH_LONG).show());
            } finally {
                if (conn != null) conn.disconnect();
            }
        }).start();
    }

    private void sendEditUser(String cardId, String newName) {
        new Thread(() -> {
            HttpURLConnection conn = null;
            try {
                URL url = new URL(ApiConfig.BASE_URL + "/edit_user");
                conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
                conn.setDoOutput(true);

                JSONObject body = new JSONObject();
                body.put("card_id", cardId);
                body.put("new_name", newName);

                OutputStream os = conn.getOutputStream();
                os.write(body.toString().getBytes("UTF-8"));
                os.flush();
                os.close();

                int code = conn.getResponseCode();
                InputStream is = (code >= 200 && code < 300)
                        ? conn.getInputStream()
                        : conn.getErrorStream();

                String resp = readStream(is);

                runOnUiThread(() -> {
                    if (code == 200) {
                        Toast.makeText(this, "Имя обновлено", Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(this, "Ошибка обновления: " + resp, Toast.LENGTH_LONG).show();
                    }
                });

            } catch (Exception e) {
                String msg = e.getMessage();
                runOnUiThread(() ->
                        Toast.makeText(this, "Сетевая ошибка: " + msg, Toast.LENGTH_LONG).show());
            } finally {
                if (conn != null) conn.disconnect();
            }
        }).start();
    }

    private String readStream(InputStream is) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(is));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = br.readLine()) != null) sb.append(line);
        br.close();
        return sb.toString();
    }
}
