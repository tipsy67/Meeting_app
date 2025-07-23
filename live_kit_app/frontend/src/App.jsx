import { useEffect, useState } from 'react';
import '@livekit/components-styles';
import { BrowserRouter as Router, Routes, Route, Link  } from 'react-router-dom';
import Main from './pages/Main';


export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/:conferenceId" element={<Main/>} />
      </Routes>
    </Router>
  )
}
