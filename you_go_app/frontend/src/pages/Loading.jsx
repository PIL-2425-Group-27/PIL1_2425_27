
import { useState } from 'react';
function Loading() {


    return (
        <>
            <div
                className='relative w-full h-screen bg-white flex flex-col items-center justify-evenly'>
                <img
                    className={`z-10 w-2/6 absolute transition-all duration-500`}
                    src='/logo.svg'
                    alt="" />
                <img
                    className={`w-2/8 absolute animate-ping opacity-60 animate-duration-2000 animate-infinite`}
                    src="/logo.svg"
                    alt="" />
                <img
                    className={`w-2/9 absolute animate-ping opacity-60 animate-duration-2000 animate-infinite`}
                    src="/logo.svg"
                    alt="" />
            </div>
        </>
    );
}

export default Loading;