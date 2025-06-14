import React from 'react'
import ChatContact from './ChatContact'

function ChatMenu() {
    let contacts = [
        {
            id : 1,
            profile:{
                full_name: 'Raven sink',
                image: './src/assets/img/bg.jpg',
                message: 'bruh 😒',
            }
        },
        {
            id : 2,
            profile:{
                full_name :'Loic Sen',
                image: './src/assets/img/bg.jpg',
                message : 'hello..',
            }
        },
        {
            id :3, 
            profile:{
                full_name :'Hailey Knot',
                image:'./src/assets/img/prf3.jpeg',
                message : 'How are u today btch',
            }
        },
        {
            id :4 ,
            profile:{
                full_name :'Lana Enders',
                image:'./src/assets/img/prf4.jpg',
                message: 'Get out',
            }
        },
        {
            id :5 ,
            profile:{
                full_name :'Raven Enders',
                image:'./src/assets/img/prf4.jpg',
                message: 'Get out',
            }
        },
        {
            id :6 ,
            profile:{
                full_name :'Kent Letho',
                image:'./src/assets/img/prf4.jpg',
                message: 'Get out',
            }
        },
    ]
    return (
        <div
            className={`absolute w-full h-screen `}>
            <div
                className='w-full py-[2vh]'
            >
                <h1 className='text-4xl font-bold pl-[4vw] pt-[5vh]'>Messages</h1>
                <div className='w-full h-full pt-[6vh] flex flex-col gap-[1vh] items-center justify-start'>
                    {contacts.map((message)=>
                    <ChatContact full_name={message.profile.full_name} small={message.profile.message} image = {`bg-[url(`+message.profile.image+`)]`} key={message.id}/>
                    )}
                    <div
                        title='Nouveau chat'
                        className='flex flex-row items-center justify-center text-2xl w-[18%] aspect-square bg-[#ffcd74] rounded-full absolute bottom-[4vh] right-[5vw]'
                    >
                        <img
                            className='w-3/5'
                            src="./src/assets/icons/chat.svg"
                            alt="New Chat" />
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ChatMenu