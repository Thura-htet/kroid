import React from 'react';
import { postData } from '../actions/http.helpers';

export function SubmitPostButton(props)
{
    const { url, inputs } = props;

    function handleSubmit(e)
    {
        e.preventDefault();
        const data = {
            'title': inputs.title.current.value,
            'summary': inputs.summary.current.value,
            'content': inputs.content.current.value,
        }
        postData(url, data)
        .then(response => {
            if (response.error) {
                alert(response.error);
            }
        });
    }

    return (
        <button className='btn btn-primary' onClick={handleSubmit}>Submit</button>
    )
}

export function SubmitCommentButton(props)
{
    const { url, commentInput } = props;

    function handleSubmit(e)
    {
        e.preventDefault();

        const commentElement = e.target.parentElement;
        const parentId = '' ? null : Number(commentElement.dataset.parentId);
        const parentType = commentElement.dataset.parentType;
        const data = {
            'parentId': parentId,
            'parentType': parentType,
            'comment': commentInput.current.value
        }
        
        postData(url, data)
        .then(response => {
            if (response.error) {
                alert(response.error);
            }
        });
        commentInput.current.value = ''
    }

    return (
        <button className='btn btn-primary' onClick={handleSubmit}>Submit</button>
    )
}