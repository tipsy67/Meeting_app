import { useEffect, useState } from 'react';
import { LiveKitRoom, GridLayout, ParticipantTile, useTracks} from '@livekit/components-react';
import '@livekit/components-styles';


export const TestComp = () => {
  const { tracks } = useTracks();
  if (!Array.isArray(tracks) || tracks.length === 0) return <div>Ожидание участников...</div>;

  return (
    <>
        <GridLayout tracks={tracks}>
          <ParticipantTile />
        </GridLayout>
    </>
  );
};