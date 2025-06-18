import { useState } from "react";
import Navbar from "../components/Navbar";

import { UNSAFE_createClientRoutesWithHMRRevalidationOptOut } from "react-router-dom";
import Return from "../components/Return";
import Title from "../components/Title";
function PublishRequest() {
    const[form,setForm] = useState({
        passengerName: "",
        start_point: "",
        end_point: "",
        start_time: "",
        price_preference: "",
        max_price: "",
    });
    const handleChange = (e) => {
        setForm({ ...form, 
            [e.target.name]: e.target.value})
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(form);
        // Les données seront envoyées au backend
    };
    return (
        <>
            <Navbar />
            <Return theme={false} />
            <div className="w-full h-screen flex flex-col items-center py-[10vh]">
                <Title content={"Publier une reqête"} floating={true} />
                <div className="max-w-4xl mx-auto mt-8 p-6 bg-white rounded-2xl shadow-sm border border-gray-200">
                    <form onSubmit={handleSubmit}>
                        <table className="w-full text-left border-separate border-spacing-y-3">
                            <tbody>
                                <tr>
                                    <td className="w-1/3 font-semibold">Nom du passager</td>
                                    <td>
                                        <input
                                            type="text"
                                            className="w-full p-2 border border-gray-300 rounded-lg"
                                            id="driverName"
                                            name="driverName"
                                            value={form.driverName}
                                            onChange={handleChange}
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="font-semibold">Point de départ</td>
                                    <td>
                                        <input
                                            type="text"
                                            className="w-full p-2 border border-gray-300 rounded-lg"
                                            id="start_point"
                                            name="start_point"
                                            value={form.start_point}
                                            onChange={handleChange}
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="font-semibold">Point d'arrivée</td>
                                    <td>
                                        <input
                                            type="text"
                                            className="w-full p-2 border border-gray-300 rounded-lg"
                                            id="end_point"
                                            name="end_point"
                                            value={form.end_point}
                                            onChange={handleChange}
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="font-semibold">Heure de départ</td>
                                    <td>
                                        <input
                                            type="text"
                                            className="w-full p-2 border border-gray-300 rounded-lg"
                                            id="start_time"
                                            name="start_time"
                                            value={form.start_time}
                                            onChange={handleChange}
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="font-semibold">Heure d'arrivée</td>
                                    <td>
                                        <input
                                            type="text"
                                            className="w-full p-2 border border-gray-300 rounded-lg"
                                            id="end_time"
                                            name="end_time"
                                            value={form.end_time}
                                            onChange={handleChange}
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="font-semibold">Préférences de prix</td>
                                    <td>
                                        <input
                                            type="text"
                                            className="w-full p-2 border border-gray-300 rounded-lg"
                                            id="price_preferences"
                                            name="price_preferences"
                                            value={form.price_type}
                                            onChange={handleChange}
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="font-semibold">Prix Max</td>
                                    <td>
                                        <input
                                            type="text"
                                            className="w-full p-2 border border-gray-300 rounded-lg"
                                            id="max_price"
                                            name="max_price"
                                            value={form.fixed_price}
                                            onChange={handleChange}
                                        />
                                    </td>
                                </tr>
                                
                            </tbody>
                        </table>
                        <div className="mt-6 text-right">
                            <button
                                type="submit"
                                className="bg-[#ffcd74] hover:bg-[#ddb570] text-white font-semibold px-6 py-2 rounded-xl transition-colors"
                            >
                                Publier la demande
                            </button>
                        </div>
                    </form>
                </div>


            </div>
        </>
    );
}

export default PublishRequest;