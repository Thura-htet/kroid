import React, { useRef, useState, useEffect } from 'react';

import axios from 'axios';

import { SubmitCommentButton } from './buttons.component';


function structureCommentTree(comments)
{
	const commentMap = {} // maps comment id to comment object
	comments.forEach(comment => {
		commentMap[comment.id] = comment
		comment['children'] = [];
	});
	comments.forEach(comment => {
		if (comment.parent !== null) // if comment is child
		{
			const parent = commentMap[comment.parent];
			parent.children.push(comment);
		}
	});
	// return the parent elements
	return comments.filter(comment => comment.parent === null);
}

function commentIsEmpty(comment) {
	return (comment != null && Object.keys(comment).length === 0 && comment.constructor === Object);
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

export function Comments(props)
{
	const { url } = props;
	const [newComment, setNewComment] = useState({});
	const [commented, setCommented] = useState(false);

	return (
		<>
			<CommentForm
				setNewComment={setNewComment}
				setCommented={setCommented}
				parentId={''}
				parentType={'post'} />
			<CommentTree
				commented={commented}
				setCommented={setCommented}
				newComment={newComment}
				url={url} />
		</>
	)
}

export function CommentForm(props)
{
	const { parentId, parentType, setNewComment, setCommented } = props;
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
				<textarea ref={commentInput} className='form-control' placeholder='What are your thoughts on this?'></textarea>
			</div>
			<SubmitCommentButton 
				url={comment_url}
				commentInput={commentInput}
				setReply={setReply}
				setReplied={setReplied}
				setNewComment={setNewComment}
				setCommented={setCommented} />
		</div>
	)
}

export function CommentTree(props)
{
	const { commented, setCommented, newComment, url } = props;
	const [isLoaded, setIsLoaded] = useState(false);
	const [loadedComments, setLoadedComments] = useState([]);
	const [updatedComment, setUpdatedComment] = useState(false);

	useEffect(() => {
		if (isLoaded === false)
		{
			axios.get(url, { withCredentials: true})
			.then(response => {
				setLoadedComments(response.data);
				setIsLoaded(true);
			})
			.catch(error => alert(`An error has occured: ${error}`));
		}
	}, [url, isLoaded, updatedComment, setIsLoaded, setLoadedComments]);

	useEffect(() => {
		if (!commentIsEmpty(newComment) && commented)
		{
			const final = [...loadedComments];
			final.unshift(newComment);
			setLoadedComments(final);
			setCommented(false);
		}
	}, [newComment, loadedComments, setLoadedComments, setUpdatedComment]);

	const commentTree = structureCommentTree(loadedComments);

	if (!isLoaded) {
		return <>Loading...</>
	}

	return (
		commentTree.map(
			(comment, index) => <Comment comment={comment} key={`${index}-${comment.id}`} />
		)
	)
}
