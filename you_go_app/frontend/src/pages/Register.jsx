import { useState } from "react";
function Register() {
    const [visible1, setvisible1] = useState(false)
    const [visible2, setvisible2] = useState(false)
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
                <div className="w-full h-full px-10 flex flex-row items-center justify-start">
                    <h1 className="text-4xl ">Inscription</h1>
                </div>
                <form
                    className="w-full h-fit flex flex-col items-center gap-3.5 text-gray-500 [&_input]:focus:outline-0 [&_input]:w-full"
                    action=""
                    method="post"
                >
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 border-gray-200 focus-within:border-blue-300">
                        <input
                            placeholder="Prenom"
                            type="text"
                            name="fistname"
                            id="firstname"
                            autoComplete="true"
                        />
                    </div>
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 border-gray-200 focus-within:border-blue-300">
                        <input
                            placeholder="Nom"
                            type="text"
                            name="lastname"
                            id="lastname"
                            required
                            autoComplete="true"
                        />
                    </div>
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 border-gray-200 focus-within:border-blue-300">
                        <input
                            className=""
                            placeholder="E-mail"
                            type="e-mail"
                            name="email"
                            id="email"
                            required
                            autoComplete="true"
                        />
                    </div>
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 border-gray-200 focus-within:border-blue-300">
                        <input
                            className=""
                            placeholder="Numero de telephone"
                            type="number"
                            name="phone"
                            id="phone"
                            required
                            autoComplete="true"
                        />
                    </div>
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 border-gray-200 focus-within:border-blue-300">
                        <input
                            placeholder="Mot de passe"
                            type={visible1 ? 'text' : 'password'}
                            name="password"
                            id="password"
                            required
                            autoComplete="true"
                        />
                        <input
                            name="checkbox"
                            type="checkbox"
                            onClick={() => { setvisible1(!visible1) }}
                            className={`max-w-5 h-5 mx-2.5 appearance-none ${visible1 === true ? "bg-[url(./src/assets/icons/hide.svg)]" : "bg-[url(./src/assets/icons/unhide.svg)]"} bg-no-repeat bg-contain bg-center`}
                        />
                    </div>
                    <div className="w-9/12 max-w-lg h-13 bg-white rounded-4xl flex flex-row items-center justify-between px-4 border-2 border-gray-200 focus-within:border-blue-300">
                        <input
                            placeholder="Confirmer le mot de passe"
                            type={visible2 ? 'text' : 'password'}
                            name="confirmpwd"
                            id="confirmpwd"
                            required
                            autoComplete="true"
                        />
                        <input
                            name="checkbox"
                            type="checkbox"
                            onClick={() => { setvisible2(!visible2) }}
                            className={`max-w-5 h-5 mx-2.5 appearance-none ${visible2 === true ? "bg-[url(./src/assets/icons/hide.svg)]" : "bg-[url(./src/assets/icons/unhide.svg)]"} bg-no-repeat bg-contain bg-center`}
                        />
                    </div>
                    <button
                        disabled
                        type="submit"
                        className="w-9/12 max-w-lg h-13 rounded-4xl text-xl text-white bg-blue-300"
                    >S'inscrire
                    </button>
                    <p>ou</p>
                    <button
                        className="w-9/12 max-w-lg h-13 px-4 rounded-4xl flex flex-row items-center justify-center text-gray-500 bg-gray-100"
                    >
                        <p
                            className="w-max"
                        >Continuer avec
                        </p>
                        <img
                            className="mx-2 w-9"
                            src="./src/assets/icons/google.svg"
                            alt="googleIcon" />
                    </button>
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