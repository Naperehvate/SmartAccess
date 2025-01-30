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
            window.location.href = "/";
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при авторизации.');
    });
});