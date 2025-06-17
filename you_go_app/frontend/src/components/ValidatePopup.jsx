import React, { useState } from 'react'
import Button from './Button'

function ValidatePopup(props) {
  
  const [pvisible, setpvisible] = useState(false)
  return (
    <div className={`absolute w-full h-full bg-[#2d2d2d46] py-5 flex-col items-center justify-center ${props.visible? 'flex':'hidden'}`}>
      <div className='w-[95%]  rounded-2xl bg-white flex flex-col items-center justify-center p-4 gap-4'>
        <img
          className='w-10'
          src="./src/assets/icons/warning.svg"
          alt="Warning Icon" />
        <h1 className='w-9/10 py-3 font-semibold'>{props.warning}</h1>
        <div className="w-9/10 max-w-lg h-13 bg-gray-300 rounded-md flex flex-row items-center justify-between px-4 [&_input]:focus:outline-0 [&_input]:w-full">
                        <input
                            placeholder="Mot de passe"
                            type={pvisible ? 'text' : 'password'}
                            name="password"
                            id="password"
                            required
                            autoComplete="true"
                            onChange={(e) => {
                                setPassword(e.target.value)
                            }}
                        />
                        <input
                            name="checkbox"
                            type="checkbox"
                            onClick={() => { setpvisible(!pvisible) }}
                            className={`max-w-5 h-5 mx-2.5 appearance-none ${pvisible === true ? "bg-[url(./src/assets/icons/hide.svg)]" : "bg-[url(./src/assets/icons/unhide.svg)]"} bg-no-repeat bg-contain bg-center invert-100`}
                        />
                    </div>
        <Button text={'Supprimer'} textCol={'text-2xl font-semibold text-white'} bg={'bg-red-400'} link={'/'}/>
        <Button text={'Annuler'} textCol={'text-2xl font-semibold text-[#202020]'} bg={'bg-white border-2 border-gray-400'} onClick={()=>props.setVisible(false)}/>
      </div>
    </div>
  )
}

export default ValidatePopup