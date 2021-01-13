// might remove later
import React, { useState, useEffect} from 'react';

import axios from 'axios';

import { FullArticle } from '../components/post-detail.component';
import { Comments } from '../components/comment.component';

export function PostDetail(props)
{
    const [isLoaded, setIsLoaded] = useState(false);
    const [post, setPost] = useState([]);

    const path = window.location.pathname;
    const splits = path.split('/');
    // this log is run four times for some reason
    // replace with regex later on
    const slug = splits[splits.length-1] ? splits[splits.length-1] : splits[splits.length-2];
    const post_url = `http://127.0.0.1:8000/api/post/${slug}`;

    useEffect(() => {
      axios.get(post_url, { withCredentials: true })
      .then(response => {
        setIsLoaded(true);
        setPost(response.data);
      })
      .catch(error => alert(`An error has occured: ${error}`))
    }, [post_url]);
  
    if (!isLoaded) {
      return <div>Loading...</div>;
    }
    else {
        return (
          <>
            <FullArticle post={post} />
            <Comments url={`${post_url}/comments`} />
          </>
        )
      }
  }