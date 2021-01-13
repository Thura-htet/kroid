import React, { useState, useEffect } from 'react';

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
        'X-Requested-With': 'XMLHttpRequest',
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
        .catch(error => {
            if (error.response.status === 401) 
            {
                if (error.response.statusText === 'Unauthorized')
                {
                    window.location.href = '/login';
                };
            };
        });
    };

    return (
        <button className='btn btn-primary' onClick={handleSubmit}>Submit</button>
    )
}

export function SubmitCommentButton(props)
{
    const { url, commentInput, setReply, setReplied, setNewComment, setCommented } = props;

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
        .then(response => {
            const comment = response.data;
            const status = response.status;
            if (status === 200)
            {
                if (comment.parent !== null)
                {
                    setReplied(true);
                    setReply(comment);
                }
                else
                {
                    setCommented(true);
                    setNewComment(comment);
                    commentInput.current.value = '';
                }
            }
        })
        .catch(error => console.log(error));
    }

    return (
        <button className='btn btn-primary' onClick={handleSubmit}>Submit</button>
    )
}

export function SubmitAboutButton(props)
{
    const { url, aboutInputs } = props;

    function handleSubmit(e)
    {
        e.preventDefault();

        const data = JSON.stringify({
            'pen_name': aboutInputs.pen_name.current.value,
            'bio': aboutInputs.bio.current.value,
            'fav_quote': aboutInputs.fav_quote.current.value
        });
        axios.put(url, data, options)
        .then(response => {
            console.log(response);
            window.location.reload();
        })
        .catch(error => alert(`An error has occurred ${error}`));
    }

    return (
        <button className='btn btn-primary' onClick={handleSubmit}>Submit</button>
    )
}

export function FollowButton(props)
{
    const { url, is_following } = props;
    const [following, setFollowing] = useState()
    const [display, setDisplay] = useState('');
    const [action, setAction] = useState('');


    useEffect(() => setFollowing(is_following), [is_following]);

    useEffect(() => {
        if (following)
        {
            setDisplay('Following');
            setAction('unfollow');
        }
        else
        {
            setDisplay('Follow');
            setAction('follow');
        }
    }, [following]);

    function handleClick(e)
    {
        e.preventDefault();
        axios.post(url, {'action': action}, options)
        .then(response => {
            console.log(response);
            setFollowing(!following);
        })
        .catch(error => alert(`An error has occurred ${error}`));
    }

    return <button className='btn btn-outline-secondary' onClick={handleClick}>{display}</button>
}