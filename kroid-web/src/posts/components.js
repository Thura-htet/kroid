import React, { useState, useEffect } from 'react';

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
      return posts.map(
            (post, index) => <Post post={post} key={`${index}-{post.id}`} />
      )
    }
}

export function ActionButton(props)
{
  const {post, action} = props
  return (
    action.type === 'save' ? <button>Save</button> : null
  )
}

export function Post(props)
{
  const { post } = props;
  const className = props.className ? props.className : 'col-10 mx-auto column-md-6';
  return (
    <div className={className}>
      <p>{post.id} - { post.title }</p>
      <div>
        <ActionButton post={post} action={{type: 'save'}} />
      </div>
    </div>
  )
}