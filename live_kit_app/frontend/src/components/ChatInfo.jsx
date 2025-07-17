import { useEffect } from 'react';
import { useChat } from '@livekit/components-react';
import { VideoConference } from '@livekit/components-react';
import { TestComp } from './TestComp';


export const ChatInfo = () => {
  const { chatMessages, send, isSending } = useChat();

    // send telegram message
    function sendTelegramMessage(botToken, chatId, message) {
        const url = `https://api.telegram.org/bot${botToken}/sendMessage?chat_id=${chatId}&text=${message}`;

        fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
            })
            .then(response => {
            if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
            return response.json();
            })
            .then(data => {
            console.log("Сообщение отправлено:", data);
            })
            .catch(error => {
            console.error("Ошибка при отправке в Telegram:", error);
            });
        }

 
  useEffect(() => {
    let messageToSend = chatMessages.at(-1)?.message;
    if (messageToSend) {
        sendTelegramMessage(
            "ttt",
            "666",
            messageToSend
        );
        console.log(messageToSend)
    }
    
  }, [chatMessages,]);

  return (
    <>
        <VideoConference ControlBar={TestComp} />
    </>
  );
};