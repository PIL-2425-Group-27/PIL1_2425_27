import Button from "../components/Button";
import Option from "../components/OptionItem";
import Photo from "../components/Photo";
import Return from "../components/Return";
import Title from "../components/Title";

function History() {
    let fn = 'John'
    let ln = "DOE"
    let statut = 'Passager'
    return (
        <>
            <div
                className="w-full h-screen bg-white flex flex-col items-center justify-center gap-[2vh] py-10"
            >
                <Return link={'/Profile'}/>
                <Title content={'Historique des trajets'} floating={false}/>
                <div className="w-full flex flex-col gap-4 py-8">
                    <Option icon={'./src/assets/icons/hide.svg'} content={'Modifier le profil'} link={'/ModifProfile'}/>
                    <Option icon={'./src/assets/icons/hide.svg'} content={'Changer de mot de passe'} link={'/ChangePassword'}/>
                    <Option icon={'./src/assets/icons/hide.svg'} content={'Themes'}/>
                    <Option icon={'./src/assets/icons/hide.svg'} content={'Historique des trajets'} link={'/History'}/>
                </div>
                <Button text={"Se deconnecter"} bg={'bg-red-400'} icon={"./src/assets/icons/logout.svg"} submitted={true} link={'/login'}/>
            </div>
        </>
    );
}

export default History;