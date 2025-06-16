import { useState } from "react";
import Button from "../components/Button";
import isValid from "../functions/entryCheck";
import Return from "../components/Return";
Return
function ForgotPassword() {
    const [border, setBorder] = useState('border-gray-200')
    const [value, setValue] = useState('')
    const [submitted, setSubmitted] = useState(false);
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
            .then(() => setSubmitted(prev =>{ const newVal=!prev;return newVal}))
            .then(json => console.log(submitted))
            .catch(e => {
                console.log("failed")
            })
    }
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
                    <Button text={"Suivant"} textCol={'text-white'} bg={'bg-[#ffcd74]'} type={'submit'} submitted={submitted} link={'/Verification'} />
                </form>
            </div>
        </>
    );
}

export default ForgotPassword;