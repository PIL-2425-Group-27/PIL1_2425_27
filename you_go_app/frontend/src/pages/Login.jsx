import { useState } from "react";
function Login() {
    const [visible, setvisible] = useState(false)
    return (
        <>
            <div className="w-full h-screen bg-white flex flex-col md:bg-amber-300 lg:bg-green-300 font-manrope">
                <form
                    className="w-full h-fit flex flex-col items-center gap-3.5 bg-amber-50 text-gray-600 [&_input]:focus:outline-0 [&_input]:w-full"
                    action=""
                    method="post"
                >
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 focus-within:border-2 border-blue-300">
                        <input
                            placeholder="Prenom"
                            type="text"
                            name="fistname"
                            id="firstname"
                            required
                        />
                    </div>
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 focus-within:border-2 border-blue-300">
                        <input
                            placeholder="Nom"
                            type="text"
                            name="lastname"
                            id="lastname"
                            required
                        />
                    </div>
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 focus-within:border-2 border-blue-300">
                        <input
                            className=""
                            placeholder="Numero de telephone"
                            type="number"
                            name="phone"
                            id="phone"
                            required
                        />
                    </div>
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 focus-within:border-2 border-blue-300">
                        <input
                            placeholder="Mot de passe"
                            type={visible ? 'text' : 'password'}
                            name="password"
                            id="password"
                            required
                        />
                        <input
                            type="checkbox"
                            onClick={() => { setvisible(!visible) }}
                            className="w-2 h-2 appearance-none bg-amber-500"
                        />
                    </div>
                </form>
            </div>
        </>
    );
}

export default Login;