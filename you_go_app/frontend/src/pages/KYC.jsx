import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ArrowBack from '../assets/icons/arrow_back.svg'; // Corrige le chemin selon ton arborescence

const KYC = () => {
  const navigate = useNavigate();

  const [fullName, setFullName] = useState('');
  const [idPhoto, setIdPhoto] = useState(null);
  const [selfie, setSelfie] = useState(null);

  const handleGoBack = () => {
    navigate('/profile'); // Assure-toi que "/profile" est bien défini dans ton routeur
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log({
      fullName,
      idPhoto,
      selfie,
    });
    // Tu pourras envoyer au backend ici avec fetch/axios
  };

  return (
    <div className="p-4">
      {/* Flèche de retour */}
      <img
        src={ArrowBack}
        alt="Retour"
        className="w-6 h-6 cursor-pointer mb-4"
        onClick={handleGoBack}
      />

      <h2 className="text-xl font-bold mb-4 text-[#fad02c] ">Vérification KYC</h2>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        {/* Nom complet */}
        <div>
          <label className="block mb-1">Nom complet</label>
          <input
            type="text"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            className="border rounded p-2 w-full"
            required
          />
        </div>

        {/* Carte d'identité */}
        <div>
          <label className="block mb-1">Photo de la carte d'identité</label>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setIdPhoto(e.target.files[0])}
            className="border rounded p-2 w-full"
            required
          />
        </div>

        {/* Selfie */}
        <div>
          <label className="block mb-1">Votre photo (selfie)</label>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setSelfie(e.target.files[0])}
            className="border rounded p-2 w-full"
            required
          />
        </div>

        {/* Bouton soumettre */}
        <button
          type="submit"
          className="bg-yellow-400 text-black py-2 px-4 rounded hover:bg-yellow-500 transition"
        >
          Soumettre
        </button>
      </form>
    </div>
  );
};

export default KYC;
