import React from 'react'

function NotificationItem(props) {
    const deleteNotif = (i)=>{
        // props.notifs.delete(i)
        console.log(props.notifs);
        
    }
    return (
        <>
            <div
                className='w-[95%] h-[10vh] rounded-xl px-4 bg-[#dedede] flex flex-row items-center justify-between gap-2'
            >
                <div className='flex flex-col items-start justify-center gap-2'>
                    <p className='text-wrap'>{props.content}</p>
                    <h1 className='text-sm font-semibold'>{props.time}</h1>
                </div>
                <div
                onClick={deleteNotif(props.pos)}
                    className='w-[8vw] aspect-square bg-[url(./src/assets/icons/delete.svg)] bg-no-repeat bg-center bg-cover'
                >

                </div>
            </div>

        </>
    )
}

export default NotificationItem