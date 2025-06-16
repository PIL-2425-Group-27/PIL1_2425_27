import { useState } from "react";
import Navbar from "../components/Navbar";
import { UNSAFE_createClientRoutesWithHMRRevalidationOptOut } from "react-router-dom";
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
            <h1 className='text-green-400'>PublishRequest Page</h1>
            <Navbar/>
            <div className="container mt-5">
                <h2>Publier une demande</h2>
                <form onSubmit={handleSubmit} className="mt-4" >
                    <div className="mt-3">
                        <label htmlFor="passengerName" className="form-label">Nom du passager</label>
                        <input 
                        type="text" 
                        className="form-control"
                        id="passengerName"
                        name="passengerName"
                        value={form.passengerName}
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
                        name="end_point"
                        value={form.end_point}
                        onChange={handleChange}/>
                    </div>
                    <div className="mt-3">
                        <label htmlFor="start_time" className="form-label">Date + heure de départ</label>
                        <input 
                        type="text" 
                        className="form-control"
                        id="start_time"
                        name="start_time"
                        value={form.start_time}
                        onChange={handleChange}/>
                    </div>
                    <div className="mt-3">
                        <label htmlFor="price_preference" className="form-label">Préférence paiement</label>
                        <input 
                        type="text" 
                        className="form-control"
                        id="price_preference"
                        name="price_preference"
                        value={form.price_preference}
                        onChange={handleChange}/>
                    </div>
                    <div className="mt-3">
                        <label htmlFor="max_price" className="form-label">Max optionnel</label>
                        <input 
                        type="text" 
                        className="form-control"
                        id="max_price"
                        name="max_price"
                        value={form.max_price}
                        onChange={handleChange}/>
                    </div>
                    <button type="submit" className=" bg-black text-white px-4 rounded">Publier la demande</button>
                </form>       
            </div>
        </> 
    );
}

export default PublishRequest;