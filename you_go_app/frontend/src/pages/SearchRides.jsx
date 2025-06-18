import React, { useState, useEffect } from "react";
import axios from "axios";

import Navbar from "../components/Navbar";
import Return from "../components/Return";
import SearchBar from "../components/SearchBar";
import Title from "../components/Title";

function SearchRides() {
  let theme = false;

  // États pour les critères de recherche étendus
  const [filters, setFilters] = useState({
    start_point: "",
    end_point: "",
    date_trajet: "",
    start_time: "",
    end_time: "",
    price_type: "",
    max_price: "",
    seats_available: "",
    is_today: false,
    is_upcoming: false,
    ordering: ""
  });

  // État pour stocker les résultats de la recherche
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState(null);

  // Fonction appelée pour mettre à jour les filtres depuis SearchBar
  const handleFilterChange = (field, value) => {
    setFilters(prev => ({ ...prev, [field]: value }));
  };

  // Fonction pour réinitialiser les filtres
  const resetFilters = () => {
    setFilters({
      start_point: "",
      end_point: "",
      date_trajet: "",
      start_time: "",
      end_time: "",
      price_type: "",
      max_price: "",
      seats_available: "",
      is_today: false,
      is_upcoming: false,
      ordering: ""
    });
    setResults([]);
  };

  // Fonction pour lancer la recherche
  const searchRides = async (page = 1) => {
    setLoading(true);
    setError(null);
    try {
      // Construire la query string à partir de filters
      const params = new URLSearchParams();

      // Ajouter les paramètres non vides
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== "" && value !== false && value !== null) {
          params.append(key, value);
        }
      });

      // Ajouter la pagination
      if (page > 1) {
        params.append("page", page);
      }

      // URL vers l'endpoint de recherche de l'API
      const url = `http://127.0.0.1:8000/offers/search/?${params.toString()}`;

      const response = await axios.get(url);
      
      // Gérer la pagination si elle existe dans la réponse
      if (response.data.pagination) {
        setPagination(response.data.pagination);
        setResults(response.data.results);
      } else {
        setResults(response.data);
        setPagination(null);
      }
    } catch (err) {
      console.error("Erreur lors de la recherche:", err);
      setError(err.response?.data?.detail || "Erreur lors de la recherche");
    } finally {
      setLoading(false);
    }
  };

  // Fonction pour charger la page suivante
  const loadNextPage = () => {
    if (pagination && pagination.current_page < pagination.total_pages) {
      searchRides(pagination.current_page + 1);
    }
  };

  // Fonction pour charger la page précédente
  const loadPrevPage = () => {
    if (pagination && pagination.current_page > 1) {
      searchRides(pagination.current_page - 1);
    }
  };

  // Fonction pour formater le prix
  const formatPrice = (price, priceType) => {
    if (priceType === 'GRATUIT') return 'Gratuit';
    if (!price) return 'À discuter';
    return `${price} FCFA`;
  };

  // Fonction pour formater la date
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <>
      <div
        className={`w-full min-h-screen flex flex-col ${
          theme === false ? "bg-white" : "bg-[#2d2d2d] text-white"
        } items-center`}
      >
        <Return theme={theme} />
        <Title content={"Rechercher un covoiturage"} floating={true} />

        {/* Formulaire de recherche étendu */}
        <div className="w-full max-w-4xl px-4 mt-6">
          <div className="bg-gray-50 p-6 rounded-lg shadow-md">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {/* Point de départ */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Point de départ
                </label>
                <input
                  type="text"
                  value={filters.start_point}
                  onChange={(e) => handleFilterChange('start_point', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Ex: Cotonou, Dantokpa..."
                />
              </div>

              {/* Point d'arrivée */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Point d'arrivée
                </label>
                <input
                  type="text"
                  value={filters.end_point}
                  onChange={(e) => handleFilterChange('end_point', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Ex: Porto-Novo, Parakou..."
                />
              </div>

              {/* Date du trajet */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Date du trajet
                </label>
                <input
                  type="date"
                  value={filters.date_trajet}
                  onChange={(e) => handleFilterChange('date_trajet', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              {/* Heure de départ */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Heure de départ (après)
                </label>
                <input
                  type="time"
                  value={filters.start_time}
                  onChange={(e) => handleFilterChange('start_time', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              {/* Prix maximum */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Prix maximum (FCFA)
                </label>
                <input
                  type="number"
                  value={filters.max_price}
                  onChange={(e) => handleFilterChange('max_price', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Ex: 5000"
                />
              </div>

              {/* Nombre de places minimum */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Places disponibles (min)
                </label>
                <input
                  type="number"
                  value={filters.seats_available}
                  onChange={(e) => handleFilterChange('seats_available', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  min="1"
                  max="8"
                />
              </div>
            </div>

            {/* Options rapides */}
            <div className="mt-4 flex flex-wrap gap-4">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={filters.is_today}
                  onChange={(e) => handleFilterChange('is_today', e.target.checked)}
                  className="mr-2"
                />
                Trajets d'aujourd'hui
              </label>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={filters.is_upcoming}
                  onChange={(e) => handleFilterChange('is_upcoming', e.target.checked)}
                  className="mr-2"
                />
                Trajets à venir
              </label>
            </div>

            {/* Tri */}
            <div className="mt-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Trier par
              </label>
              <select
                value={filters.ordering}
                onChange={(e) => handleFilterChange('ordering', e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Par défaut</option>
                <option value="price">Prix croissant</option>
                <option value="-price">Prix décroissant</option>
                <option value="date">Date croissante</option>
                <option value="-date">Date décroissante</option>
                <option value="start_time">Heure de départ</option>
              </select>
            </div>

            {/* Boutons d'action */}
            <div className="mt-6 flex gap-3">
              <button
                onClick={() => searchRides(1)}
                disabled={loading}
                className="px-6 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? "Recherche..." : "Rechercher"}
              </button>
              <button
                onClick={resetFilters}
                className="px-6 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 transition-colors"
              >
                Réinitialiser
              </button>
            </div>
          </div>
        </div>

        {/* Résultats de recherche */}
        <div className="w-full max-w-4xl px-4 mt-6 pb-6">
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          {results.length === 0 && !loading && !error && (
            <div className="text-center py-8">
              <p className="text-gray-500">Aucun covoiturage trouvé. Essayez de modifier vos critères de recherche.</p>
            </div>
          )}

          {/* Liste des résultats */}
          <div className="space-y-4">
            {results.map((ride) => (
              <div key={ride.id} className="bg-white border border-gray-200 rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {/* Informations du trajet */}
                  <div className="md:col-span-2">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {ride.start_point} → {ride.end_point}
                      </h3>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        ride.price_type === 'GRATUIT' 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-blue-100 text-blue-800'
                      }`}>
                        {formatPrice(ride.price, ride.price_type)}
                      </span>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
                      <div>
                        <p><strong>Date:</strong> {formatDate(ride.date_trajet)}</p>
                        <p><strong>Départ:</strong> {ride.start_time}</p>
                      </div>
                      <div>
                        <p><strong>Arrivée:</strong> {ride.end_time}</p>
                        <p><strong>Places libres:</strong> {ride.seats_available}</p>
                      </div>
                    </div>

                    {ride.description && (
                      <p className="mt-3 text-sm text-gray-600 italic">
                        "{ride.description}"
                      </p>
                    )}

                    {/* Informations du véhicule */}
                    {ride.vehicle_info && (
                      <div className="mt-3 text-sm text-gray-600">
                        <p><strong>Véhicule:</strong> {ride.vehicle_info.brand} {ride.vehicle_info.model}</p>
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex flex-col justify-center space-y-2">
                    <button className="w-full px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 transition-colors">
                      Réserver
                    </button>
                    <button className="w-full px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 transition-colors">
                      Voir détails
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Pagination */}
          {pagination && (
            <div className="mt-6 flex justify-center items-center space-x-4">
              <button
                onClick={loadPrevPage}
                disabled={pagination.current_page === 1}
                className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-400 transition-colors"
              >
                Précédent
              </button>
              
              <span className="text-sm text-gray-600">
                Page {pagination.current_page} sur {pagination.total_pages} 
                ({pagination.total_items} résultats)
              </span>
              
              <button
                onClick={loadNextPage}
                disabled={pagination.current_page === pagination.total_pages}
                className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-400 transition-colors"
              >
                Suivant
              </button>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default SearchRides;