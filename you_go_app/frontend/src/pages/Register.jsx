import { useState,useMemo } from "react";
import { useGoogleLogin } from '@react-oauth/google';
import axios from "axios"
import Button from "../components/Button";
import isValid from "../functions/entryCheck";

function Register() {
    const [border, setBorder] = useState('border-gray-200')
    const [visible1, setvisible1] = useState(false)
    const [visible2, setvisible2] = useState(false)
    const [confpwd, setConfpwd] = useState('');
    const [password, setPassword] = useState('');
    const [fir_name, setFir_name] = useState('');
    const [las_name, setLas_name] = useState('');
    const [email, setEmail] = useState('');
    const [phone, setPhone] = useState('');
    const [value, setValue] = useState('');
    const [submitted, setSubmitted] = useState(false);
    // Handle google registration
    const register = useGoogleLogin({
        onSuccess: async (tokenResponse) => {
            try {
                const res = await axios.get(
                    "https://www.googleapis.com/oauth2/v3/userinfo",
                    {
                        headers: {
                            Authorization: `Bearer ${tokenResponse.access_token}`,
                        },
                    }
                );
                console.log(res.data);
            } catch (error) {
                console.log(error)
            }
        }
    });
    const checkValidity = useMemo(() => {
        return fir_name.trim() !=='' && las_name.trim() !=='' && password.trim() !== '' && confpwd.trim() !=='' && email.trim() !=='' && phone.trim() !=='';
    }, [fir_name,las_name,password,confpwd,email,phone]);
    
    // Handle login by email
    const send = (e) => {
        e.preventDefault();
        fetch(
            'https://jsonplaceholder.typicode.com/todos',
            {
                method: 'POST',
                body: JSON.stringify({
                    value,
                    completed: false
                })
            }
        )
            .then(response => response.json())
            .then(() => console.log("Submitted successfully"))
            .then(() => setSubmitted(prev => { const newVal = !prev; return newVal }))
            .then(json => console.log(submitted))
            .catch(e => {
                console.log("failed:"+e)
            })
    }

    return (
        <>
            <div className="w-full h-screen bg-white flex flex-col items-center justify-center animate-fade md:bg-amber-300 lg:bg-green-300 font-manrope font-semibold">

                <div className="w-full h-[10em] px-10 flex flex-row items-center justify-start">
                    <h1 className="text-4xl ">Inscription</h1>
                </div>
                <form
                    className="w-full h-fit flex flex-col items-center pt-[2vh] gap-[1vh] text-gray-500 [&_input]:focus:outline-0 [&_input]:w-full"
                    action=""
                    onSubmit={send}
                >
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 border-gray-200 focus-within:border-[#ffdb99]">
                        <input
                            placeholder="Prenom"
                            type="text"
                            name="fist_name"
                            id="firstname"
                            autoComplete="true"
                            onChange={setFir_name}
                        />
                    </div>
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 border-gray-200 focus-within:border-[#ffdb99]">
                        <input
                            placeholder="Nom"
                            type="text"
                            name="last_name"
                            id="lastname"
                            required
                            autoComplete="true"
                            onChange={setLas_name}

                        />
                    </div>
                    <div className={`w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 ${border}`}>
                        <input
                            className=""
                            placeholder="E-mail"
                            type="e-mail"
                            name="email"
                            id="email"
                            required
                            autoComplete="true"
                            onChange={(e) => {
                                setBorder(isValid(e.target.value) ? 'border-green-200' : 'border-red-200');
                                setEmail
                            }}
                        />
                    </div>
                    <div className={`w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 ${border}`}>
                        <input
                            className=""
                            placeholder="Numero de telephone"
                            type="number"
                            name="phone_number"
                            id="phone"
                            required
                            autoComplete="true"
                            onChange={(e) => {
                                setBorder(isValid(e.target.value) ? 'border-green-200' : 'border-red-200');
                                setPhone
                            }}
                        />
                    </div>
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 border-gray-200">
                        <input
                            placeholder="Mot de passe"
                            type={visible1 ? 'text' : 'password'}
                            name="password"
                            id="password"
                            required
                            autoComplete="true"
                            onChange={setPassword}
                        />
                        <input
                            name="checkbox"
                            type="checkbox"
                            onClick={() => { setvisible1(!visible1) }}
                            className={`max-w-5 h-5 mx-2.5 appearance-none ${visible1 === true ? "bg-[url(./src/assets/icons/hide.svg)]" : "bg-[url(./src/assets/icons/unhide.svg)]"} bg-no-repeat bg-contain bg-center`}
                        />
                    </div>
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 border-gray-200 focus-within:border-[#ffdb99]">
                        <input
                            placeholder="Confirmer le mot de passe"
                            type={visible2 ? 'text' : 'password'}
                            name="confirmpwd"
                            id="confirmpwd"
                            required
                            autoComplete="true"
                            onChange={setConfpwd}

                        />
                        <input
                            name="checkbox"
                            type="checkbox"
                            onClick={() => { setvisible2(!visible2) }}
                            className={`max-w-5 h-5 mx-2.5 appearance-none ${visible2 === true ? "bg-[url(./src/assets/icons/hide.svg)]" : "bg-[url(./src/assets/icons/unhide.svg)]"} bg-no-repeat bg-contain bg-center`}
                        />
                    </div>
                    <button
                        disabled={!checkValidity}
                        type="submit"
                        className="w-9/12 max-w-lg h-13 rounded-4xl text-xl text-white bg-[#ffcd74]"
                    >S'inscrire
                    </button>
                    <p>ou</p>
                    <Button onClick={() => register()} text={"Continuer avec"} textCol={'text-gray-500'} bg={'bg-gray-100'} icon={'./src/assets/icons/google.svg'} />
                    <p
                        className="my-9">
                        Vous avez déjà un compte?
                        <a
                            href="/Login"
                            className="text-blue-400 mx-1">
                            Se connecter
                        </a>
                    </p>
                </form>

            </div>
        </>
    );
}

export default Register;