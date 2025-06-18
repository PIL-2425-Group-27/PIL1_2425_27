import { useState, useEffect } from "react";
import Button from "../components/Button";
import Notification from "../components/Notification";
import Option from "../components/OptionItem";
import Photo from "../components/Photo";
import Return from "../components/Return";
import Title from "../components/Title";
import Toggle from "../components/Toggle";
import ValidatePopup from "../components/ValidatePopup";
import axios from "axios";
import Loading from "./Loading";


function Profile() {
    
    const [theme, setTheme] = useState(false)
    const [visible, setVisible] = useState(false)
    const [value, setValue] = useState(false)
    const [statut, setStatut] = useState('PASSAGER')
    const [loading, setLoading] = useState(true);
    const [firstName, setFirstName] = useState()
    const [lastName, setLastName] = useState()
    const [picture, setPicture] = useState('./src/assets/img/placeholderPicture.png')
    const token = localStorage.getItem("authToken")
    const [verified, setVerified] = useState(false)
    let fn = firstName
    let ln = lastName

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const res = await axios.get("http://localhost:8000/accounts/profile/", {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                console.log(res.data);
                
                setFirstName(res.data.first_name || res.data.username || "Utilisateur");
                setLastName(res.data.last_name || "");
                setStatut(res.data.role || "passager"); // adapt to your serializer
            } catch (error) {
                console.error("Failed to fetch user:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchUser();
    }, []);

    const toggle = () => {
        setTheme(!theme)
        send(theme)
    }
    const setIt = () => {
        setVisible(!visible)
    }
    useEffect(() => {
        console.log(`Est visible :${visible}`);
    }, [visible]);
    if (loading) {
        return <Loading />;
    }
    return (
        <>
            <div
                className={`w-full h-screen ${theme == false ? 'bg-white' : 'bg-[#2d2d2d] text-white'} flex flex-col items-center justify-evenly py-[12vh]`}
            >
                <Return theme={theme} />
                <Title content={'Profil'} floating={true} />
                <div
                    className='w-full flex flex-col items-center'
                >
                    <Photo picture={picture} />
                    <Title content={fn + ' ' + ln} subContent={statut} visible={verified} image={'./src/assets/icons/verified.svg'} />
                </div>
                <div
                    className={`w-full flex flex-col items-center gap-1 mt-3 ${verified ? 'hidden' : ''}`}>
                    <h1>Votre profil n'est pas vérifié</h1>
                    <Button text={'Vérifier maintenant'} textCol={'text-white font-semibold'} bg={'bg-[#ffcd74]'} icon={'./src/assets/icons/verified.svg'} link={'/KYC'} />
                </div>
                <div className="w-full flex flex-col gap-4 py-8">
                    <Option icon={'./src/assets/icons/manage_accounts.svg'} content={'Modifier le profil'} link={'/ModifProfile'} theme={theme} />
                    <Option icon={'./src/assets/icons/edit2.svg'} content={'Changer de mot de passe'} link={'/ChangePassword'} theme={theme} />
                    <Option icon={'./src/assets/icons/hourglass.svg'} content={'Historique des trajets'} link={'/History'} theme={theme} />
                    <Option icon={'./src/assets/icons/faq.svg'} content={'FAQ'} link={'/FAQ'} theme={theme} />
                    <Option icon={'./src/assets/icons/support.svg'} content={'Support Client'} link={'/Support'} theme={theme} />
                    <Toggle onclick={toggle} icon={theme ? './src/assets/icons/light.svg' : './src/assets/icons/dark.svg'} content={theme ? 'Thème clair' : 'Thème sombre'} theme={theme} />
                </div>
                <div className="w-full flex flex-col items-center justify-center gap-5 mb-10">
                    <Button text={"Se déconnecter"} textCol={'text-white font-semibold'} bg={'bg-red-400 active:bg-red-500 '} icon={"./src/assets/icons/logout.svg"} submitted={true} link={'/Login'} onClick={() => { localStorage.removeItem('authToken'); localStorage.setItem('active_status', false); console.log('get out'); }} />
                    <div className="w-full">
                        <Button text={"Supprimer le compte"} textCol={'text-red-400 font-semibold'} bg={'bg-white border-2 border-red-400 active:bg-gray-100 mb-10'} icon={"./src/assets/icons/deleteForever2.svg"} submitted={true} onClick={() => {
                            setIt();
                        }} />
                    </div>
                </div>
                <ValidatePopup warning={'Voulez-vous supprimer ce compte?\n Tapez votre mot de passe puis validez.'} visible={visible} setVisible={setVisible} />
            </div >
        </>
    );
}

export default Profile;