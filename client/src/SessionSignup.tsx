import React, { useCallback, useState } from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import Loading from './common/Loading';
import { Session, parseSession } from './ApiTypes';
import { apiUrl } from './AppSettings';
import generateFetchDataFunction from './common/generateFetchDataFunction';

interface RouteParams {
  sessionId: string;
}

const SessionSignup: React.FC = () => {
  const { sessionId } = useParams<RouteParams>();
  const [session, setSession] = useState<Session | undefined>(undefined);

  const getSession = useCallback<() => Promise<string | void>>(
    generateFetchDataFunction(
      `${apiUrl}/session/${sessionId}`,
      (json) => {
        setSession(parseSession(json));
      },
      'There was a problem loading the session info'
    ),
    [setSession]
  );

  return (
    <div>
      <Link component={RouterLink} variant="body1" to="/">
        ← Back to session list
      </Link>
      <Loading loadingFunction={getSession}>
        <Typography variant="h4" component="h1">
          Sign up for a session on {session?.date}
        </Typography>
      </Loading>
    </div>
  );
};

export default SessionSignup;
