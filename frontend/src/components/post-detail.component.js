import React from 'react';

import parse from 'html-react-parser';

export function FullArticle(props)
{
  const { post } = props;
  return (
    <div className='full-article'>
      <h2>{post.title}</h2>
      <h5>{post.summary}</h5>
      <div>
        {parse(`${post.html_content}`)}
      </div>
    </div>
  )
}