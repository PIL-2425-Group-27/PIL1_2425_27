import React from 'react'
import ChatMenu from '../components/ChatMenu'
import Chatbox from '../components/Chatbox'

function Chat() {
    return (
        <>
            <div
                className='w-full h-screen bg-white relative'
            >
              <ChatMenu/>  
              <Chatbox/>  

            </div>
        </>
    )
}

export default Chat