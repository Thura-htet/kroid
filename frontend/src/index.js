import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

import { PostList } from './screens/homepage.screen';
import { PostDetail } from './screens/post-detail.screen';
import { Write } from './screens/write.screen';

import { Navbar } from './components/navbar.component';
import { ReplyComment } from './components/comment.component';

import App from "./App"

import * as serviceWorker from './serviceWorker';

// gonna have to improve this
const djangoIdentifier = document.getElementById('kroid');
if (djangoIdentifier) {
    ReactDOM.render(<Navbar />, document.getElementById('kroid-nav'));
    const postList = document.getElementById('post-list');
    if (postList) {
        ReactDOM.render(<PostList />, postList);
    }
    const write = document.getElementById('write');
    if (write) {
        ReactDOM.render(<Write />, write);
    }
    const detailViewIdentifier = document.getElementById('article-detail');
    if (detailViewIdentifier) {
        ReactDOM.render(<PostDetail />, detailViewIdentifier);
        const commentElements = document.querySelectorAll(".child-comment-button");
        if (commentElements) {
            commentElements.forEach(comment => {
                console.log(comment);
                const parentId = comment.dataset.nodeId;
                ReactDOM.render(<ReplyComment parentId={parentId} />, comment);
            });
        }
    }
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
