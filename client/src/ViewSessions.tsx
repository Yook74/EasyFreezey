import React, { useCallback, useState } from 'react';
import Typography from '@material-ui/core/Typography';
import Loading from './common/Loading';
import SessionList from './SessionList';
import { Session } from './ApiTypes';

const ViewSessions: React.FC = () => {
  const [sessions, setSessions] = useState<Session[]>([]);

  const getSessions = useCallback<() => Promise<string | void>>(() => {
    return new Promise((resolve, reject) => {
      setSessions([{ id: 1, date: '11 Jan' }]);
      resolve();
    });
  }, [setSessions]);

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
