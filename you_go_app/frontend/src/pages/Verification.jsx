
import { useState } from "react";
import Button from "../components/Button";

function Verification() {
    const [value, setValue] = useState('')
    const [submitted, setSubmitted] = useState(false);
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
    return (
        <>
            <div className="w-full h-screen bg-white flex flex-col items-center justify-center gap-[4vh] animate-fade md:bg-amber-300 lg:bg-green-300 font-manrope font-semibold">

                <div className="flex flex-row items-start px-2.5 absolute top-12 left-3">
                    <a
                        className="flex flex-row text-sm font-bold"
                        href="/ForgotPassword"><img
                            className="w-5 aspect-square"
                            src="./src/assets/icons/left-arrow.svg"
                            alt="return" />Retour
                    </a>
                </div>
                <div className="w-full h-fit pl-10 flex flex-row items-center justify-start">
                    <h1 className="text-3xl font-bold">Vérification</h1>
                </div>
                <div className="w-6/10 aspect-square">
                    <img
                        src="./src/assets/img/OTP.svg"
                        alt="" />
                </div>
                <form
                    className="w-full h-fit flex flex-col items-center gap-5 text-gray-500 [&_input]:focus:outline-0 [&_input]:w-full [&_input]:text-center"
                    action=""
                    method="post"
                    onSubmit={login}
                >
                    <div className="flex flex-row w-full items-center justify-center gap-2 text-3xl">
                        <div className="w-2/12 aspect-square bg-white rounded-xl flex flex-row items-center justify-center px-4 border-2 border-gray-200 focus-within:border-[#ffdb99]">
                            <input
                                placeholder="X"
                                type="number"
                                name="contact"
                                id="contact"
                                max={9}
                                required
                            />
                        </div>
                        <div className="w-2/12 aspect-square bg-white rounded-xl flex flex-row items-center justify-center px-4 border-2 border-gray-200 focus-within:border-[#ffdb99]">
                            <input
                                placeholder="X"
                                type="number"
                                name="contact"
                                id="contact"
                                max={9}
                                required
                            />
                        </div>
                        <div className="w-2/12 aspect-square bg-white rounded-xl flex flex-row items-center justify-center px-4 border-2 border-gray-200 focus-within:border-[#ffdb99]">
                            <input
                                placeholder="X"
                                type="number"
                                name="contact"
                                id="contact"
                                max={9}
                                required
                            />
                        </div>
                        <div className="w-2/12 aspect-square bg-white rounded-xl flex flex-row items-center justify-center px-4 border-2 border-gray-200 focus-within:border-[#ffdb99]">
                            <input
                                placeholder="X"
                                type="number"
                                name="contact"
                                id="contact"
                                max={9}
                                required
                            />
                        </div>
                    </div>
                    <Button text={"Vérifier"} textCol={'text-white'} bg={'bg-[#ffcd74]'} type={'submit'} submitted={submitted} link={'/ChangePassword'} />
                </form>

            </div>
        </>
    );
}

export default Verification;