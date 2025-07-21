

export default function sendTelegramMessage(chatId, message) {
    const url = `${import.meta.env.VITE_BACKEND_URL}/send_message_to_tg`;
    const messageData = {
        "chat_id": chatId,
        "text": message
    }
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: messageData
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
