import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { getData } from '../actions/http.helpers';

import parse from 'html-react-parser';

import { SubmitCommentButton } from '../components/buttons.component'

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
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
        console.log(post)
        return (
          // might factor out into a separate component
          <div className='container'>
            <h2>{post.title}</h2>
            <h5>{post.summary}</h5>
            <div>
              {/* might be inefficient and unnecessary */}
              {/* and the syntax highlighting is gone. */}
              {parse(`${post.html_content}`)}
            </div>
            {/* separate into a comment component */}
            <div className='comment'>
              <div className='form-group'>
                <textarea ref={commentInput} className='form-control'></textarea>
              </div>
              <SubmitCommentButton url={comment_url} parentId={null}
                parentType='post' commentInput={commentInput} />
            </div>
          </div>
        )
      }
  }