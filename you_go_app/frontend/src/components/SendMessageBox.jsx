// src/components/SendMessageBox.jsx
import React, { useState } from "react";

function SendMessageBox(props) {
    const [message, setMessage] = useState("");

    const handleSend = (e) => {
        e.preventDefault();
        if (message.trim() !== "") {
            props.onSend(message.trim());
            setMessage("");
        }
    };

    return (
        <form
            onSubmit={handleSend}
            className={`w-full px-4 flex items-center gap-2 ${props.theme ? 'bg-gray-800' : 'bg-white'} `}
        >
            <input
                type="text"
                className={`flex-1 rounded-full px-4 py-2 ${props.theme} focus:outline-none`}
                placeholder="Écrivez un message..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
            />
            <button
                type="submit"
                className="flex flex-col items-center justify-center w-14 aspect-square bg-[#ffcd74] hover:bg-[#f4b74f] text-white font-semibold rounded-full transition-colors duration-200 disabled:opacity-60"
                disabled={message.trim() === ""}
            >
                <img
                    src="../src/assets/icons/send.svg"
                    alt="Send" 
                    className="invert-100 w-2/3"/>
            </button>
        </form>
    );
}

export default SendMessageBox;
