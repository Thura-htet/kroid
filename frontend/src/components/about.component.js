import React, { useState, useRef } from 'react';

import { SubmitAboutButton } from './buttons.component';


export function AboutForm(props)
{
    const { pen_name, bio, fav_quote } = props;

    const path = window.location.pathname;
    const splits = path.split('/');
    // this log is run four times for some reason
    // replace with regex later on
    const username = splits[splits.length-1] ? splits[splits.length-1] : splits[splits.length-2];
    const url = `http://127.0.0.1:8000/api/profile/${username}/`;

    const nameInput = useRef();
    const bioInput = useRef();
    const favInput = useRef();

    return (
        <>
            <div className='form-group'>
                <input type='text' ref={nameInput} className='form-control' defaultValue={pen_name} />
            </div>
            <div className='form-group'>
                <input type='text' ref={bioInput} className='form-control' defaultValue={bio} />
            </div>
            <div className='form-group'>
                <input type='text' ref={favInput} className='form-control' defaultValue={fav_quote} />
            </div>
            <SubmitAboutButton url={url} aboutInputs={{
                'pen_name': nameInput,
                'bio': bioInput,
                'fav_quote': favInput
            }} />
        </>
    )
}


export function AboutComponent(props)
{
    const { about } = props;
    const [showForm, setShowForm] = useState(false);
    
    function handleClick(e)
    {
        e.preventDefault();
        setShowForm(true)
    }

    const editButton = about.editable ? <button className="btn btn-primary btn-sm" 
        onClick={handleClick}>Edit</button> : null;
    
    if (showForm) {
        return <AboutForm pen_name={about.pen_name} bio={about.bio} fav_quote={about.fav_quote} />
    }

    return (
        <div className='jumbotron px-2 py-1 bg-white'>
            <h1 className='display-4'>{about.pen_name}</h1>
            <h5>@{about.username}</h5>
            <p className='lead'>{about.bio}</p>
            <p><em>{about.fav_quote}</em></p>
            {editButton}
            <hr />
        </div>
    );
}    