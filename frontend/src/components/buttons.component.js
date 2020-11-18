import React from 'react';

import axios from 'axios';

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '')
    {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++)
        {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) 
            {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
        return cookieValue;
    }
}
const csrftoken = getCookie('csrftoken');
const options = {
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
    },
    withCredentials: true 
};

export function SubmitPostButton(props)
{
    const { url, inputs } = props;

    function handleSubmit(e)
    {
        e.preventDefault();

        const data = JSON.stringify({
            'title': inputs.title.current.value,
            'summary': inputs.summary.current.value,
            'content': inputs.content.current.value,
        });

        axios.post(url, data, options)
        .then(response => {
            console.log(response);
            window.location.href = '/';
        })
        .catch(error => alert(error));
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
        const data = JSON.stringify({
            'parentId': parentId,
            'parentType': parentType,
            'comment': commentInput.current.value
        });
        
        axios.post(url, data, options)
        .then(response => console.log(response))
        .catch(error => alert(error));
        commentInput.current.value = ''
    }

    return (
        <button className='btn btn-primary' onClick={handleSubmit}>Submit</button>
    )
}