import { useRoomContext, VideoConference} from "@livekit/components-react";
import { RoomEvent } from "livekit-client";
import { WaitingModerator } from "./WaitingModerator";
import { useEffect, useState } from "react";

export const StartConference = () => {
  const speakerId = JSON.parse(localStorage.getItem("conference")).speaker.user_id;
  const role = JSON.parse(localStorage.getItem("role"));
  const [speakerJoined, setSpeakerJoined] = useState(false);

  const room = useRoomContext();

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