import React, { useRef } from 'react';

import { SubmitPostButton } from '../components/buttons.component';

export function Write(props)
{
    const titleInput = useRef(),
          summaryInput = useRef(),
          contentInput = useRef();
    const url = 'http://localhost:8000/api/posts/'

    return (
        <>
            <div className='form-group'>
                <input ref={titleInput} className='form-control' type='text'
                    name='title' placeholder='Enter Title' autoComplete='off'/>
            </div>
            <div className='form-group'>
                <input ref={summaryInput} className='form-control' type='text'
                    name='summary' placeholder='Enter Summary' autoComplete='off'/>
            </div>
            <div className='form-group'>
                <textarea ref={contentInput} className='form-control' name='content'
                    placeholder='Enter Content' autoComplete='off'>
                </textarea>
            </div>
            <SubmitPostButton url={url} inputs={{
                title: titleInput,
                summary: summaryInput,
                content: contentInput
            }} />
        </>
    )
}