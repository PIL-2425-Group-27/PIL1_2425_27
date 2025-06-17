import Navbar from '../components/Navbar';
import Button from "../components/Button";
import { useState } from 'react';
function Landing() {
    const [anim, setanim] = useState('animate-ping')
    const [trans, setTrans] = useState()
    const [logo, setlogo] = useState('./logo.svg')
    setTimeout(() => {
        setanim('hidden')
        setTrans('-translate-y-[45vh] -translate-x-[40vw] scale-28')
    }, 3000);
    setTimeout(() => {
        setlogo('./logo-light.svg')
    }, 3200);

    // bg-[url(./src/assets/img/bg.jpg)]
    // bg-white
    return (
        <>
            <div
                className='relative w-full h-screen bg-white flex flex-col items-center justify-evenly'>
                <img
                    className={`z-10 w-2/6 absolute ${trans} transition-all duration-500`}
                    src={logo}
                    alt="" />
                <img
                    className={`w-2/8 ${anim} absolute opacity-60 animate-duration-2000`}
                    src="/logo.svg"
                    alt="" />
                <img
                    className={`w-2/9 ${anim} absolute opacity-60 animate-duration-2000`}
                    src="/logo.svg"
                    alt="" />
                <div className=' w-full h-screen flex flex-col items-center justify-center gap-6'>
                    <div className='w-full'>
                        <h1
                            className='w-full px-14 text-4xl text-gray-600 font-bold animate-fade-right animate-delay-3500'
                        >Bienvenue <span className='animate-fade animate-delay-200'>sur</span></h1>
                        <h1
                            className='w-full text-center my-2 text-[#ffcb74] text-4xl font-bold animate-fade-right animate-delay-3800'
                        >YouGo App</h1>
                    </div>

                    <img
                        className='max-w-lg w-[30vh] animate-fade animate-ease-in-out animate-delay-4000'
                        src="./src/assets/img/carpool.gif"
                        alt="Login" />
                    <h1 className='w-8/10 text-xl text-center font-semibold mx-auto animate-fade animate-delay-4000'>L'application de covoiturage pour Etudiants</h1>
                </div>
                <div className='w-full flex flex-col items-center animate-fade animate-delay-4200'>
                    <Button text={'Creer un compte'} textCol={'text-white'} bg={'bg-[#ffcb74]'} submitted={true} link={'/Register'} />
                    <p
                        className="my-5 text-gray-600">
                        Vous avez déjà un compte?
                        <a
                            href="/Login"
                            className="text-blue-400 mx-1">
                            Se connecter
                        </a>
                    </p>
                </div>
            </div>
        </>
    );
}

export default Landing;