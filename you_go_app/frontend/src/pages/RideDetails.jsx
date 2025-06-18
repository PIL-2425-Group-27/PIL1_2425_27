import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import Navbar from "../components/Navbar";

function RideDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [ride, setRide] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [bookingLoading, setBookingLoading] = useState(false);

  useEffect(() => {
    async function fetchRide() {
      if (!id) {
        setError("ID du trajet manquant");
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);
      
      try {
        const response = await axios.get(`http://127.0.0.1:8000/offers/${id}/`);
        setRide(response.data);
      } catch (err) {
        console.error("Erreur lors du chargement:", err);
        if (err.response?.status === 404) {
          setError("Trajet non trouvé");
        } else if (err.response?.status === 500) {
          setError("Erreur serveur. Veuillez réessayer plus tard.");
        } else {
          setError("Erreur lors du chargement des détails");
        }
      } finally {
        setLoading(false);
      }
    }
    
    fetchRide();
  }, [id]);

  const handleBooking = async () => {
    if (!ride || ride.seats_available <= 0) {
      alert("Aucune place disponible pour ce trajet");
      return;
    }

    setBookingLoading(true);
    try {
      // Remplacez par votre endpoint de réservation
      const response = await axios.post(`http://127.0.0.1:8000/offers/requests/create`, {
        offer_id: id,
        // Ajoutez d'autres données nécessaires pour la réservation
      });
      
      if (response.status === 201) {
        alert("Réservation effectuée avec succès !");
        // Mettre à jour le nombre de places disponibles
        setRide(prev => ({
          ...prev,
          seats_available: prev.seats_available - 1
        }));
      }
    } catch (err) {
      console.error("Erreur lors de la réservation:", err);
      if (err.response?.status === 400) {
        alert("Impossible de réserver ce trajet. Vérifiez les informations.");
      } else {
        alert("Erreur lors de la réservation. Veuillez réessayer.");
      }
    } finally {
      setBookingLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return "N/A";
    try {
      return new Date(dateString).toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    } catch {
      return dateString;
    }
  };

  const formatTime = (timeString) => {
    if (!timeString) return "N/A";
    return timeString.slice(0, 5); // Format HH:MM
  };

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="flex justify-center items-center min-h-screen">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p>Chargement des détails du trajet...</p>
          </div>
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Navbar />
        <div className="flex justify-center items-center min-h-screen">
          <div className="text-center text-red-600">
            <p className="text-xl mb-4">{error}</p>
            <button 
              onClick={() => navigate(-1)}
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              Retour
            </button>
          </div>
        </div>
      </>
    );
  }

  if (!ride) {
    return (
      <>
        <Navbar />
        <div className="flex justify-center items-center min-h-screen">
          <div className="text-center">
            <p className="text-xl mb-4">Aucun trajet trouvé.</p>
            <button 
              onClick={() => navigate(-1)}
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              Retour
            </button>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <div className="container mx-auto px-4 py-8 max-w-2xl">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
            Détails du trajet
          </h1>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center border-b pb-2">
              <span className="font-semibold text-gray-600">Point de départ :</span>
              <span className="text-gray-800">{ride.start_point || "N/A"}</span>
            </div>
            
            <div className="flex justify-between items-center border-b pb-2">
              <span className="font-semibold text-gray-600">Point d'arrivée :</span>
              <span className="text-gray-800">{ride.end_point || "N/A"}</span>
            </div>
            
            <div className="flex justify-between items-center border-b pb-2">
              <span className="font-semibold text-gray-600">Date de départ :</span>
              <span className="text-gray-800">{formatDate(ride.date_trajet)}</span>
            </div>
            
            <div className="flex justify-between items-center border-b pb-2">
              <span className="font-semibold text-gray-600">Heure de départ :</span>
              <span className="text-gray-800">{formatTime(ride.start_time)}</span>
            </div>
            
            <div className="flex justify-between items-center border-b pb-2">
              <span className="font-semibold text-gray-600">Conducteur :</span>
              <span className="text-gray-800">{ride.driverName || ride.driver || "N/A"}</span>
            </div>
            
            <div className="flex justify-between items-center border-b pb-2">
              <span className="font-semibold text-gray-600">Places disponibles :</span>
              <span className={`font-bold ${ride.seats_available > 0 ? 'text-green-600' : 'text-red-600'}`}>
                {ride.seats_available}
              </span>
            </div>
            
            <div className="flex justify-between items-center border-b pb-2">
              <span className="font-semibold text-gray-600">Véhicule :</span>
              <span className="text-gray-800">{ride.vehiculesmodel || ride.vehicle_model || "N/A"}</span>
            </div>
            
            <div className="flex justify-between items-center border-b pb-2">
              <span className="font-semibold text-gray-600">Type de prix :</span>
              <span className="text-gray-800">{ride.price_type || "N/A"}</span>
            </div>
            
            {ride.price && (
              <div className="flex justify-between items-center border-b pb-2">
                <span className="font-semibold text-gray-600">Prix :</span>
                <span className="text-gray-800 font-bold">{ride.price} FCFA</span>
              </div>
            )}
            
            <div className="flex justify-between items-center border-b pb-2">
              <span className="font-semibold text-gray-600">Note du conducteur :</span>
              <span className="text-gray-800">
                {ride.rating ? `${ride.rating}/5 ⭐` : "N/A"}
              </span>
            </div>
          </div>
          
          <div className="mt-8 flex gap-4">
            <button 
              onClick={handleBooking}
              disabled={bookingLoading || ride.seats_available <= 0}
              className={`flex-1 py-3 px-6 rounded-lg font-semibold transition-colors ${
                ride.seats_available > 0 && !bookingLoading
                  ? 'bg-green-500 hover:bg-green-600 text-white'
                  : 'bg-gray-400 text-gray-200 cursor-not-allowed'
              }`}
            >
              {bookingLoading 
                ? "Réservation en cours..." 
                : ride.seats_available > 0 
                  ? "Réserver ce trajet" 
                  : "Complet"
              }
            </button>
            
            <button 
              onClick={() => navigate(-1)}
              className="px-6 py-3 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
            >
              Retour
            </button>
          </div>
        </div>
      </div>
    </>
  );
}

export default RideDetails;