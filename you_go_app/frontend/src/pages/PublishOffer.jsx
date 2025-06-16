import { useState } from "react";
import {GoogleOAuthprovider} from "@react-oauth/google";
import Navbar from "../components/Navbar";
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
        description: "",

    });
    const handleChange = (e) => {
        setForm({ ...form, 
            [e.target.name]: e.target.value});
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(form);
        // Les données seront envoyées au backend
    };
    return (
        <>
        <Navbar/>
        <div className="container mt-5">
            <h2>Publier une offre</h2>
            <form onSubmit={handleSubmit} className="mt-4">
                <div className="mt-3">
                    <label htmlFor="driverName" className="form-label">Nom du conducteur</label>
                    <input 
                        type="text" 
                        className="w-full p-2 border rounded-2xl"
                        id="driverName"
                        name="driverName"
                        value={form.driverName}
                        onChange={handleChange}/>
                </div>
                <div className="mt-3">
                    <label htmlFor="start_point" className="form-label">Point de départ</label>
                    <input 
                    type="text" 
                    className="form-control"
                    id="start_point"
                    name="start_point"
                    value={form.start_point}
                    onChange={handleChange}/>
                </div>
                <div className="mt-3">
                    <label htmlFor="end_point" className="form-label">Point d'arrivée</label>
                    <input 
                    type="text" 
                    className="form-control"
                    id="end_point"
                    name=" end_point"
                    value={form.end_point}
                    onChange={handleChange}/>
                </div>
                <div className="mt-3">
                    <label htmlFor="start_time" className="form-label">Heure de départ</label>
                    <input 
                    type="text" 
                    className="form-control"
                    id="start_time"
                    name="start_time"
                    value={form.start_time}
                    onChange={handleChange}/>
                </div>
                <div className="mt-3">
                    <label htmlFor="end_time" className="form-label">Heure d'arrivée</label>
                    <input 
                    type="text" 
                    className="form-control"
                    id="end_time"
                    name="end_time"
                    value={form.end_time}
                    onChange={handleChange}/>
                </div>
                <div className="mt-3">
                    <label htmlFor="price_type" className="form-label">Nature du prix</label>
                    <input 
                    type="text" 
                    className="form-control"
                    id="price_type"
                    name="price_type"
                    value={form.price_type}
                    onChange={handleChange}/>
                </div>
                <div className="mt-3">
                    <label htmlFor="fixed_price" className="form-label">Prix fixé</label>
                    <input 
                    type="text" 
                    className="form-control"
                    id="fixed_price"
                    name="fixed_price"
                    value={form.fixed_price}
                    onChange={handleChange}/>
                </div>
                <div className="mt-3">
                    <label htmlFor="vehiculesmodel" className="form-label">Modèle de véhicule</label>
                    <input 
                    type="text" 
                    className="form-control"
                    id="vehiculesmodel"
                    name="vehiculesmodel"
                    value={form.vehiculesmodel}
                    onChange={handleChange}/>
                </div>
                <div className="mt-3">
                    <label htmlFor="seats" className="form-label">Nombres de places disponibles</label>
                    <input 
                    type="text" 
                    className="form-control"
                    id="seats"
                    name="seats"
                    value={form.seats}
                    onChange={handleChange}/>
                </div>
                <div className="mt-3">
                    <label htmlFor="description" className="form-label">Conditions</label>
                    <input 
                    type="text" 
                    className="form-control"
                    id="description"
                    name="description"
                    value={form.description}
                    onChange={handleChange}/>
                </div>
                <button type="submit" className="bg-green-950 text-white px-4 rounded">Publier l'offre</button>

            </form>
        </div>
        </>
    );
}

export default PublishOffer;