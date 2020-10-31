import React from 'react';
import { 
  BrowserRouter as Router,
  Route
} from 'react-router-dom'

import { Navbar } from './components/navbar.component';
import { PostList } from './screens/homepage.screen';
import { PostDetail } from './screens/post-detail.screen';

function App()
{
  return (
    <Router>
      <div className="container">
        <Navbar />
        <Route path="/" exact component={PostList} />
        <Route path="/post/:slug" component={PostDetail} />
      </div>
    </Router>
  );
}

export default App;
