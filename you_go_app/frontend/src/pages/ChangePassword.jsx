import { useState, useRef } from "react";
import Button from "../components/Button";
import Return from "../components/Return";

function ChangePassword() {
    const [visible, setvisible] = useState(false)
    const [same, setSame] = useState(false)
    const [value, setValue] = useState('')
    const [submitted, setSubmitted] = useState(false);
    const oldpwd = useRef(null)
    const newpwd = useRef(null);
    // login handler function
    const login = (e) => {
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
            .then(() => setSubmitted(prevSubmitted => true))
            .then(json => console.log(json))
            .catch(e => {
                console.log("failed")
            })
    }
    const condition = submitted
    let show = 'hidden'
    const compatible = () => {
        setSame(oldpwd.value === newpwd.value)
        show = same ? 'hidden':'';
        console.log(newpwd.current.value);
        console.log(same);
        console.log(oldpwd.current.value === newpwd.current.value);

    }
    return (
        <>
            <div className="w-full h-screen bg-white flex flex-col items-center justify-evenly animate-fade md:bg-amber-300 lg:bg-green-300 font-manrope font-semibold">

                <Return link={'/Profile'}/>
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
                    action=""
                    method="post"
                    onSubmit={login}
                >
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 border-gray-200 focus-within:border-[#ffdb99]">
                        <input
                            placeholder="Nouveau mot de passe"
                            type={visible ? 'text' : 'password'}
                            name="password"
                            id="password"
                            required
                            autoComplete="true"
                            ref={oldpwd}
                        />
                        <input
                            name="checkbox"
                            type="checkbox"
                            onClick={() => { setvisible(!visible) }}
                            className={`max-w-5 h-5 mx-2.5 appearance-none ${visible === true ? "bg-[url(./src/assets/icons/hide.svg)]" : "bg-[url(./src/assets/icons/unhide.svg)]"} bg-no-repeat bg-contain bg-center`}
                        />
                    </div>
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 border-gray-200 focus-within:border-[#ffdb99]">
                        <input
                            placeholder="Confirmer le mot de passe"
                            type={visible ? 'text' : 'password'}
                            name="newPassword"
                            id="newPassword"
                            required
                            autoComplete="true"
                            ref={newpwd}
                            onChange={console.log('raven')}
                        />
                        <input
                            name="checkbox"
                            type="checkbox"
                            onClick={() => { setvisible(!visible) }}
                            className={`max-w-5 h-5 mx-2.5 appearance-none ${visible === true ? "bg-[url(./src/assets/icons/hide.svg)]" : "bg-[url(./src/assets/icons/unhide.svg)]"} bg-no-repeat bg-contain bg-center`}
                        />
                    </div>
                    <p className={`text-red-400 text-sm ${show}`}>Les mots de passe ne correspondent pas</p>
                    <Button text={"Changer"} textCol={'text-white'} bg={'bg-[#ffcd74]'} submitted={condition} link={'/PasswordChanged'} />
                </form>

            </div>
        </>
    );
}

export default ChangePassword;