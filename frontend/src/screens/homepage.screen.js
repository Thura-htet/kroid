import React, { useState, useEffect } from 'react';

import Post from '../components/post.compenent'

export function PostList(props)
{
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [posts, setPosts] = useState([]);

  // Note: the empty deps array [] means
  // this useEffect will run once
  // similar to componentDidMount()
  useEffect(() => {
    fetch("http://localhost:8000/api/posts")
      .then(res => res.json())
      .then(
        (result) => {
          setIsLoaded(true);
          setPosts(result);
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
  }, [])

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  } else {
      return (
        posts.map(
            (post, index) => <Post post={post} key={`${index}-{post.id}`} />
        )
      )
    }
}