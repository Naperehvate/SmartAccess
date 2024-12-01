// Добавление пользователя
function addUser() {
    const cardId = prompt("Введите ID карты:");
    const name = prompt("Введите имя пользователя:");
    const accessLevel = prompt("Введите уровень доступа (1 - стандартный, 2 - админ):");

    fetch('/add_user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ card_id: cardId, name, access_level: accessLevel })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Ошибка:', error));
}

// Удаление пользователя
function deleteUser() {
    const cardId = prompt("Введите ID карты для удаления:");

    fetch('/delete_user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ card_id: cardId })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Ошибка:', error));
}

// Эмуляция работы
function emulateSystem() {
    alert("Эмуляция работы системы. Действия выполняются на сервере.");
}
