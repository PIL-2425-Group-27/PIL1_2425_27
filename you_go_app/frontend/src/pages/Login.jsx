import { useState } from "react";
function Login() {
    const [visible, setvisible] = useState(false)
    return (
        <>
            <div className="w-full h-screen bg-white flex flex-col items-center justify-evenly md:bg-amber-300 lg:bg-green-300 font-manrope font-semibold">

                <div className="flex flex-row items-start px-2.5 absolute top-12 left-3">
                    <a href="/"><img
                        className="w-6 aspect-square"
                        src="./src/assets/icons/left-arrow.svg"
                        alt="return" />
                    </a>
                </div>
                <form
                    className="w-full h-fit flex flex-col items-center gap-3.5 text-gray-500 [&_input]:focus:outline-0 [&_input]:w-full"
                    action=""
                    method="post"
                >
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 border-gray-200 focus-within:border-blue-300">
                        <input
                            className=""
                            placeholder="E-mail ou téléphone"
                            type="text"
                            name="contact"
                            id="contact"
                            required
                            autoComplete="true"
                        />
                    </div>
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 border-gray-200 focus-within:border-blue-300">
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
                    <button
                        disabled
                        type="submit"
                        className="w-9/12 max-w-lg h-13 rounded-4xl text-xl text-white bg-blue-300"
                    >Se connecter
                    </button>
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