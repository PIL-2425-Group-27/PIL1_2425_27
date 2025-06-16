import Button from "../components/Button";

function PasswordChanged() {

    return (
        <>
            <div className="w-full h-screen bg-white flex flex-col items-center justify-center gap-[3vh] animate-fade md:bg-amber-300 lg:bg-green-300 font-manrope font-semibold">

                <div className="w-full h-fit flex flex-row items-center justify-center">
                    <h1 className="text-4xl ">Succès!</h1>
                </div>
                <div className="w-2/3 flex flex-row items-center justify-center">
                    <img
                        src="./src/assets/img/done.gif"
                        alt="" />
                </div>
                <div className="w-full h-fit flex flex-row items-center justify-center">
                    <h1 className="text-xl w-2/3 text-center text-gray-500">Mot de passe modifié avec succes.</h1>
                </div>
                <Button text={"Se connecter"} textCol={'text-white'} bg={'bg-[#ffcd74]'} submitted={true} link={'/Login'} />
            </div>
        </>
    );
}

export default PasswordChanged;