package com.example.android_app;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;


public class HomeActivity extends AppCompatActivity {

    private Button btnUsers;
    private Button btnHistory;
    private Button btnAdmin;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        btnUsers   = findViewById(R.id.btnUsers);
        btnHistory = findViewById(R.id.btnHistory);
        btnAdmin   = findViewById(R.id.btnAdmin);

        btnUsers.setOnClickListener(v ->
                startActivity(new Intent(this, UserListActivity.class)));

        btnHistory.setOnClickListener(v ->
                startActivity(new Intent(this, AccessHistoryActivity.class)));

        btnAdmin.setOnClickListener(v ->
                startActivity(new Intent(this, AdminMenuActivity.class)));
    }
}
