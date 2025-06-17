import { useState, useMemo, useRef, useEffect } from "react";
import { useGoogleLogin } from '@react-oauth/google';
import axios from "axios"
import Button from "../components/Button";
import isValid from "../functions/entryCheck";
import { useNavigate } from "react-router-dom";
import passwordSame from "../functions/passwordSame";

function Register() {
    const [border1, setBorder1] = useState('border-gray-200')
    const [border2, setBorder2] = useState('border-gray-200')
    const [border3, setBorder3] = useState('border-gray-200')
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
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate()

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
                setSubmitted(true);
                console.log(res.data);
            } catch (error) {
                console.log(error)
            }
        }
    });
    const checkValidity = useMemo(() => {
        return (fir_name.trim() !== '' && las_name.trim() !== '' && password.trim() !== '' && confpwd.trim() !== '' && email.trim() !== '' && phone.trim() !== '' && (password == confpwd));
    }, [fir_name, las_name, password, confpwd, email, phone]);

    // Handle login by email
    useEffect(() => {
        if (submitted) {
            navigate('/RoleChoice');
        }
    }, [submitted, navigate]);



    const send = (e) => {
        e.preventDefault();
        setLoading(true); // start loading

        axios.post('', {
            value,
            completed: false
        })
            .then(response => {
                console.log("Submitted successfully", response.data);
                setSubmitted(true); // triggers navigation in useEffect
            })
            .catch(error => {
                console.error("Request failed:", error);
            })
            .finally(() => {
                setLoading(false); // done loading
            });
    };

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
                            onChange={(e) => setFir_name(e.target.value)}
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
                            onChange={(e) => setLas_name(e.target.value)}

                        />
                    </div>
                    <div className={`w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 ${border1}`}>
                        <input
                            className=""
                            placeholder="E-mail"
                            type="e-mail"
                            name="email"
                            id="email"
                            required
                            autoComplete="true"
                            onChange={(e) => {
                                setBorder1(isValid(e.target.value) ? 'border-green-200' : 'border-red-200');
                                setEmail(e.target.value)
                            }}
                        />
                    </div>
                    <div className={`w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 ${border2}`}>
                        <input
                            className=""
                            placeholder="Numero de telephone"
                            type="number"
                            name="phone_number"
                            id="phone"
                            required
                            autoComplete="true"
                            onChange={(e) => {
                                setBorder2(isValid(e.target.value) ? 'border-green-200' : 'border-red-200');
                                setPhone(e.target.value)
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
                            minLength={4}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <input
                            name="checkbox"
                            type="checkbox"
                            onClick={() => { setvisible1(!visible1) }}
                            className={`max-w-5 h-5 mx-2.5 appearance-none ${visible1 === true ? "bg-[url(./src/assets/icons/hide.svg)]" : "bg-[url(./src/assets/icons/unhide.svg)]"} bg-no-repeat bg-contain bg-center`}
                        />
                    </div>
                    <p className={`w-full text-sm text-center text-red-400 ${passwordSame(password, confpwd) ? 'hidden' : ''}`}>
                        Les mots de passe ne correspondent pas</p>
                    <div className={`w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 ${border3} `}>
                        <input
                            placeholder="Confirmer le mot de passe"
                            type={visible2 ? 'text' : 'password'}
                            name="confirmpwd"
                            id="confirmpwd"
                            required
                            autoComplete="true"
                            minLength={4}
                            onChange={(e) => {
                                setConfpwd(e.target.value);
                                setBorder3(passwordSame(password, e.target.value) ? 'border-green-200' : 'border-red-200')
                            }}

                        />
                        <input
                            name="checkbox"
                            type="checkbox"
                            onClick={() => { setvisible2(!visible2) }}
                            className={`max-w-5 h-5 mx-2.5 appearance-none ${visible2 === true ? "bg-[url(./src/assets/icons/hide.svg)]" : "bg-[url(./src/assets/icons/unhide.svg)]"} bg-no-repeat bg-contain bg-center`}
                        />
                    </div>
                    {/* Where we set the user's activity */}

                    <input
                        type="hidden"
                        name="is_active"
                        value={true} />
                    <Button
                        text={loading ? "Chargement..." : "S'inscrire"}
                        textCol={'text-white'}
                        bg={(loading || !checkValidity) ? 'bg-gray-200' : 'bg-[#ffcd74]'}
                        type={'submit'}
                        disabled={loading || !checkValidity}
                    />
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