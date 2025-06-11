import { useState } from "react";
import Button from "../components/Button";
import Checkbox from "../components/Checkbox";

function RoleChoice() {
    const [visible, setvisible] = useState(false)

    // choices handler function

    return (
        <>
            <div className="relative w-full h-screen bg-white flex flex-col items-center justify-center animate-fade md:bg-amber-300 lg:bg-green-300 font-manrope font-semibold">

                <div className="absolute top-[5vh] left-[6vw] w-12 aspect-square">
                    <img
                        src="/logo-light.svg"
                        alt="" />
                </div>
                <div className="w-full h-fit pl-10 mb-3 flex flex-col items-start justify-center gap-2">
                    <h1 className="text-3xl font-bold animate-fade-right animate-delay-200">Bienvenue !</h1>
                </div>
                <div className="w-full h-fit pl-10 flex flex-col items-start justify-center gap-2">
                    <h1 className="text-4xl animate-fade-right animate-delay-700">Choisissez votre</h1>
                    <h1 className="text-4xl font-bold ml-8 text-[#ffcd74] animate-fade-right animate-delay-900">Rôle</h1>
                </div>
                <form
                    className="py-15 w-full h-fit flex flex-col items-center gap-4.5 text-gray-700 [&_input]:focus:outline-0 [&_input]:w-full"
                    action=""
                    method="post"
                >
                    <div className="flex flex-col items-start w-7/9 gap-3 mb-8">
                        <Checkbox text={'Passager'} val={'passager'} name={'role'}/>
                        <Checkbox text={'Conducteur'} val={'conducteur'} name={'role'} />
                    </div>
                    <Button text={"Valider"} textCol={'text-gray-100'} bg={'bg-[#ffcd74]'} />

                    <p
                        className="my-9 text-sm">
                        Veuillez choisir un role pour continuer.
                    </p>
                </form>

            </div>
        </>
    );
}

export default RoleChoice;