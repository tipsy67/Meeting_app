import { useEffect, useState } from 'react';
import { LiveKitRoom, GridLayout, ParticipantTile, useTracks} from '@livekit/components-react';
import '@livekit/components-styles';
import { WaitingTime } from './pages/WaitingTime';

const identity = 'dmitrii zimin';
const room = 'first_test_room';

function App() {
  const [token, setToken] = useState(null);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_BACKEND_URL}/get-token?name=${identity}`)
      .then(res => res.json())
      .then(data => setToken(data.access_token));
  }, []);
  if (!token) return <div>Loading</div>;

  return (
    // <LiveKitRoom data-lk-theme="default"
    //   token={token}
    //   serverUrl={import.meta.env.VITE_LIVEKIT_URL}
    //   connect={true}
    //   video={true}
    //   audio={true}
    // >
      
    // </LiveKitRoom>
    <WaitingTime/>
  );
}

export default App;