import React from 'react';
import { useParams } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';

interface RouteParams {
  sessionId: string;
}

const SessionSignup: React.FC = () => {
  const { sessionId } = useParams<RouteParams>();
  return (
    <div>
      <Typography variant="h4" component="h1">
        Sign up for a session on {sessionId}
      </Typography>
    </div>
  );
};

export default SessionSignup;