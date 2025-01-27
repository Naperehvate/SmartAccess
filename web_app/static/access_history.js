// Загрузка списка логов

fetch('/accsess_history_logs')
.then(response => response.json())
.then(logss => {
    const logsTable = document.getElementById('logs-table');
    logss.reverse().forEach(logs => {
        const row = `<tr>
            <td>${logs.id}</td>
            <td>${logs.event_type}</td>
            <td>${logs.event_details}</td>
            <td>${logs.timestamp}</td>
        </tr>`;
        logsTable.innerHTML += row;
    });
})
.catch(error => console.error('Ошибка загрузки истории:', error));