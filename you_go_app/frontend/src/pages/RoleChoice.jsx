
import { useRef, useState, useEffect } from "react";
import Button from "../components/Button";
import Checkbox from "../components/Checkbox";
import { useNavigate } from "react-router-dom";

function RoleChoice() {
    const [role, setRole] = useState('passager')
    const [roleImg, setRoleImg] = useState('./src/assets/img/passenger.svg')
    const [value, setValue] = useState('')
    const [submitted, setSubmitted] = useState(false);
    const passer = (data) => {
        setRole('passager')
        data=='passager'?setRoleImg('./src/assets/img/passenger.svg'):setRoleImg('./src/assets/img/driver.gif');
        data=='passager'?setRole('passager'):setRole('conducteur');
        console.log(data);
    }
    // choices handler function
        const [loading, setLoading] = useState(false);
    const navigate = useNavigate()
    
    useEffect(() => {
        if (submitted) {
            navigate('/');
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
    return (
        <>
            <div className="relative w-full h-screen bg-white flex flex-col items-center justify-center animate-fade md:bg-amber-300 lg:bg-green-300 font-manrope font-semibold">

                <div className="absolute top-[5vh] left-[6vw] w-11 aspect-square">
                    <img
                        src="/logo-light.svg"
                        alt="" />
                </div>
                <div className="w-full h-fit pl-10 mb-[1vh] flex flex-col items-start justify-center gap-[2vh]">
                    <h1 className="text-3xl font-bold animate-fade-right animate-delay-200">Bienvenue !</h1>
                </div>
                <div className="w-full h-fit pl-10 flex flex-col items-start justify-center gap-[2vh]">
                    <h1 className="text-3xl animate-fade-right animate-delay-700">Choisissez votre</h1>
                    <h1 className="text-4xl font-bold ml-8 text-[#ffcd74] animate-fade-right animate-delay-900">Statut</h1>
                </div>
                <div className="h-[30vh] aspect-square flex flex-col items-center justify-center animate-fade animate-delay-1000">
                    <img
                        src={roleImg}
                        alt="passenger/driver" />
                </div>
                <form
                    className="py-[3vh] w-full h-fit flex flex-col items-center gap-[1vh] animate-fade animate-delay-1200 text-gray-700 [&_input]:focus:outline-0 [&_input]:w-full"
                    method="post"
                    onSubmit={send}
                >
                    <div className="flex flex-col items-start w-7/9 gap-[1vh] mb-[4vh]">
                        <Checkbox text={'Passager'} val={'passager'} name={'role'} passer={passer} checked={true} selected ={role=='passager'}/>
                        <Checkbox text={'Conducteur'} val={'conducteur'} name={'role'} passer={passer} checked={false} selected ={role=='conducteur'}/>
                    </div>
                    <Button
                        text={loading ? "Chargement..." : "Valider"}
                        textCol={'text-white'}
                        bg={loading ? 'bg-gray-400' : 'bg-[#ffcd74]'}
                        type={'submit'}
                        disabled={loading}
                    />

                    <p
                        className="mt-[1vh] text-sm">
                        Veuillez choisir un role pour continuer.
                    </p>
                </form>

            </div>
        </>
    );
}

export default RoleChoice;