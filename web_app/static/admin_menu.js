

// Добавление пользователя
function addUser() {
    const cardId = prompt("Введите ID карты:").trim();
    const name = prompt("Введите имя пользователя:").trim();
    const accessLevel = prompt("Введите уровень доступа (1 - стандартный, 2 - админ):").trim();

    if (!cardId || !name || !accessLevel) {
        alert("Все поля должны быть заполнены!");
        return;
    }

    fetch('/add_user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ card_id: cardId, name: name, access_level: accessLevel })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Ошибка: " + data.error);
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при добавлении пользователя.');
    });
}

// Удаление пользователя
function deleteUser() {
    const cardId = prompt("Введите ID карты для удаления:").trim();

    if (!cardId) {
        alert("Введите ID карты!");
        return;
    }

    fetch('/delete_user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ card_id: cardId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Ошибка: " + data.error);
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при удалении пользователя.');
    });
}


// Редактирование пользователя
function editUser() {
    const cardId = prompt("Введите ID карты пользователя для редактирования:").trim();
    if (!cardId) {
        alert("Введите ID карты!");
        return;
    }

    const newName = prompt("Введите новое имя пользователя:").trim();
    if (!newName) {
        alert("Имя пользователя не может быть пустым!");
        return;
    }

    fetch('/edit_user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ card_id: cardId, new_name: newName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Ошибка: " + data.error);
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при редактировании пользователя.');
    });
}