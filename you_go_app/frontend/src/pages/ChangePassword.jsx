import { useState, useMemo, useEffect } from "react";
import Button from "../components/Button";
import Return from "../components/Return";
import passwordSame from "../functions/passwordSame";
import { Navigate, useNavigate } from "react-router-dom";


function ChangePassword() {
    let theme = false
    const [visible, setvisible] = useState(false)
    const [border, setBorder] = useState('border-gray-200')
    const [value, setValue] = useState('')
    const [submitted, setSubmitted] = useState(false);
    const [newPwd, setNewpwd] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate()
    // login handler function
    useEffect(() => {
            if (submitted) {
                navigate('/PasswordChanged');
            }
        }, [submitted, navigate]);

    const login = (e) => {
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
    }

    const checkValidity = useMemo(() => {
        return (password.trim() !== '' && newPwd.trim() !== '' && (password == newPwd));
    }, [ password, newPwd]);

    return (
        <>
            <div className="w-full h-screen bg-white flex flex-col items-center justify-evenly animate-fade md:bg-amber-300 lg:bg-green-300 font-manrope font-semibold">

                <Return theme={theme} />
                <div className="w-full h-fit pl-10 flex flex-row items-center justify-start">
                    <h1 className="text-4xl ">Changer le Mot de passe</h1>
                </div>
                <div className="w-6/10 aspect-square">
                    <img
                        src="./src/assets/img/reset-password.svg"
                        alt="" />
                </div>
                <form
                    className="w-full h-fit flex flex-col items-center justify-center gap-3.5 text-gray-500 [&_input]:focus:outline-0 [&_input]:w-full"
                    onSubmit={(e)=>{
                        login(e)
                    }}
                >
                    <div className={`w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 ${border}`}>
                        <input
                            placeholder="Nouveau mot de passe"
                            type={visible ? 'text' : 'password'}
                            name="password"
                            id="password"
                            required
                            autoComplete="true"
                            minLength={4}
                            onChange={(e) => {
                                setPassword(e.target.value);
                            }}
                        />
                        <input
                            name="checkbox"
                            type="checkbox"
                            onClick={() => { setvisible(!visible) }}
                            className={`max-w-5 h-5 mx-2.5 appearance-none ${visible === true ? "bg-[url(./src/assets/icons/hide.svg)]" : "bg-[url(./src/assets/icons/unhide.svg)]"} bg-no-repeat bg-contain bg-center`}
                        />
                    </div>
                    <div className={`w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 ${border}`}>
                        <input
                            placeholder="Confirmer le mot de passe"
                            type={visible ? 'text' : 'password'}
                            name="newPassword"
                            id="newPassword"
                            required
                            autoComplete="true"
                            minLength={4}
                            onChange={(e) => {
                                setNewpwd(e.target.value);
                                setBorder(passwordSame(password, e.target.value) ? 'border-green-200' : 'border-red-200')
                            }}
                        />
                        <input
                            name="checkbox"
                            type="checkbox"
                            onClick={() => { setvisible(!visible) }}
                            className={`max-w-5 h-5 mx-2.5 appearance-none ${visible === true ? "bg-[url(./src/assets/icons/hide.svg)]" : "bg-[url(./src/assets/icons/unhide.svg)]"} bg-no-repeat bg-contain bg-center`}
                        />
                    </div>
                    <p className={`text-red-400 text-sm ${passwordSame(password, newPwd) ? 'hidden' : ''}`}>Les mots de passe ne correspondent pas</p>
                    <Button
                        text={loading ? "Chargement..." : "Changer"}
                        textCol={'text-white'}
                        bg={(loading || !checkValidity) ? 'bg-gray-200' : 'bg-[#ffcd74]'}
                        type={'submit'}
                        disabled={loading || !checkValidity}
                    />
                </form>

            </div>
        </>
    );
}

export default ChangePassword;