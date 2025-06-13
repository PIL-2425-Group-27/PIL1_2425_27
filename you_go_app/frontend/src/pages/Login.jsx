import { useState } from "react";
import Button from "../components/Button";
import { useGoogleLogin } from '@react-oauth/google';
import axios from "axios"
import isValid from "../functions/entryCheck";

function Login() {
    const [border, setBorder] = useState('border-gray-200')
    const [visible, setvisible] = useState(false)

    // login handler function
    const login = useGoogleLogin({
        onSuccess: async (tokenResponse) => {
            try {
                const res = await axios.get(
                    "https://www.googleapis.com/oauth2/v3/userinfo",
                    {
                        headers: {
                            Authorization: `Bearer ${tokenResponse.access_token}`,
                        }
                    }
                );
                console.log(res.data.email);
            } catch (error) {
                console.log(error)
            }
        }
    });
    return (
        <>
            <div className="w-full h-screen bg-white flex flex-col items-center justify-evenly animate-fade md:bg-amber-300 lg:bg-green-300 font-manrope font-semibold">

                <div className="w-full h-fit pl-10 flex flex-row items-center justify-start">
                    <h1 className="text-4xl ">Connexion</h1>
                </div>
                <form
                    className="w-full h-fit flex flex-col items-center gap-3.5 text-gray-500 [&_input]:focus:outline-0 [&_input]:w-full"
                    action=""
                    method="post"
                >
                    <div className={`w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 ${border}`}>
                        <input
                            className=""
                            placeholder="E-mail ou téléphone"
                            type="text"
                            name="contact"
                            id="contact"
                            required
                            autoComplete="true"
                            onChange={(e) => {
                                setBorder(isValid(e.target.value)?'border-green-200':'border-red-200')
                            }}
                        />
                    </div>
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 border-gray-200 focus-within:border-[#ffdb99]">
                        <input
                            placeholder="Mot de passe"
                            type={visible ? 'text' : 'password'}
                            name="password"
                            id="password"
                            required
                            autoComplete="true"
                        />
                        <input
                            name="checkbox"
                            type="checkbox"
                            onClick={() => { setvisible(!visible) }}
                            className={`max-w-5 h-5 mx-2.5 appearance-none ${visible === true ? "bg-[url(./src/assets/icons/hide.svg)]" : "bg-[url(./src/assets/icons/unhide.svg)]"} bg-no-repeat bg-contain bg-center`}
                        />
                    </div>
                    <p className="w-9/12 text-right text-sm text-blue-400 mr-2">
                        <a href="/ForgotPassword">Mot de passe oublié</a>
                    </p>
                    <button
                        disabled
                        type="submit"
                        className="w-9/12 max-w-lg h-13 rounded-4xl text-xl text-white bg-[#ffdc74]"
                    >Se connecter
                    </button>
                    <p>ou</p>
                    <Button onClick={() => login()} text={"Continuer avec"} textCol={'text-gray-500'} bg={'bg-gray-100'} icon={'./src/assets/icons/google.svg'} />

                    <p
                        className="my-9">
                        Vous n'avez pas avez de compte?
                        <a
                            href="/Register"
                            className="text-blue-400 mx-1">
                            S'inscrire
                        </a>
                    </p>
                </form>

            </div>
        </>
    );
}

export default Login;