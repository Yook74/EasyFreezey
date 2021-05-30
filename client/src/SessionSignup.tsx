import React from 'react';
import { useParams } from 'react-router-dom';

interface RouteParams {
  sessionId: string;
}

const SessionSignup: React.FC = () => {
  const { sessionId } = useParams<RouteParams>();
  return (
    <div>Session Signup for {sessionId}</div>
  );
};

export default SessionSignup;