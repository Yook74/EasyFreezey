import React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import { Link as RouterLink } from 'react-router-dom';
import { Session } from './ApiTypes';
import './css/SessionList.css';

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
    <TableContainer className="sessions-table" component={Paper}>
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
