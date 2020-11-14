import React, { useRef } from 'react';

import { SubmitCommentButton } from './buttons.component'

export function ReplyComment(props)
{
	const commentInput = useRef();

	function showCommentForm(e)
	{
		const commentElement = e.target.parentElement;
		const parentId = commentElement.dataset.parentId;
		const comment_url = `http://localhost:8000/api/post/${slug}/comments/`
		
		// use React.createElement
		return (
			<div className='child-comment' data-parent-type='comment' data-parent-id={parentId}>
				<div className='form-group'>
					<textarea ref={commentInput} className='form-control'></textarea>
			  </div>
			  <SubmitCommentButton url={comment_url} commentInput={commentInput} />
			</div>
		)
	}

	return (
		<button className='btn btn-primary' onClick={showCommentForm}>Reply</button>
	)
}