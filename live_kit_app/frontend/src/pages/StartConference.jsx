import { useParticipants, ParticipantTile, ParticipantName, VideoTrack, useTracks, TrackRefContext, GridLayout, ControlBar, Chat, ChatToggle, LayoutContextProvider, VideoConference } from "@livekit/components-react";
import { ParticipantEvent, RoomEvent, Track} from "livekit-client";
import { WaitingModerator } from "./WaitingModerator";

export const StartConference = () => {
  const speakerId = JSON.parse(localStorage.getItem("conference")).speaker.user_id;
  const role = JSON.parse(localStorage.getItem("role"));
  const participants = useParticipants({updateOnlyOn:RoomEvent.ParticipantConnected});
  
  const speakerExist = participants.some(item => item.identity === String(speakerId));
  if (role === "listener" && !speakerExist) {
    return <WaitingModerator/>
  } 
  return (
    <> 
      <VideoConference/>
    </>
  );
};