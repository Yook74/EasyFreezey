import React from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Link from '@material-ui/core/Link';
import { Link as RouterLink } from 'react-router-dom';
import { Session } from './ApiTypes';

type Props = {
  sessions: Session[];
};

const SessionList: React.FC<Props> = (props: Props) => {
  const { sessions } = props;
  if (sessions.length === 0) {
    return (
      <Typography variant="body1">
        There are currently no sessions planned.
      </Typography>
    );
  }

  return (
    <TableContainer component={Paper}>
      <Table aria-label="list of sessions">
        <TableHead>
          <TableRow>
            <TableCell>Session date</TableCell>
            <TableCell>Link to sign up</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {sessions.map((session) => (
            <TableRow key={session.id}>
              <TableCell>{session.date}</TableCell>
              <TableCell>
                <Link component={RouterLink} to={`/signup/${session.id}`}>
                  Sign up
                </Link>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default SessionList;
