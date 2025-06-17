import React from "react";

function MessageBubble(props) {
    let theme = props.theme
    return (
        <div
            className={`flex ${props.isSender ? "justify-end" : "justify-start"} w-full px-4 mb-4`}
        >
            <div
                className={`max-w-[75%] py-2 px-6 rounded-full shadow-sm text-sm
        ${props.isSender
                        ? "bg-[#ffcd74] text-white"
                        : `${theme ? 'text-white bg-gray-700' : 'bg-gray-200 text-gray-900'} `}`}
            >
                <p className="text-xl font-semibold">{props.text}</p>
                <span className={`block text-[10px] text-right
                    ${props.isSender
                        ? "bg-[#ffcd74] text-white"
                        : `${theme ? 'text-white ' : 'text-gray-900'} `} text-gray-300 mt-1`}>
                    {props.time}
                </span>
            </div>
        </div>
    );
}

export default MessageBubble;
