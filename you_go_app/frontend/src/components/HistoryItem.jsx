import React from 'react'

function HistoryItem(props) {
    const deleteNotif = (i) => {
        // props.notifs.delete(i)
        console.log(props.notifs);

    }
    return (
        <>
            <div
                className={`w-[95%] h-[10vh] rounded-xl px-4 ${props.theme==false?'bg-[#dedede]':'bg-[#1f1f1f] text-white'} flex flex-row items-center justify-start gap-3`}
            >
                <div
                    className={`w-[8vw] aspect-square bg-[url(./src/assets/icons/clock.svg)] ${props.theme==false?'':'invert-100'} bg-no-repeat bg-center bg-cover`}
                >

                </div>
                <div className='flex flex-col items-start justify-center gap-2'>
                    <p className='text-wrap'>{props.content}</p>
                    <h1 className='text-sm font-semibold'>{props.duration}</h1>
                </div>
            </div>

        </>
    )
}

export default HistoryItem