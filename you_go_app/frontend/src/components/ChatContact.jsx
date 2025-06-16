import React from 'react'

function ChatContact(props) {
    return (
        <div className='w-full flex flex-row items-center justify-between px-[4vw] py-[1vh] gap-5'>
            <div className='flex flex-row gap-3' >
                <div className={`w-[14vw] aspect-square ${props.image} bg-cover bg-center rounded-full`}>
                </div>
                <div>
                    <h1 className='text-2xl font-semibold'>{props.full_name}</h1>
                    <p>{props.small}</p>
                </div>
            </div>
            <div>
                <h1>{props.time}</h1>
            </div>
        </div>
    )
}

export default ChatContact