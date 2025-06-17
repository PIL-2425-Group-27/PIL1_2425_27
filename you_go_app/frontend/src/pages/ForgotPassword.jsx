import { useState, useEffect } from "react";
import Button from "../components/Button";
import isValid from "../functions/entryCheck";
import Return from "../components/Return";
import { Navigate, useNavigate } from "react-router-dom";

function ForgotPassword(props) {
    const [border, setBorder] = useState('border-gray-200')
    const [value, setValue] = useState('')
    const [submitted, setSubmitted] = useState(false);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate()
    
    useEffect(() => {
        if (submitted) {
            navigate('/Verification');
        }
    }, [submitted, navigate]);

    const send = (e) => {
        e.preventDefault();
        setLoading(true); // start loading

        fetch(
            'https://jsonplaceholder.typicode.com/todos',
            {
                method: 'POST',
                body: JSON.stringify({
                    value,
                    completed: false
                }),
                headers: {
                    'Content-type': 'application/json; charset=UTF-8'
                }
            }
        )
            .then(response => response.json())
            .then(data => {
                console.log("Submitted successfully", data);
                setSubmitted(true); // triggers navigation in useEffect
            })
            .catch(err => {
                console.error("Request failed:", err);
            })
            .finally(() => {
                setLoading(false); // done loading
            });
    };
    // /^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$/
    //  /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/
    return (
        <>
            <div className="w-full h-screen bg-white flex flex-col items-center justify-center gap-[4vh] animate-fade md:bg-amber-300 lg:bg-green-300 font-manrope font-semibold">

                <Return link={'/Login'} />
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
                    method="post"
                    onSubmit={send}
                >
                    <div className={`w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-3 ${border}`}>
                        <input
                            placeholder="E-mail ou téléphone"
                            type="text"
                            name="contact"
                            id="contact"
                            required
                            autoComplete="true"
                            onChange={(e) => {
                                setValue(e.target.value)
                                console.log('changed', e.target.value)
                                setBorder(isValid(e.target.value) ? 'border-green-200' : 'border-red-200')
                            }}
                        />
                    </div>
                    {/*onClick={() => login()}  link={'/Verification'}*/}
                    <Button
                        text={loading ? "Chargement..." : "Suivant"}
                        textCol={'text-white'}
                        bg={loading ? 'bg-gray-400' : 'bg-[#ffcd74]'}
                        type={'submit'}
                        disabled={loading}
                    />
                </form>
            </div>
        </>
    );
}

export default ForgotPassword;