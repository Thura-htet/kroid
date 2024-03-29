import React, { useState, useEffect } from 'react';


export function ActionButton(props)
{
  const {post, action} = props
  if (action.type === 'save')
  {
    return (
      <svg width="1em" height="1em" viewBox="0 0 16 16" className="bi bi-bookmark-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
        <path fillRule="evenodd" d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.74.439L8 13.069l-5.26 2.87A.5.5 0 0 1 2 15.5V2z"/>
      </svg>
    )
  }
  else
  {
    return (
      <svg width="1em" height="1em" viewBox="0 0 16 16" className="bi bi-bookmark-check-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
        <path fillRule="evenodd" d="M4 0a2 2 0 0 0-2 2v13.5a.5.5 0 0 0 .74.439L8 13.069l5.26 2.87A.5.5 0 0 0 14 15.5V2a2 2 0 0 0-2-2H4zm6.854 5.854a.5.5 0 0 0-.708-.708L7.5 7.793 6.354 6.646a.5.5 0 1 0-.708.708l1.5 1.5a.5.5 0 0 0 .708 0l3-3z"/>
      </svg>
    )
  }
}

export function Post(props)
{
  const { post } = props;
  const className = props.className ? props.className : 'media';
  const postURL = `/post/${post.slug}/`
  return (
    <>
      <div className={className}>
        <div className='media-body'>
            <h4 className='mt-0'><a href={postURL}>{post.title}</a></h4>
            <h5>{post.summary}</h5>
            <a href={`/profile/${post.author_name}`}><h6>@{post.author_name}</h6></a>
            <hr/>
        </div>
        <div>
            <ActionButton post={post} action={{type: 'save'}} />
        </div>
      </div>
    </>
  )
}

export function PostList(props)
{
  const { postList } = props;
  return (
    postList.map(
        (post, index) => <Post post={post} key={`${index}-${post.id}`} />
    ));
}