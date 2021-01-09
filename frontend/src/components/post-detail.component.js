import React from 'react';

import parse from 'html-react-parser';

export function FullArticle(props)
{
  const { post } = props;
  return (
      <div className='full-article'>
        <div className='jumbotron'>
          <h1 className='display-3'>{post.title}</h1>
          <h1 className='text-muted'>{post.summary}</h1>
          <a href={`/profile/${post.author_name}/`}><h3>@{post.author_name}</h3></a>
        </div>
        <div>
          {parse(`${post.html_content}`)}
        </div>
      </div>
  )
}