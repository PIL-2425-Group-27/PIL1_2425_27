import Button from "../components/Button";
import Navbar from "../components/Navbar";
import Photo from "../components/Photo";
import Title from "../components/Title";

function Profile() {
    let fn = 'John'
    let ln = "DOE"
    let statut = 'Passager'
    return (
        <>
            <div
                className="w-full h-screen bg-white flex flex-col items-center justify-evenly"
            >
                <Title content={'Profil'} />
                <div
                    className="w-full flex flex-col items-center"
                >
                    <Photo picture={'./src/assets/img/bg.jpg'} />
                    <Title content={fn + ' ' + ln} subContent={statut} />
                </div>
                <div
                    className="w-full bg-green-300"
                >

                </div>
                <Button text={"Se deconnecter"} bg={'bg-red-300'} icon={"./src/assets/icons/logout.svg"}/>
            </div>
        </>
    );
}

export default Profile;