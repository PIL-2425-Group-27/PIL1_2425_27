import React from 'react'

function HistoryItem(props) {
    const deleteNotif = (i) => {
        // props.notifs.delete(i)
        console.log(props.notifs);

    }
    return (
        <>
            <div
                className={`w-[95%] py-4 rounded-xl px-4 ${props.theme == false ? 'bg-[#dedede]' : 'bg-[#1f1f1f] text-white'} flex flex-row items-center justify-start gap-3`}
            >
                <div
                    className={`w-[8vw] aspect-square bg-[url(./src/assets/icons/clock.svg)] ${props.theme == false ? '' : 'invert-100'} bg-no-repeat bg-center bg-cover`}
                >

                </div>
                <div key={props.label} className='flex flex-col items-start justify-center gap-2'>
                    <h2 className='text-lg font-semibold text-gray-700'>{props.label}</h2>
                    <p className='text-sm text-gray-600'>Kilomètres parcourus : <span className='font-medium'>{props.km} km</span></p>
                    <p className='text-sm text-gray-600'>Trajets effectués : <span className='font-medium'>{props.trajets}</span></p>
                    <p className='text-sm text-gray-600'>Avis donnés : <span className='font-medium'>{props.reviews}</span></p>
                </div>
            </div>

        </>
    )
}

export default HistoryItem