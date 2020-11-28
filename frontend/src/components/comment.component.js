import React, { useRef, useState } from 'react';

import { SubmitCommentButton } from './buttons.component';


export function CommentForm(props)
{
	const { parentId, parentType } = props;

	const path = window.location.pathname;
    const splits = path.split('/');
    // this log is run four times for some reason
    // not a good idea; replace with regex later on
    const slug = splits[splits.length-1] ? splits[splits.length-1] : splits[splits.length-2]
    const comment_url = `http://127.0.0.1:8000/api/post/${slug}/comments/`;
	
	const commentInput = useRef();

	return (
		<div className='child-comment-form' data-parent-type={parentType} data-parent-id={parentId}>
			<div className='form-group'>
				<textarea ref={commentInput} className='form-control'></textarea>
			</div>
			<SubmitCommentButton url={comment_url} commentInput={commentInput} />
		</div>
	)
}

export function ReplyComment(props)
{
	const { parentId } = props;
	const [showForm, setShowForm] = useState(false);

	function handleClick(e)
	{
		e.preventDefault();
		setShowForm(true);
	}

	if (showForm) {
		return <CommentForm parentId={parentId} parentType={'comment'} />
	}
	return (
		<button className="btn btn-primary btn-sm" onClick={handleClick}>Reply</button>
	)
}