import { useState } from "react";
import Navbar from "../components/Navbar";
function PublishOffer() {
    const [form, setForm] = useState({
        driverName: "",
        start_point: "",
        end_point: "",
        start_time: "",
        end_time: "",
        price_type: "",
        fixed_priced: "",
        Vehiclesmodel: "",

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
                        className="form-control"
                        id="driverName"
                        name="driverName"
                        value={form.driverName}
                        onChange={handleChange}/>
                </div>

            </form>
        </div>
        </>
    );
}

export default PublishOffer;