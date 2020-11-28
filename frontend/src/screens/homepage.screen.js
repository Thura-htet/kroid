import React, { useState, useEffect } from 'react';

import axios from 'axios';

import { PostList} from '../components/post.compenent';

export function HomePage(props)
{
  const [isLoaded, setIsLoaded] = useState(false);
  const [posts, setPosts] = useState([]);
  const url = "http://127.0.0.1:8000/api/posts/";

  useEffect(() => {
    axios.get(url, { withCredentials: true })
    .then(response => {
      setIsLoaded(true);
      setPosts(response.data);
    })
    .catch(error => alert(`An error has occured: ${error}`));
  }, [url]);

  if (!isLoaded) {
    return <>Loading...</>
  }
  else {
    return (
      <PostList postList={posts} />
    )
  }
}