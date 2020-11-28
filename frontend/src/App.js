import React from 'react';
import { 
  BrowserRouter as Router,
  Route
} from 'react-router-dom'

import { Navbar } from './components/navbar.component';
import { HomePage } from './screens/homepage.screen';
import { PostDetail } from './screens/post-detail.screen';
import { Write } from './screens/write.screen';
import { ProfileScreen } from './screens/profile.screen';

function App()
{
  return (
    <Router>
      <div className="container">
        <Navbar />
        <Route path="/" exact component={HomePage} />
        <Route path="/write/" component={Write} />
        <Route path="/post/:slug/" component={PostDetail} />
        <Route path="/profile/:username" component={ProfileScreen} />
      </div>
    </Router>
  );
}

export default App;
