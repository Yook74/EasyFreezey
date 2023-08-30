import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { ThemeProvider, createMuiTheme } from '@mui/material/styles';
import SessionSignup from './SessionSignup';
import ViewSessions from './ViewSessions';

const theme = createMuiTheme();

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Switch>
          <Route path="/signup/:sessionId">
            <SessionSignup />
          </Route>
          <Route path="/">
            <ViewSessions />
          </Route>
        </Switch>
      </Router>
    </ThemeProvider>
  );
};

export default App;
