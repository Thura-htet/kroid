// might remove later
import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { getData } from '../actions/http.helpers';

import { SubmitCommentButton } from '../components/buttons.component';
import { FullArticle } from '../components/post-detail.component';

export function PostDetail(props)
{
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [post, setPost] = useState([]);

    let { slug } = useParams();
    const post_url = `http://localhost:8000/api/post/${slug}/`;
    const comment_url = `http://localhost:8000/api/post/${slug}/comments/`;

    const commentInput = useRef();
  
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
            <div className='parent-comment' data-parent-type='post' data-parent-id=''>
              <div className='form-group'>
                <textarea ref={commentInput} className='form-control'></textarea>
              </div>
              <SubmitCommentButton url={comment_url} commentInput={commentInput} />
            </div>
          </div>
        )
      }
  }