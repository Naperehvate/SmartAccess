

// Загрузка списка пользователей
fetch('/get_users')
.then(response => response.json())
.then(users => {
    const userTable = document.getElementById('user-table');
    users.forEach(user => {
        const row = `<tr>
            <td>${user.card_id}</td>
            <td>${user.name}</td>
            <td>${user.access_level}</td>
        </tr>`;
        userTable.innerHTML += row;
    });
})
.catch(error => console.error('Ошибка загрузки пользователей:', error));