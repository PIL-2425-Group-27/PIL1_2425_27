import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ModifProfile = () => {
  // État pour les données du profil
  const [profileData, setProfileData] = useState({
    first_name: '',
    last_name: '',
    photo_profile: null,
    default_start_point: '',
    default_end_point: '',
    default_start_time: '',
    default_end_time: '',
    consent_tracking: false,
    theme_preference: 'light'
  });

  // États pour la gestion de l'interface
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState('');
  const [photoPreview, setPhotoPreview] = useState(null);

  // Configuration axios avec token (ajuste selon ton système d'auth)
  const getAuthHeaders = () => {
    const token = localStorage.getItem('access_token'); // ou selon ton système
    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'multipart/form-data'
    };
  };

  // Charger les données du profil au montage
  useEffect(() => {
    fetchProfile();
  }, []);

  // Récupérer les données actuelles du profil
  const fetchProfile = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://127.0.0.1:8000/accounts/profile/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      
      setProfileData(response.data);
      if (response.data.photo_profile) {
        setPhotoPreview(response.data.photo_profile);
      }
    } catch (error) {
      console.error('Erreur lors du chargement du profil:', error);
      if (error.response?.status === 401) {
        // Rediriger vers login si token invalide
        window.location.href = '/login';
      }
    } finally {
      setLoading(false);
    }
  };

  // Gérer les changements des champs input
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setProfileData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    
    // Effacer l'erreur du champ modifié
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: null }));
    }
  };

  // Gérer le changement de photo
  const handlePhotoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Vérification de la taille (5MB max selon ton serializer)
      if (file.size > 5 * 1024 * 1024) {
        setErrors(prev => ({ 
          ...prev, 
          photo_profile: 'Le fichier ne doit pas dépasser 5 Mo.' 
        }));
        return;
      }

      setProfileData(prev => ({ ...prev, photo_profile: file }));
      
      // Créer un aperçu
      const reader = new FileReader();
      reader.onload = (e) => setPhotoPreview(e.target.result);
      reader.readAsDataURL(file);
    }
  };

  // Soumettre les modifications
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setErrors({});
    setSuccess('');

    try {
      // Créer FormData pour supporter l'upload de fichier
      const formData = new FormData();
      
      // Ajouter tous les champs
      Object.keys(profileData).forEach(key => {
        if (profileData[key] !== null && profileData[key] !== '') {
          if (key === 'photo_profile' && profileData[key] instanceof File) {
            formData.append(key, profileData[key]);
          } else if (key !== 'photo_profile') {
            formData.append(key, profileData[key]);
          }
        }
      });

      const response = await axios.patch(
        'http://127.0.0.1:8000/accounts/profile/',
        formData,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'multipart/form-data'
          }
        }
      );

      setSuccess('Profil mis à jour with succès !');
      // Actualiser les données avec la réponse
      setProfileData(response.data);
      
      // Faire disparaître le message après 3 secondes
      setTimeout(() => setSuccess(''), 3000);

    } catch (error) {
      console.error('Erreur lors de la mise à jour:', error);
      
      if (error.response?.data) {
        // Gérer les erreurs de validation du backend
        setErrors(error.response.data);
      } else {
        setErrors({ general: 'Une erreur est survenue lors de la mise à jour.' });
      }
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Modifier le Profil</h2>
      
      {/* Messages de succès et d'erreur */}
      {success && (
        <div className="mb-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded">
          {success}
        </div>
      )}
      
      {errors.general && (
        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {errors.general}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Photo de profil */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Photo de profil
          </label>
          <div className="flex items-center space-x-4">
            {photoPreview && (
              <img
                src={photoPreview}
                alt="Aperçu"
                className="w-20 h-20 rounded-full object-cover"
              />
            )}
            <input
              type="file"
              accept="image/*"
              onChange={handlePhotoChange}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />
          </div>
          {errors.photo_profile && (
            <p className="mt-1 text-sm text-red-600">{errors.photo_profile}</p>
          )}
        </div>

        {/* Prénom et Nom */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Prénom
            </label>
            <input
              type="text"
              name="first_name"
              value={profileData.first_name}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Votre prénom"
            />
            {errors.first_name && (
              <p className="mt-1 text-sm text-red-600">{errors.first_name}</p>
            )}
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nom
            </label>
            <input
              type="text"
              name="last_name"
              value={profileData.last_name}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Votre nom"
            />
            {errors.last_name && (
              <p className="mt-1 text-sm text-red-600">{errors.last_name}</p>
            )}
          </div>
        </div>

        {/* Points par défaut */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Point de départ par défaut
            </label>
            <input
              type="text"
              name="default_start_point"
              value={profileData.default_start_point}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Adresse de départ"
            />
            {errors.default_start_point && (
              <p className="mt-1 text-sm text-red-600">{errors.default_start_point}</p>
            )}
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Point d'arrivée par défaut
            </label>
            <input
              type="text"
              name="default_end_point"
              value={profileData.default_end_point}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Adresse d'arrivée"
            />
            {errors.default_end_point && (
              <p className="mt-1 text-sm text-red-600">{errors.default_end_point}</p>
            )}
          </div>
        </div>

        {/* Heures par défaut */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Heure de départ par défaut
            </label>
            <input
              type="time"
              name="default_start_time"
              value={profileData.default_start_time}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            {errors.default_start_time && (
              <p className="mt-1 text-sm text-red-600">{errors.default_start_time}</p>
            )}
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Heure d'arrivée par défaut
            </label>
            <input
              type="time"
              name="default_end_time"
              value={profileData.default_end_time}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            {errors.default_end_time && (
              <p className="mt-1 text-sm text-red-600">{errors.default_end_time}</p>
            )}
          </div>
        </div>

        {/* Préférences */}
        <div className="space-y-4">
          <div className="flex items-center">
            <input
              type="checkbox"
              name="consent_tracking"
              checked={profileData.consent_tracking}
              onChange={handleInputChange}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label className="ml-2 block text-sm text-gray-700">
              Autoriser le suivi GPS
            </label>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Thème
            </label>
            <select
              name="theme_preference"
              value={profileData.theme_preference}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="light">Clair</option>
              <option value="dark">Sombre</option>
              <option value="auto">Automatique</option>
            </select>
          </div>
        </div>

        {/* Boutons */}
        <div className="flex justify-end space-x-4">
          <button
            type="button"
            onClick={() => window.history.back()}
            className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Annuler
          </button>
          
          <button
            type="submit"
            disabled={saving}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {saving ? 'Enregistrement...' : 'Enregistrer'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ModifProfile;