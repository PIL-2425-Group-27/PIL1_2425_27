import React from 'react'

function SearchBar(props) {
    return (
        <>
            <div className='absolute top-[10vh] flex flex-row items-center justify-center gap-4 w-full '>
                <input 
                className={`focus:outline-none w-[75%] h-11 rounded-4xl p-6 ${props.theme == false ? 'bg-gray-200' : 'bg-[#515151] text-white'}`}
                type="text"
                placeholder='Rechercher'
                 />
                 <button type="submit">
                    <img
                    className={`w-[8vw] ${props.theme == false ? '' : 'invert-100'}`}
                    src="./src/assets/icons/search2.svg" alt="" />
                 </button>
            </div>
        </>
    )
}

export default SearchBar