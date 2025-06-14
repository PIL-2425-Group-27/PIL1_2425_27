import { useState } from "react";
import Button from "../components/Button";
import Notification from "../components/Notification";
import Option from "../components/OptionItem";
import Photo from "../components/Photo";
import Return from "../components/Return";
import Title from "../components/Title";
import Toggle from "../components/Toggle";


function Profile() {
    let fn = 'John'
    let ln = "DOE"
    let statut = 'Passager'
    const [theme, setTheme] = useState(false)
    const verified = true
    const toggle = ()=>{
        setTheme(!theme)
    }
    return (
        <>
            <div
                className="w-full h-screen bg-white flex flex-col items-center justify-evenly py-10"
            >
                <Return />
                <Title content={'Profil'} floating={true} />
                <Notification floating={true} icon={'./src/assets/icons/notification.svg'} link={'/Notifications'} />
                <div
                    className='w-full flex flex-col items-center'
                >
                    <Photo picture={'./src/assets/img/bg.jpg'} />
                    <Title content={fn + ' ' + ln} subContent={statut} visible={verified} image={'./src/assets/icons/verified.svg'} />
                </div>
                <div
                    className={`w-full flex flex-col items-center gap-1 ${verified ? 'hidden' : ''}`}>
                    <h1>Votre profil n'est pas vérifié</h1>
                    <Button text={'Vérifier maintenant'} textCol={'text-white font-semibold'} bg={'bg-[#ffcd74]'} icon={'./src/assets/icons/verified.svg'} />
                </div>
                <div className="w-full flex flex-col gap-4 py-8">
                    <Option icon={'./src/assets/icons/manage_accounts.svg'} content={'Modifier le profil'} link={'/ModifProfile'} />
                    <Option icon={'./src/assets/icons/edit2.svg'} content={'Changer de mot de passe'} link={'/ChangePassword'} />
                    <Option icon={'./src/assets/icons/hourglass.svg'} content={'Historique des trajets'} link={'/History'} />
                    <Option icon={'./src/assets/icons/faq.svg'} content={'FAQ'} link={'/FAQ'} />
                    <Toggle onclick={toggle} icon={theme?'./src/assets/icons/light.svg':'./src/assets/icons/dark.svg'} content={theme ? 'Thème clair' : 'Thème sombre'} />
                </div>
                <Button text={"Se deconnecter"} textCol={'text-white font-semibold'} bg={'bg-red-400'} icon={"./src/assets/icons/logout.svg"} submitted={true} link={'/login'} />
            </div>
        </>
    );
}

export default Profile;