import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

import { PostList } from './screens/homepage.screen';
import { Navbar } from './components/navbar.component';

import App from "./App"

import * as serviceWorker from './serviceWorker';

// gonna have to improve this
const djangoIdentifier = document.getElementById('kroid');
if (djangoIdentifier) {
    ReactDOM.render(<Navbar />, document.getElementById('kroid-nav'));
    ReactDOM.render(<PostList />, document.getElementById('post-list'));
}

const appElement =  document.getElementById('root');
if (appElement)
{
    ReactDOM.render(<App />, appElement);
}

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
