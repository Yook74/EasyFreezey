import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import SessionSignup from './SessionSignup';
import ViewSessions from './ViewSessions';

const App: React.FC = () => {
  return (
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
  );
}

export default App;
