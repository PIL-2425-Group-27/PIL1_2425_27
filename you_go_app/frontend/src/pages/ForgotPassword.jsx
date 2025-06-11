import { useState } from "react";
import Button from "../components/Button";

function ForgotPassword() {
    const [visible, setvisible] = useState(false)
    return (
        <>
            <div className="w-full h-screen bg-white flex flex-col items-center justify-center gap-[4vh] animate-fade md:bg-amber-300 lg:bg-green-300 font-manrope font-semibold">

                <div className="flex flex-row items-start px-2.5 absolute top-12 left-3">
                    <a
                        className="flex flex-row text-sm font-bold"
                        href="/Login"><img
                            className="w-5 aspect-square"
                            src="./src/assets/icons/left-arrow.svg"
                            alt="return" />Retour
                    </a>
                </div>
                <div className="w-full h-fit pl-10 flex flex-row items-center justify-start">
                    <h1 className="text-3xl font-bold">Mot de passe oublié?</h1>
                </div>
                <div className="w-6/10 aspect-square">
                    <img
                        src="./src/assets/img/forgot-password.svg"
                        alt="" />
                </div>
                <i className="w-9/12 text-right text-sm border-l-2 border-[#ffcd74]">
                    Veuillez entrer votre adresse e-mail ou votre numero de telephone pour reçevoir un <span className="text-blue-400">Code de Vérification</span>
                </i>
                <form
                    className="w-full h-fit flex flex-col items-center gap-5 text-gray-500 [&_input]:focus:outline-0 [&_input]:w-full"
                    action=""
                    method="post"
                >
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 border-gray-200 focus-within:border-[#ffdb99]">
                        <input
                            className=""
                            placeholder="E-mail ou téléphone"
                            type="text"
                            name="contact"
                            id="contact"
                            required
                            autoComplete="true"
                        />
                    </div>
                    
                
                    <Button onClick={() => login()} text={"Suivant"} textCol={'text-white'} bg={'bg-[#ffcd74]'} type={'submit'} />
                </form>

            </div>
        </>
    );
}

export default ForgotPassword;