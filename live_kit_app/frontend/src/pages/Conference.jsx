import { VideoConference } from '@livekit/components-react';
import '@livekit/components-styles';
import { useState, useEffect } from 'react';
import { LiveKitRoom } from '@livekit/components-react';
import { WaitingModerator } from './WaitingModerator';
import { StartConference } from './StartConference';


export const Conference = ({conference, participant, role}) => {
  localStorage.setItem("conference", JSON.stringify(conference));
  localStorage.setItem("participant", JSON.stringify(participant));
  localStorage.setItem("role", JSON.stringify(role));

  const identity = participant.first_name;
  const userId = participant.id;
  const room = conference.id;


  const [token, setToken] = useState(null);
  
  useEffect(() => {
    fetch(`${import.meta.env.VITE_BACKEND_URL}/get-token?user_id=${userId}&name=${identity}&room=${room}&is_speaker=${role === "speaker"}`)
      .then(res => res.json())
      .then(data => setToken(data.access_token));
  }, []);

  if (!token) return <div>Loading</div>;

  return (
      <LiveKitRoom data-lk-theme="default"
        token={token}
        serverUrl={import.meta.env.VITE_LIVEKIT_URL}
        connect={true}
        video={true}
        audio={true}
      >
        <StartConference/>
      </LiveKitRoom>
  );
};