import Button from "../components/Button";
import Navbar from "../components/Navbar";
import Option from "../components/OptionItem";
import Photo from "../components/Photo";
import Title from "../components/Title";

function Profile() {
    let fn = 'John'
    let ln = "DOE"
    let statut = 'Passager'
    return (
        <>
            <div
                className="w-full h-screen bg-white flex flex-col items-center justify-evenly py-10"
            >
                <Title content={'Profil'} floating={true}/>
                <div
                    className="w-full flex flex-col items-center"
                >
                    <Photo picture={'./src/assets/img/bg.jpg'} />
                    <Title content={fn + ' ' + ln} subContent={statut} />
                </div>
                <div className="w-full flex flex-col gap-4 py-8">
                    <Option icon={'./src/assets/icons/hide.svg'} content={'Modifier le profil'} link={'/'}/>
                    <Option icon={'./src/assets/icons/hide.svg'} content={'Yaa le profil'} link={'/'}/>
                    <Option icon={'./src/assets/icons/hide.svg'} content={'Get out le profil'} link={'/'}/>
                    <Option icon={'./src/assets/icons/hide.svg'} content={'Hehe le profil'} link={'/'}/>
                </div>
                <Button text={"Se deconnecter"} bg={'bg-red-300'} icon={"./src/assets/icons/logout.svg"} />
            </div>
        </>
    );
}

export default Profile;