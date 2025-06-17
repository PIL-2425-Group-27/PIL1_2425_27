import React, { useEffect, useRef, useState } from 'react';
import { useParams } from 'react-router-dom';
import MessageBubble from '../components/MessageBubble';
import SendMessageBox from '../components/SendMessageBox';
import Return from './Return';

const Chatbox = () => {
    let theme = false
    const { chatId } = useParams();
    const [messages, setMessages] = useState([]);
    const messagesEndRef = useRef(null);

    // Scroll to bottom when messages update
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Simulate fetch chat messages by chatId (replace with real fetch)
    useEffect(() => {
        // Dummy data; replace with API call
        const chatHistory = [
            { id: 1, sender: 'user1', text: 'Hey there!', time: '10:00 AM' },
            { id: 2, sender: 'user2', text: 'Hello!', time: '10:01 AM' },
            { id: 3, sender: 'user1', text: 'How’s it going?', time: '10:02 AM' },
            { id: 4, sender: 'user2', text: "I'm fine tho", time: '10:02 AM' },
            { id: 5, sender: 'user2', text: 'BTW, why are u gay?', time: '10:02 AM' },
            { id: 6, sender: 'user1', text: 'What', time: '10:02 AM' },
            { id: 7, sender: 'user1', text: "Who says I'm gay?", time: '10:02 AM' },
            { id: 8, sender: 'user2', text: 'You are gay', time: '10:02 AM' },
        ];
        setMessages(chatHistory);
    }, [chatId]);

    const handleSend = (newMessage) => {
        setMessages((prev) => [...prev, {
            id: prev.length + 1,
            sender: 'user1',
            text: newMessage,
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }]);
    };

    return (
        <div className={`flex flex-col w-full h-screen ${theme ? 'bg-gray-900' : 'bg-white'} p-4${theme ? 'text-white' : 'text-gray-800'} `}>

            <div className="flex flex-row items-center justify-start px-4 py-4 border-b border-gray-400">
                <Return link={'/ChatList'} theme={theme}/>
                <img
                    src="../src/assets/img/prf3.jpeg"
                    alt="picture"
                    className='w-15 aspect-square rounded-full ml-8 ' 
                    />
                <h2 className="text-xl ml-3 font-semibold">Conversation #{chatId}</h2>
            </div>

            <div className="flex-1 overflow-y-auto px-4 py-2 space-y-3">
                {messages.map((msg) => (
                    <MessageBubble theme={theme} key={msg.id} isSender={msg.sender == 'user1'} text={msg.text} time={msg.time} />
                ))}
                <div ref={messagesEndRef} />
            </div>

            <div className="flex-none px-4 py-3 border-t-2 border-gray-400">
                <SendMessageBox onSend={handleSend} theme={theme}/>
            </div>
        </div>
    );
};

export default Chatbox