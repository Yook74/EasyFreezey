import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { StylesProvider } from '@material-ui/core/styles';
import SessionSignup from './SessionSignup';
import ViewSessions from './ViewSessions';

const App: React.FC = () => {
  // injectFirst allows for overriding Material UI styles with regular CSS
  return (
    <StylesProvider injectFirst>
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
    </StylesProvider>
  );
};

export default App;
