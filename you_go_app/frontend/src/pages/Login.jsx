import { useState, useEffect, useMemo } from "react";
import Button from "../components/Button";
import { useGoogleLogin } from '@react-oauth/google';
import axios from "axios"
import isValid from "../functions/entryCheck";
import { Navigate, useNavigate } from "react-router-dom";


function Login() {
    const [formData, setFormData] = useState(
        {
            contact: "",
            password: "",
        });

    const [border1, setBorder1] = useState('border-gray-200')
    const [border2, setBorder2] = useState('border-gray-200')
    const [visible, setvisible] = useState(false)
    const [compatible, setCompatible] = useState(false)
    const [showErr, setShowErr] = useState(false)
    const [password, setPassword] = useState('');
    const [contact, setContact] = useState('');
    const [value, setValue] = useState('')
    const [submitted, setSubmitted] = useState(false);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate()
    // checking compatibility
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData, [name]: value,

        }))
    }
    const handleSubmit = (e) => {
        e.preventDefault()
        console.log("Form Data Submitted: ", formData);

    }

    // Google login handler function
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
    const isCompatible = () => {
        setCompatible((formData.contact.toString() === '0198989898' || formData.contact === 'martharun514@gmail.com') && formData.password === 'legit')
        setShowErr(!((formData.contact.toString() === '0198989898' || formData.contact === 'martharun514@gmail.com') && formData.password === 'legit'))
        setBorder1(((formData.contact.toString() === '0198989898' || formData.contact === 'martharun514@gmail.com') && formData.password === 'legit')?'border-green-200':'border-red-200')
        setBorder2(((formData.contact.toString() === '0198989898' || formData.contact === 'martharun514@gmail.com') && formData.password === 'legit')?'border-green-200':'border-red-200')
    }

    const checkValidity = useMemo(() => {
        return password.trim() !== '' && contact.trim() !== '';
    }, [password, contact]);

    useEffect(() => {
        if (compatible) {
            navigate('/');
        }
    }, [compatible, navigate]);

const send = async (e) => {
    e.preventDefault();
    setLoading(true);
    setShowErr(false);

    try {
        const response = await axios.post('http://localhost:8000/accounts/login/', {
            email: formData.contact,
            password: formData.password
        });
        
        // If login is successful
        const { token, user } = response.data;
        console.log("Login successful", user);

        // Save token to localStorage or context for future requests
        localStorage.setItem("authToken", token);

        // Navigate to home or dashboard
        navigate('/');

    } catch (error) {
        console.error("Login failed:", error.response?.data || error.message);
        setShowErr(true);
    } finally {
        setLoading(false);
    }
};

    return (
        <>
            <div className="w-full h-screen bg-white flex flex-col items-center justify-evenly animate-fade md:bg-amber-300 lg:bg-green-300 font-manrope font-semibold">

                <div className="w-full h-fit pl-10 flex flex-row items-center justify-start">
                    <h1 className="text-4xl ">Connexion</h1>
                </div>
                <form
                    className="w-full h-fit flex flex-col items-center gap-3.5 text-gray-500 [&_input]:focus:outline-0 [&_input]:w-full"
                    onSubmit={
                        (e) => {
                            e.preventDefault();
                            isCompatible(e);
                            handleSubmit(e);
                            send(e);
                        }
                    }
                >
                    <div className={`w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 ${border1}`}>
                        <input
                            className=""
                            placeholder="E-mail ou téléphone"
                            type="text"
                            name="contact"
                            id="contact"
                            value={formData.contact}
                            required
                            autoComplete="true"
                            onChange={(e) => {
                                setBorder1(isValid(e.target.value) ? 'border-green-200' : 'border-red-200')
                                setContact(e.target.value)
                                handleChange(e)
                            }}
                        />
                    </div>
                    <div className={`w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 ${border2 }`}>
                        <input
                            placeholder="Mot de passe"
                            type={visible ? 'text' : 'password'}
                            name="password"
                            id="password"
                            value={formData.password}
                            required
                            autoComplete="true"
                            onChange={(e) => {
                                setPassword(e.target.value)
                                handleChange(e)
                            }}
                        />
                        <input
                            name="checkbox"
                            type="checkbox"
                            onClick={() => { setvisible(!visible) }}
                            className={`max-w-5 h-5 mx-2.5 appearance-none ${visible === true ? "bg-[url(./src/assets/icons/hide.svg)]" : "bg-[url(./src/assets/icons/unhide.svg)]"} bg-no-repeat bg-contain bg-center`}
                        />
                    </div>
                    <input
                        type="hidden"
                        name="is_active"
                        value={true} />
                    <p className="w-9/12 text-right text-sm text-blue-400 mr-2">
                        <a href="/ForgotPassword">Mot de passe oublié</a>
                    </p>
                    <p className={`w-9/12 text-sm text-center text-red-400 ${showErr ? '' : 'hidden'}`}>
                        Vos identifiants sont incorrects.Veuillez réessayer</p>
                    <Button
                        text={loading ? "Chargement..." : "S'inscrire"}
                        textCol={'text-white'}
                        bg={(loading || !checkValidity) ? 'bg-gray-200' : 'bg-[#ffcd74]'}
                        type={'submit'}
                        disabled={loading || !checkValidity}
                    />
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