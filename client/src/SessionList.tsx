import React from 'react';
import { Session } from './ApiTypes';

type Props = {
  sessions: Session[];
};

const SessionList: React.FC<Props> = (props: Props) => {
  return <div>there are {props.sessions.length} sessions</div>;
};

export default SessionList;
