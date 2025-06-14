import Button from "../components/Button";
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
                <Title content={'Profil'} floating={true} />
                <div
                    className="w-full flex flex-col items-center"
                >
                    <Photo picture={'./src/assets/img/bg.jpg'} />
                    <Title content={fn + ' ' + ln} subContent={statut} />
                </div>
                <div
                    className="w-full flex flex-col items-center gap-1">
                    <h1>Votre profil n'est pas vérifié</h1>
                    <Button text={'Vérifier maintenant'} textCol={'text-white font-semibold'} bg={'bg-[#ffcd74]'} icon={'./src/assets/icons/verified.svg'}/>
                </div>
                <div className="w-full flex flex-col gap-4 py-8">
                    <Option icon={'./src/assets/icons/manage_accounts.svg'} content={'Modifier le profil'} link={'/ModifProfile'} />
                    <Option icon={'./src/assets/icons/edit.svg'} content={'Changer de mot de passe'} link={'/ChangePassword'} />
                    <Option icon={'./src/assets/icons/palette.svg'} content={'Themes'} />
                    <Option icon={'./src/assets/icons/hourglass.svg'} content={'Historique des trajets'} link={'/History'} />
                </div>
                <Button text={"Se deconnecter"} textCol={'text-white font-semibold'} bg={'bg-red-400'} icon={"./src/assets/icons/logout.svg"} submitted={true} link={'/login'} />
            </div>
        </>
    );
}

export default Profile;