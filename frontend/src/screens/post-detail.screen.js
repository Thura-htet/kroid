// might remove later
import React, { useState, useEffect} from 'react';
import { getData } from '../actions/http.helpers';

import { FullArticle } from '../components/post-detail.component';
import { CommentForm } from '../components/comment.component';

export function PostDetail(props)
{
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [post, setPost] = useState([]);

    const path = window.location.pathname;
    const splits = path.split('/');
    // this log is run four times for some reason
    // replace with regex later on
    const slug = splits[splits.length-1] ? splits[splits.length-1] : splits[splits.length-2]
    console.log(slug)
    const post_url = `http://localhost:8000/api/post/${slug}/`;

    useEffect(() => {
      getData(post_url)
      .then(response => {
        setIsLoaded(response.isLoaded);
        setError(response.error);
        setPost(response.data);
      });
    }, [post_url])
  
    if (error) {
      return <div>Error: {error}</div>; // changed from {error.message}
    }
    else if (!isLoaded) {
      return <div>Loading...</div>;
    }
    else {
        return (
          <div className='container'>
            <FullArticle post={post} />
            <CommentForm parentId={''} parentType={'post'} />
          </div>
        )
      }
  }