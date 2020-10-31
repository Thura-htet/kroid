import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

export function PostDetail(props)
{
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [post, setPost] = useState([]);
    let { slug } = useParams();
  
    // Note: the empty deps array [] means
    // this useEffect will run once
    // similar to componentDidMount()
    useEffect(() => {
      fetch(`http://localhost:8000/api/post/${slug}`)
        .then(res => res.json())
        .then(
          (result) => {
            setIsLoaded(true);
            setPost(result);
          },
          // Note: it's important to handle errors here
          // instead of a catch() block so that we don't swallow
          // exceptions from actual bugs in components.
          (error) => {
            setIsLoaded(true);
            setError(error);
          }
        )
    }, [slug])
  
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
        return (
          // might factor out into a separate component
          <div className='container'>
            <h2>{post.title}</h2>
            <h5>{post.summary}</h5>
            <p>{post.content}</p>
            <form
              data-parent-type="post"
              action={`/api/post/${slug}/comments`}>
              <div className='form-group'>
                <textarea className='form-control'></textarea>
              </div>
              <button className="btn btn-primary">Submit</button>
            </form>
          </div>
        )
      }
  }