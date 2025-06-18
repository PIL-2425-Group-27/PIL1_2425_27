import { useState } from "react";
import Navbar from "../components/Navbar";
import Return from "../components/Return";
import Title from "../components/Title";

function PublishOffer() {
    const [form, setForm] = useState({
        driverName: "",
        start_point: "",
        end_point: "",
        start_time: "",
        end_time: "",
        price_type: "",
        fixed_price: "",
        vehiculesmodel: "",
        seats: "",
        description: ""
    });
    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value
        });
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
            <div className="w-full h-screen flex flex-col items-center py-[5vh]">
                <Title content={"Publier une offre"} floating={true} />
                <div className="max-w-4xl mx-auto mt-8 p-6 bg-white rounded-2xl shadow-sm border border-gray-200">
                    <form onSubmit={handleSubmit}>
                        <table className="w-full text-left border-separate border-spacing-y-3">
                            <tbody>
                                <tr>
                                    <td className="w-1/3 font-semibold">Nom du conducteur</td>
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
                                    <td className="font-semibold">Nature du prix</td>
                                    <td>
                                        <input
                                            type="text"
                                            className="w-full p-2 border border-gray-300 rounded-lg"
                                            id="price_type"
                                            name="price_type"
                                            value={form.price_type}
                                            onChange={handleChange}
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="font-semibold">Prix fixé</td>
                                    <td>
                                        <input
                                            type="text"
                                            className="w-full p-2 border border-gray-300 rounded-lg"
                                            id="fixed_price"
                                            name="fixed_price"
                                            value={form.fixed_price}
                                            onChange={handleChange}
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="font-semibold">Modèle de véhicule</td>
                                    <td>
                                        <input
                                            type="text"
                                            className="w-full p-2 border border-gray-300 rounded-lg"
                                            id="vehiculesmodel"
                                            name="vehiculesmodel"
                                            value={form.vehiculesmodel}
                                            onChange={handleChange}
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="font-semibold">Places disponibles</td>
                                    <td>
                                        <input
                                            type="text"
                                            className="w-full p-2 border border-gray-300 rounded-lg"
                                            id="seats"
                                            name="seats"
                                            value={form.seats}
                                            onChange={handleChange}
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="font-semibold">Conditions</td>
                                    <td>
                                        <input
                                            type="text"
                                            className="w-full p-2 border border-gray-300 rounded-lg"
                                            id="description"
                                            name="description"
                                            value={form.description}
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
                                Publier l'offre
                            </button>
                        </div>
                    </form>
                </div>


            </div>
        </>
    );
}

export default PublishOffer;