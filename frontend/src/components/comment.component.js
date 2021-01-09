import React, { useRef, useState, useEffect } from 'react';

import axios from 'axios';

import { SubmitCommentButton } from './buttons.component';


export function CommentForm(props)
{
	const { parentId, parentType } = props;
	const [reply, setReply] = useState({});
	const [replied, setReplied] = useState(false);

	const path = window.location.pathname;
    const splits = path.split('/');
    // this log is run four times for some reason
    // not a good idea; replace with regex later on
    const slug = splits[splits.length-1] ? splits[splits.length-1] : splits[splits.length-2]
    const comment_url = `http://127.0.0.1:8000/api/post/${slug}/comments/`;
	
	const commentInput = useRef();

	if (replied)
	{
		return <Comment comment={reply} />
	}

	return (
		<div className='child-comment-form' data-parent-type={parentType} data-parent-id={parentId}>
			<div className='form-group'>
				<textarea ref={commentInput} className='form-control'></textarea>
			</div>
			<SubmitCommentButton 
				url={comment_url}
				commentInput={commentInput}
				setReply={setReply}
				setReplied={setReplied}
			/>
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
		setShowForm(!showForm);
	}

	return (
		<>
			<button className="btn btn-light btn-sm mb-1" onClick={handleClick}>Reply</button>
			{
				showForm?
				<CommentForm parentId={parentId} parentType={'comment'} />
				: <></>
			}
		</>
	)
}

export function Comment(props)
{
	const { comment } = props;
	const style = (comment.parent === null) ? {listStyleType: 'none', paddingLeft: '0px'} : {listStyleType: 'none'};
	const commentTree = (comment.children || []).map(
		(comment, index) => <Comment comment={comment} key={`${index}-${comment.id}`} />
	);
	return (
		<ul style={style}>
			<li>
				<p></p>
				<span className='text-muted'>@{comment.author_name}</span>
				<p>{comment.comment}</p>
				<ReplyComment parentId={comment.id} />
				{commentTree}
			</li>
		</ul>
	)
}

// const groupBy = (xs, key)  => xs.reduce(
// 	(rv, x) => {
// 		// push into the pre-existing array or create a new array and push into it
// 		(rv[x[key]] = rv[x[key]] || []).push(x);
// 		return rv;
// 	}, {}
// );

function structureCommentTree(comments)
{
	const commentMap = {} // maps comment id to comment object
	comments.forEach(comment => commentMap[comment.id] = comment);
	comments.forEach(comment => {
		if (comment.parent !== null)
		{
			const parent = commentMap[comment.parent];
			(parent.children = parent.children || []).push(comment)
		}
	});
	// return the parent elements
	return comments.filter(comment => comment.parent === null);
}

export function CommentTree(props)
{
	const { url } = props;
	const [isLoaded, setIsLoaded] = useState(false);
	const [comments, setComments] = useState([]);

	useEffect(() => {
		axios.get(url, { withCredentials: true})
		.then(response => {
			setIsLoaded(true);
			setComments(response.data);
		})
		.catch(error => alert(`An error has occured: ${error}`));
	}, [url]);

	if (!isLoaded) {
		return <>Loading...</>
	}

	const commentTree = structureCommentTree(comments);
	return (
		commentTree.map(
			(comment, index) => <Comment comment={comment} key={`${index}-${comment.id}`} />
		)
	)
}
