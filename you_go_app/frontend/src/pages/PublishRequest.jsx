import { useState } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";

function PublishRequest() {
  const [form, setForm] = useState({
    start_point: "",
    end_point: "",
    date_trajet: "",        // format: YYYY-MM-DD
    start_time: "",         // format: HH:MM
    end_time: "",           // format: HH:MM
    price_preference: "",   // 'FIXE' ou autre
    max_price: "",          // string ou number
  });

  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("access"); // JWT access token

    if (!token) {
      setMessage("Vous devez être connecté pour publier une demande.");
      return;
    }

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/offers/requests/create/",
        form,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      setMessage("Demande publiée avec succès !");
      setForm({
        start_point: "",
        end_point: "",
        date_trajet: "",
        start_time: "",
        end_time: "",
        price_preference: "",
        max_price: "",
      });

    } catch (error) {
      console.error("Erreur de publication :", error.response?.data || error.message);
      setMessage("Erreur lors de la publication de la demande.");
    }
  };

  return (
    <>
      <Navbar />
      <div className="container mt-5">
        <h2>Publier une demande</h2>
        {message && <p className="mt-2 text-info">{message}</p>}
        <form onSubmit={handleSubmit} className="mt-4">
          <div className="mt-3">
            <label htmlFor="start_point" className="form-label">Point de départ</label>
            <input type="text" className="form-control" id="start_point" name="start_point" value={form.start_point} onChange={handleChange} />
          </div>
          <div className="mt-3">
            <label htmlFor="end_point" className="form-label">Point d'arrivée</label>
            <input type="text" className="form-control" id="end_point" name="end_point" value={form.end_point} onChange={handleChange} />
          </div>
          <div className="mt-3">
            <label htmlFor="date_trajet" className="form-label">Date du trajet (YYYY-MM-DD)</label>
            <input type="date" className="form-control" id="date_trajet" name="date_trajet" value={form.date_trajet} onChange={handleChange} />
          </div>
          <div className="mt-3">
            <label htmlFor="start_time" className="form-label">Heure de départ (HH:MM)</label>
            <input type="time" className="form-control" id="start_time" name="start_time" value={form.start_time} onChange={handleChange} />
          </div>
          <div className="mt-3">
            <label htmlFor="end_time" className="form-label">Heure d'arrivée (HH:MM)</label>
            <input type="time" className="form-control" id="end_time" name="end_time" value={form.end_time} onChange={handleChange} />
          </div>
          <div className="mt-3">
            <label htmlFor="price_preference" className="form-label">Préférence de prix (ex: FIXE)</label>
            <input type="text" className="form-control" id="price_preference" name="price_preference" value={form.price_preference} onChange={handleChange} />
          </div>
          <div className="mt-3">
            <label htmlFor="max_price" className="form-label">Prix max (si FIXE)</label>
            <input type="number" className="form-control" id="max_price" name="max_price" value={form.max_price} onChange={handleChange} />
          </div>
          <button type="submit" className="bg-black text-white px-4 py-2 mt-3 rounded">Publier la demande</button>
        </form>
      </div>
    </>
  );
}

export default PublishRequest;
