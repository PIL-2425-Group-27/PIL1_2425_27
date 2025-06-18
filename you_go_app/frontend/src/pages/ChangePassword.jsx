import { useState, useMemo, useEffect } from "react";
import Button from "../components/Button";
import Return from "../components/Return";
import passwordSame from "../functions/passwordSame";
import { Navigate, useNavigate } from "react-router-dom";

function ChangePassword() {
    let theme = false
    const [visible, setvisible] = useState(false)
    const [border, setBorder] = useState('border-gray-200')
    const [submitted, setSubmitted] = useState(false);
    const [newPwd, setNewpwd] = useState('');
    const [password, setPassword] = useState('');
    const [oldPassword, setOldPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate()

    // Navigation effect
    useEffect(() => {
        if (submitted) {
            navigate('/PasswordChanged');
        }
    }, [submitted, navigate]);

    // Change password handler function
    const changePassword = (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        // Get JWT token from localStorage or wherever you store it
        const token = localStorage.getItem('access_token');
        
        if (!token) {
            setError('Vous devez être connecté pour changer votre mot de passe');
            setLoading(false);
            return;
        }

        fetch('/api/accounts/password/change/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                old_password: oldPassword,
                new_password: password,
                new_password2: newPwd
            })
        })
         .then(response => response.json())
        .then(data => {
            console.log("Mot de passe changé avec succès", data);
            setSubmitted(true);
        })
        .catch(err => {
            console.error("Erreur:", err);
        })
        .finally(() => {
            setLoading(false);
        });
    }

    const checkValidity = useMemo(() => {
        return (
            oldPassword.trim() !== '' && 
            password.trim() !== '' && 
            newPwd.trim() !== '' && 
            password === newPwd
        );
    }, [oldPassword, password, newPwd]);

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
                    onSubmit={changePassword}
                >
                    {/* Old Password Field */}
                    <div className={`w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 ${border}`}>
                        <input
                            placeholder="Ancien mot de passe"
                            type={visible ? 'text' : 'password'}
                            name="oldPassword"
                            id="oldPassword"
                            required
                            autoComplete="current-password"
                            minLength={4}
                            value={oldPassword}
                            onChange={(e) => {
                                setOldPassword(e.target.value);
                            }}
                        />
                        <input
                            name="checkbox"
                            type="checkbox"
                            onClick={() => { setvisible(!visible) }}
                            className={`max-w-5 h-5 mx-2.5 appearance-none ${visible === true ? "bg-[url(./src/assets/icons/hide.svg)]" : "bg-[url(./src/assets/icons/unhide.svg)]"} bg-no-repeat bg-contain bg-center`}
                        />
                    </div>

                    {/* New Password Field */}
                    <div className={`w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 ${border}`}>
                        <input
                            placeholder="Nouveau mot de passe"
                            type={visible ? 'text' : 'password'}
                            name="password"
                            id="password"
                            required
                            autoComplete="new-password"
                            minLength={4}
                            value={password}
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

                    {/* Confirm New Password Field */}
                    <div className={`w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 ${border}`}>
                        <input
                            placeholder="Confirmer le mot de passe"
                            type={visible ? 'text' : 'password'}
                            name="newPassword"
                            id="newPassword"
                            required
                            autoComplete="new-password"
                            minLength={4}
                            value={newPwd}
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

                    <p className={`text-red-400 text-sm ${passwordSame(password, newPwd) ? 'hidden' : ''}`}>
                        Les mots de passe ne correspondent pas
                    </p>

                    {/* Error message */}
                    {error && (
                        <p className="text-red-400 text-sm text-center max-w-lg">
                            {error}
                        </p>
                    )}

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