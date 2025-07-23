

export default function sendTelegramMessage(conference_id, message, name) {
    const url = `${import.meta.env.VITE_BACKEND_URL}/send_message_to_tg`;
    const messageData = {
        "conference_id": conference_id,
        "text": message,
        "name": name
    }
    console.log("VALIDATION", JSON.stringify(messageData))
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(messageData)
        })
        .then(response => {
        if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
        return response.json();
        })
        .then(data => {
        console.log("Сообщение отправлено:", data);
        })
        .catch(error => {
        console.error("Ошибка при обращении в backend", error);
        });
    }
