import { useDataChannel, useChat, useRoomContext, VideoConference} from "@livekit/components-react";
import { RoomEvent } from "livekit-client";
import { WaitingModerator } from "./WaitingModerator";
import { useEffect, useState } from "react";
import sendTelegramMessage from "../assets/js/sendMessageToTelegram";

export const StartConference = () => {
  const conferenceId = JSON.parse(localStorage.getItem("conference")).id;
  const speakerId = JSON.parse(localStorage.getItem("conference")).speaker.user_id;
  const role = JSON.parse(localStorage.getItem("role"));
  const [speakerJoined, setSpeakerJoined] = useState(false);

  const room = useRoomContext();

  // if localUser is Speaker -> send message to telegram (useDataChannel - latestMessage)
  const { chatMessages, send, isSending } = useChat()

  useEffect(() => {
    if (chatMessages.length > 0 && role !== "listener") {
      const data = chatMessages[chatMessages.length - 1]
      sendTelegramMessage(conferenceId, data.message, data.from?.name)
    }
  })

  const checkIfSpeakerPresent = () => {
    return Array.from(room.remoteParticipants).some(
      (p) => p[0] == String(speakerId)
    )
  };

  useEffect(() => {
    if (role !== "listener") {
      setSpeakerJoined(true);
      return;
    }

    const updateSpeakerState = () => {
      const isPresent = checkIfSpeakerPresent();
      setSpeakerJoined(isPresent);
    };

    // при маунте сразу проверяем
    updateSpeakerState();

    // подписываемся на вход/выход
    room.on(RoomEvent.Connected, () => {updateSpeakerState()});
    room.on(RoomEvent.ParticipantConnected, (participant) => {participant.identity === String(speakerId) ? setSpeakerJoined(true) : setSpeakerJoined(speakerJoined)});
    room.on(RoomEvent.ParticipantDisconnected, (participant) => {participant.identity === String(speakerId) ? setSpeakerJoined(false) : setSpeakerJoined(speakerJoined)});

    return () => {
      room.off(RoomEvent.ParticipantConnected, (participant) => {participant.identity === String(speakerId) ? setSpeakerJoined(true) : setSpeakerJoined(speakerJoined)});
      room.off(RoomEvent.ParticipantDisconnected, (participant) => {participant.identity === String(speakerId) ? setSpeakerJoined(false) : setSpeakerJoined(speakerJoined)});
    };
  }, [room,]);


  return (
    <> 
      {speakerJoined ? <VideoConference /> : <WaitingModerator />}
    </>
  );
};