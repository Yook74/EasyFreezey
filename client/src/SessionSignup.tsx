import React from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import Link from '@material-ui/core/Link';
import Typography from '@material-ui/core/Typography';

interface RouteParams {
  sessionId: string;
}

const SessionSignup: React.FC = () => {
  const { sessionId } = useParams<RouteParams>();

  return (
    <div>
      <Link component={RouterLink} variant="body1" to="/">
        ← Back to session list
      </Link>
      <Typography variant="h4" component="h1">
        Sign up for a session on {sessionId}
      </Typography>
    </div>
  );
};

export default SessionSignup;
