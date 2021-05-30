import React, { useCallback, useState } from 'react';
import Typography from '@material-ui/core/Typography';
import Loading from './common/Loading';
import SessionList from './SessionList';
import { Session, parseSessionListResponse } from './ApiTypes';

const ViewSessions: React.FC = () => {
  const [sessions, setSessions] = useState<Session[]>([]);

  const getSessions = useCallback<() => Promise<string | void>>(() => {
    return new Promise((resolve, reject) => {
      fetch('http://localhost:5000/session')
        .then((response) => {
          return response.json();
        })
        .then((json: any) => {
          try {
            setSessions(parseSessionListResponse(json));
            resolve();
          } catch (e) {
            return Promise.reject();
          }
        })
        .catch((error: Error) => {
          reject('There was a problem loading the list of sessions');
        });
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
