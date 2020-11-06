import React, { useState, useEffect } from 'react';

import Post from '../components/post.compenent';
import { getData } from '../actions/http.helpers';

export function PostList(props)
{
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [posts, setPosts] = useState([]);
  const url = "http://localhost:8000/api/posts/";

  useEffect(() => {
    getData(url)
    .then(response => {
      setIsLoaded(response.isLoaded);
      setError(response.error);
      setPosts(response.data);
    });
  }, [url])

  if (error) {
    return <div>Error: {error}</div>; // changed from {error.message}
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