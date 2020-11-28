import React, { useState, useEffect } from 'react';

import axios from 'axios';

import { AboutComponent } from '../components/about.component';
import { PostList } from '../components/post.compenent';


export function ProfileScreen(props)
{
    const [isLoaded, setIsLoaded] = useState(false);
    const [about, setAbout] = useState({});
    const [posts, setPosts] = useState([]);

    const path = window.location.pathname;
    const splits = path.split('/');
    // this log is run four times for some reason
    // replace with regex later on
    const username = splits[splits.length-1] ? splits[splits.length-1] : splits[splits.length-2];
    const aboutURL = `http://127.0.0.1:8000/api/profile/${username}/`;
    const postsURL = `http://127.0.0.1:8000/api/posts/${username}/`;


    useEffect(() => {
        axios.get(aboutURL, { withCredentials: true })
        .then(response => {
            console.log(response.data)
            setIsLoaded(true);
            setAbout(response.data);
        })
        .catch(error => alert(`An error has occured: ${error}`));

        axios.get(postsURL, { withCredentials: true })
        .then(response => {
            setPosts(response.data)
        })
        .catch(error => alert(`An error has occured: ${error}`));
    }, [aboutURL, postsURL]);

    if (!isLoaded) {
        return <div>Loading...</div>
    }
    else {
        return (
            <>
                <AboutComponent about={about} />
                <PostList postList={posts} />
            </>
        )
    }
}