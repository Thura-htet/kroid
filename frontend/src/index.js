import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

import { PostList } from './screens/homepage.screen';
import { Navbar } from './components/navbar.component';

import * as serviceWorker from './serviceWorker';

ReactDOM.render(
    <Navbar />,
    document.getElementById('kroid-nav')
);

ReactDOM.render(
    <PostList />,
    document.getElementById('kroid')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
