document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Ошибка: " + data.error);
        } else {
            // Сохраняем флаг авторизации в localStorage
            localStorage.setItem('isAuthenticated', 'true');
            window.location.href = "/index";
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при авторизации.');
    });
});


// Проверяем авторизацию
window.onload = function() {
    const isAuthenticated = localStorage.getItem('isAuthenticated');
    const currentPath = window.location.pathname;
    
    if (isAuthenticated && currentPath === "/") {
        window.location.href = "/index";  // Перенаправляем на главную страницу
    }
};
