import { useState } from "react";
import Button from "../components/Button";
import Title from "../components/Title";
import Return from "../components/Return";

function ModifProfile() {
    const [picture, setPicture] = useState('./src/assets/img/bg.jpg')
    const changeFile = (e) => {
        const files = e.target.files;
        for (const file of files) {
            if (!file.type.startsWith("image/")) {
                console.warn("Not an image file");
                continue;
            }
            const reader = new FileReader();
            reader.onload = (event) => {
                setPicture(event.target.result);
            };
            reader.readAsDataURL(file);
        }
    };
    let fn = 'John'
    let ln = "DOE"
    let statut = 'Passager'
    let ld = 'Agla'
    let hd = '6:30'
    return (
        <>
            <div
                className="w-full h-screen bg-white flex flex-col items-center justify-evenly py-10"
            >
                <Return link={'/Profile'} />
                <Title content={'Modifier le Profil'} floating={true} />
                <form
                    className="w-full h-max flex flex-col items-center">
                    <div
                        className=" relative w-6/7 rounded-xl py-4  bg-[#e8e8e8] flex flex-col items-center"
                    >
                        <div className="absolute top-5 right-5 w-1/10 aspect-square bg-center bg-cover bg-[url(./src/assets/icons/edit.svg)]"></div>
                        <div
                            style={{ backgroundImage: `url(${picture})` }}
                            className={`w-[30vw] aspect-square rounded-full bg-center bg-cover`}>
                        </div>
                        <label className="w-fit px-[4vw] py-[2vh] text-xl mt-[4vh] font-semibold rounded-xl bg-white text-center">
                            Choisir un fichier
                            <input
                                className="text-[0px]"
                                placeholder="photo"
                                onChange={(e) => { changeFile(e) }}
                                type="file"
                                name="photo"
                                id="file"
                                accept="image/*" />
                        </label>
                    </div>
                    <div className="w-6/7 flex flex-col items-center py-[4vh] gap-[1.5vh] [&_input]:border-b-1 [&_input]:text-xl [&_input]:p-2 [&_input]:outline-none [&_input]: [&_label]:font-semibold [&_select]:c-none [&_select]:focus:outline-none">
                        <div className="w-8/9 flex flex-col">
                            <label htmlFor="fn">Prénom</label>
                            <input
                                placeholder={fn}
                                type="text"
                                name="first_name"
                                id="fn" />
                        </div>
                        <div className="w-8/9 flex flex-col">
                            <label htmlFor="fn">Nom</label>
                            <input
                                placeholder={ln}
                                type="text"
                                name="first_name"
                                id="ln" />
                        </div>

                        <div className="w-8/9 flex flex-col gap-2">
                            <label htmlFor="statut">Statut</label>
                        <select name="statut" id="statut">
                                <option value="passager">Passager</option>
                                <option value="conducteur">Conducteur</option>
                            </select>
                        </div>
                        <div className="w-8/9 flex flex-col">
                            <label htmlFor="lieu">Lieu-départ</label>
                            <input
                                placeholder={ld}
                                type="text"
                                name="first_name"
                                id="lieu" />
                        </div>
                        <div className="w-8/9 flex flex-col">
                            <label htmlFor="heure">Heure-départ</label>
                            <input
                                placeholder={hd}
                                type="text"
                                name="first_name"
                                id="heure" />
                        </div>
                    </div>
                </form>
                <Button text={"Valider"} textCol={'text-white'} bg={'bg-green-400'}  submitted={true} link={'/login'} />
            </div>
        </>
    );
}

export default ModifProfile;