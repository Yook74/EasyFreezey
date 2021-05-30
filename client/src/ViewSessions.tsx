import React, { useCallback, useState } from 'react';
import Typography from '@material-ui/core/Typography';
import Loading from './common/Loading';
import SessionList from './SessionList';
import { Session, parseSessionListResponse } from './ApiTypes';
import { apiUrl } from './AppSettings';
import generateFetchDataFunction from './common/generateFetchDataFunction';

const ViewSessions: React.FC = () => {
  const [sessions, setSessions] = useState<Session[]>([]);

  const getSessions = useCallback<() => Promise<string | void>>(
    generateFetchDataFunction(
      `${apiUrl}/session`,
      (json) => {
        setSessions(parseSessionListResponse(json));
      },
      'There was a problem loading the list of sessions'
    ),
    [setSessions]
  );

  return (
    <div>
      <Typography variant="h4" component="h1">
        Find a session
      </Typography>
      <Loading loadingFunction={getSessions}>
        <SessionList sessions={sessions} />
      </Loading>
    </div>
  );
};

export default ViewSessions;
