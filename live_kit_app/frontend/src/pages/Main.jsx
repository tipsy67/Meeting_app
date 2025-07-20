import { useEffect, useState } from 'react';
import '@livekit/components-styles';
import { useParams, useSearchParams } from 'react-router-dom';
import { Conference } from './Conference';
import { UserNotAtRoom } from './UserNotAtRoom';
import { WaitingTime } from './WaitingTime';
import { ExpiredConference } from './ExpiredConference';


export default function Main() {
  const [searchParams] = useSearchParams();

  const {conferenceId} = useParams();
  const userToken = searchParams.get("token");
  
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);


  useEffect(() => {
    const startChecking = async () => {
        try {
            const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/check_conference/${conferenceId}/${userToken}`);
            const responseData = await response.json();
            const status = responseData?.status;
            if (status) {
                setData(responseData);
            } else {
                const inputError = responseData?.error || "Unknown error";
                setError(inputError);
            }
            
            } catch (err) {
                setError(err);
            } finally {
                setLoading(false);
            } 
    };
    startChecking();
}, []);

  if (loading) return <div>Loading</div>;

  if (error) {
    return (
        <p>{`${error}`}</p>
    )
  };

  if (data) {
    if (data.status == "success") {
        return <Conference conference={data.detail.conference} participant={data.detail.participant} role={data.detail.role}/>
    } if (data.status == "denied") {
        return <UserNotAtRoom/>
    } if (data.status == "expired") {
        return <ExpiredConference/>
    } if (data.status == "pending") {
        return <WaitingTime/>
    } else {
        return <h1>Status not found</h1>
    }
  }

  return <h1>Page Not Found</h1>
}
