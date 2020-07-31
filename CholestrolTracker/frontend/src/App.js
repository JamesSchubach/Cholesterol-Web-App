import React from 'react';
import logo from './logo.svg';
import './App.css';
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams
} from "react-router-dom";

function App() {
  return (
    <Router>
    <div className="App">
      <Switch>
      <Route path='/dashboard/' component={Dashboard}/>
          <Route path='' component={Login}/>
          </Switch>
    </div>
    </Router>
  );
}

export default App;
