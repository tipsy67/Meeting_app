import { useParticipants, ParticipantTile, ParticipantName, VideoTrack, useTracks, TrackRefContext, GridLayout, ControlBar, Chat, ChatToggle, LayoutContextProvider } from "@livekit/components-react";
import { RoomEvent, Track} from "livekit-client";

export const VideoConferenceCustom = () => {
  const tracks = useTracks(
    [
      { source: Track.Source.Camera, withPlaceholder: true },
      { source: Track.Source.ScreenShare, withPlaceholder: false },
    ],
    { onlySubscribed: true },
  );
  return (
    <> 
    <LayoutContextProvider>
      <GridLayout tracks={tracks}>
        <ParticipantTile>
          <ParticipantName />
          <VideoTrack/>
        </ParticipantTile>
      </GridLayout>
        <ControlBar controls={
          {
            chat:true,
            settings:true
          }
        }>
        </ControlBar>
      </LayoutContextProvider>
    </>
  );
};