import React from 'react'
import ChatContact from './ChatContact'
import Return from './Return'
import { Link } from 'react-router-dom';

function ChatList() {
    let theme = false
    const mockChats = [
        {
            id: 1,
            name: 'Raven Sink',
            lastMessage: 'bruh 😒',
            timestamp: '10:45 AM',
            avatar: './src/assets/img/prf4.jpg',
        },
        {
            id: 2,
            name: 'Loic Sen',
            lastMessage: 'hello..',
            timestamp: '09:30 AM',
            avatar: './src/assets/img/bg.jpg',
        },
        {
            id: 3,
            name: 'Hailey Knot',
            lastMessage: 'How are u today btch',
            timestamp: 'Yesterday',
            avatar: './src/assets/img/prf3.jpeg',
        },
    ];
    return (
        <div className={`w-full h-screen ${theme ? 'bg-gray-900' : 'bg-white'} p-4${theme ? 'text-white' : 'text-gray-800'} `}>

            <Return theme={theme} />
            <h1 className='text-4xl font-bold pl-[8vw] pt-[10vh] pb-[5vh]'>Messages</h1>
            <ul className="flex flex-col px-8 ">
                {mockChats.map((chat) => (
                    <li key={chat.id} className="flex items-center justify-between border-b border-gray-200 py-5">
                        <Link to={`/Chat/${chat.id}`} className="flex items-center space-x-3 w-full">
                            <img
                                src={chat.avatar}
                                alt={chat.name}
                                className="w-15 h-15 rounded-full object-cover"
                            />
                            <div className="flex-1">
                                <h1 className="font-bold text-xl">{chat.name}</h1>
                                <p className="text-2sm text-gray-500 dark:text-gray-400 truncate">{chat.lastMessage}</p>
                            </div>
                            <span className="text-xs text-gray-400">{chat.timestamp}</span>
                        </Link>
                    </li>
                ))}
            </ul>
            <Link to={'/SearchChat'}>
                <div
                    title='Nouveau chat'
                    className='flex flex-row items-center justify-center text-2xl w-[18%] aspect-square bg-[#ffcd74] rounded-full absolute bottom-[4vh] right-[5vw] shadow-lg shadow-gray-300'
                >
                    <img
                        className='w-3/5 '
                        src="./src/assets/icons/chat.svg"
                        alt="New Chat" />
                </div>
            </Link>
        </div>
    )
}

export default ChatList