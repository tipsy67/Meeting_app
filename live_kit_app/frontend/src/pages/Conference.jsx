import { VideoConference } from '@livekit/components-react';
import '@livekit/components-styles';
import { useState, useEffect } from 'react';
import { LiveKitRoom } from '@livekit/components-react';


export const Conference = ({conference, participant}) => {
  localStorage.setItem("conference", JSON.stringify(conference));
  localStorage.setItem("participant", JSON.stringify(participant));

  const identity = participant.first_name;
  const room = conference.id;
  const is_speaker = participant?.is_speaker || false;

  const [token, setToken] = useState(null);
  
  useEffect(() => {
    fetch(`${import.meta.env.VITE_BACKEND_URL}/get-token?name=${identity}&room=${room}&is_speaker=${is_speaker}`)
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
        <VideoConference/>
      </LiveKitRoom>
  );
};