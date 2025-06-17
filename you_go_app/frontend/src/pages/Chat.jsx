import React from 'react'
import ChatMenu from '../components/ChatList'
import Chatbox from '../components/Chatbox'

function Chat() {
    return (
        <>
            <div
                className='w-full h-screen bg-white relative'
            >
              <ChatMenu/>  

            </div>
        </>
    )
}

export default Chat