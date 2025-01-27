

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

// Эмуляция работы
function emulateSystem() {
    alert("Эмуляция работы системы. Действия выполняются на сервере.");
}
