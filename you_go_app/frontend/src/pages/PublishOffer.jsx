import { useState } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";

function PublishOffer() {
    const [form, setForm] = useState({
        start_point: "",
        end_point: "",
        date_trajet: "",
        start_time: "",
        end_time: "",
        seats_available: "",
        price_type: "DYNAMIQUE",
        price: "",
        description: "",
        use_custom_vehicle_info: false,
        custom_vehicle_brand: "",
        custom_vehicle_model: "",
        custom_vehicle_plate: "",
        custom_vehicle_seats: ""
    });

    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});
    const [successMessage, setSuccessMessage] = useState("");

    // Configuration API
    const API_BASE_URL = 'http://127.0.0.1:8000/offers/create/';

    // Configuration axios avec intercepteur pour l'authentification
    const apiClient = axios.create({
        baseURL: reponse,
        headers: {
            'Content-Type': 'application/json',
        },
    });

    // Intercepteur pour ajouter le token d'authentification
    apiClient.interceptors.request.use(
        (config) => {
            const token = localStorage.getItem('authToken');
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        },
        (error) => {
            return Promise.reject(error);
        }
    );

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        
        setForm({ 
            ...form, 
            [name]: type === 'checkbox' ? checked : value
        });

        // Effacer l'erreur spécifique du champ modifié
        if (errors[name]) {
            setErrors({ ...errors, [name]: "" });
        }
    };

    const validateForm = () => {
        const newErrors = {};

        // Validations basiques
        if (!form.start_point.trim()) {
            newErrors.start_point = "Le point de départ est requis";
        }
        if (!form.end_point.trim()) {
            newErrors.end_point = "Le point d'arrivée est requis";
        }
        if (!form.date_trajet) {
            newErrors.date_trajet = "La date du trajet est requise";
        }
        if (!form.start_time) {
            newErrors.start_time = "L'heure de départ est requise";
        }
        if (!form.end_time) {
            newErrors.end_time = "L'heure d'arrivée est requise";
        }
        if (!form.seats_available || parseInt(form.seats_available) < 1) {
            newErrors.seats_available = "Le nombre de places doit être au moins 1";
        }

        // Validation du prix si type FIXE
        if (form.price_type === "FIXE" && (!form.price || parseFloat(form.price) <= 0)) {
            newErrors.price = "Le prix est requis pour le type FIXE";
        }

        // Validation des heures
        if (form.start_time && form.end_time && form.start_time >= form.end_time) {
            newErrors.end_time = "L'heure d'arrivée doit être après l'heure de départ";
        }

        // Validation des infos véhicule personnalisé
        if (form.use_custom_vehicle_info) {
            if (!form.custom_vehicle_brand.trim()) {
                newErrors.custom_vehicle_brand = "La marque du véhicule est requise";
            }
            if (!form.custom_vehicle_model.trim()) {
                newErrors.custom_vehicle_model = "Le modèle du véhicule est requis";
            }
            if (!form.custom_vehicle_seats || parseInt(form.custom_vehicle_seats) < 1) {
                newErrors.custom_vehicle_seats = "Le nombre de places du véhicule est requis";
            }
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const createOffer = async (offerData) => {
        try {
            const response = await apiClient.post('/create/', offerData);
            return {
                success: true,
                data: response.data,
                message: 'Offre créée avec succès'
            };
        } catch (error) {
            console.error('Erreur API:', error);
            return {
                success: false,
                error: error.response?.data || error.message,
                message: 'Erreur lors de la création de l\'offre'
            };
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // Réinitialiser les messages
        setSuccessMessage("");
        setErrors({});

        // Valider le formulaire
        if (!validateForm()) {
            return;
        }

        setLoading(true);

        try {
            // Préparer les données pour l'API
            const offerData = {
                start_point: form.start_point.trim(),
                end_point: form.end_point.trim(),
                date_trajet: form.date_trajet,
                start_time: form.start_time,
                end_time: form.end_time,
                seats_available: parseInt(form.seats_available),
                price_type: form.price_type,
                description: form.description.trim(),
                use_custom_vehicle_info: form.use_custom_vehicle_info
            };

            // Ajouter le prix si nécessaire
            if (form.price_type === "FIXE") {
                offerData.price = parseFloat(form.price);
            }

            // Ajouter les infos véhicule personnalisé si nécessaire
            if (form.use_custom_vehicle_info) {
                offerData.custom_vehicle_brand = form.custom_vehicle_brand.trim();
                offerData.custom_vehicle_model = form.custom_vehicle_model.trim();
                offerData.custom_vehicle_plate = form.custom_vehicle_plate.trim();
                offerData.custom_vehicle_seats = parseInt(form.custom_vehicle_seats);
            }

            console.log("Données envoyées:", offerData);

            // Appel API
            const result = await createOffer(offerData);

            if (result.success) {
                setSuccessMessage(result.message);
                // Réinitialiser le formulaire
                setForm({
                    start_point: "",
                    end_point: "",
                    date_trajet: "",
                    start_time: "",
                    end_time: "",
                    seats_available: "",
                    price_type: "DYNAMIQUE",
                    price: "",
                    description: "",
                    use_custom_vehicle_info: false,
                    custom_vehicle_brand: "",
                    custom_vehicle_model: "",
                    custom_vehicle_plate: "",
                    custom_vehicle_seats: ""
                });
                
                // Scroll vers le haut pour voir le message de succès
                window.scrollTo({ top: 0, behavior: 'smooth' });
                
                // Optionnel: rediriger vers une autre page après succès
                // setTimeout(() => {
                //     window.location.href = '/mes-offres';
                // }, 3000);
            } else {
                // Gérer les erreurs de validation du backend
                if (result.error && typeof result.error === 'object') {
                    setErrors(result.error);
                } else {
                    setErrors({ general: result.message || "Une erreur est survenue" });
                }
            }
        } catch (error) {
            console.error("Erreur lors de la soumission:", error);
            setErrors({ general: "Erreur de connexion au serveur" });
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <Navbar />
            <div className="container mt-5">
                <h2 className="mb-4">Publier une offre de covoiturage</h2>
                
                {/* Messages de succès */}
                {successMessage && (
                    <div className="alert alert-success alert-dismissible fade show" role="alert">
                        <i className="fas fa-check-circle me-2"></i>
                        {successMessage}
                        <button 
                            type="button" 
                            className="btn-close" 
                            onClick={() => setSuccessMessage("")}
                        ></button>
                    </div>
                )}
                
                {/* Erreurs générales */}
                {errors.general && (
                    <div className="alert alert-danger alert-dismissible fade show" role="alert">
                        <i className="fas fa-exclamation-triangle me-2"></i>
                        {errors.general}
                        <button 
                            type="button" 
                            className="btn-close" 
                            onClick={() => setErrors({ ...errors, general: "" })}
                        ></button>
                    </div>
                )}

                <form onSubmit={handleSubmit} className="mt-4">
                    <div className="row">
                        {/* Point de départ */}
                        <div className="col-md-6 mt-3">
                            <label htmlFor="start_point" className="form-label">
                                Point de départ <span className="text-danger">*</span>
                            </label>
                            <input 
                                type="text" 
                                className={`form-control ${errors.start_point ? 'is-invalid' : ''}`}
                                id="start_point"
                                name="start_point"
                                value={form.start_point}
                                onChange={handleChange}
                                placeholder="Ex: Cotonou, Place de l'Étoile Rouge"
                                disabled={loading}
                            />
                            {errors.start_point && <div className="invalid-feedback">{errors.start_point}</div>}
                        </div>

                        {/* Point d'arrivée */}
                        <div className="col-md-6 mt-3">
                            <label htmlFor="end_point" className="form-label">
                                Point d'arrivée <span className="text-danger">*</span>
                            </label>
                            <input 
                                type="text" 
                                className={`form-control ${errors.end_point ? 'is-invalid' : ''}`}
                                id="end_point"
                                name="end_point"
                                value={form.end_point}
                                onChange={handleChange}
                                placeholder="Ex: Porto-Novo, Gare routière"
                                disabled={loading}
                            />
                            {errors.end_point && <div className="invalid-feedback">{errors.end_point}</div>}
                        </div>
                    </div>

                    <div className="row">
                        {/* Date du trajet */}
                        <div className="col-md-4 mt-3">
                            <label htmlFor="date_trajet" className="form-label">
                                Date du trajet <span className="text-danger">*</span>
                            </label>
                            <input 
                                type="date" 
                                className={`form-control ${errors.date_trajet ? 'is-invalid' : ''}`}
                                id="date_trajet"
                                name="date_trajet"
                                value={form.date_trajet}
                                onChange={handleChange}
                                min={new Date().toISOString().split('T')[0]}
                                disabled={loading}
                            />
                            {errors.date_trajet && <div className="invalid-feedback">{errors.date_trajet}</div>}
                        </div>

                        {/* Heure de départ */}
                        <div className="col-md-4 mt-3">
                            <label htmlFor="start_time" className="form-label">
                                Heure de départ <span className="text-danger">*</span>
                            </label>
                            <input 
                                type="time" 
                                className={`form-control ${errors.start_time ? 'is-invalid' : ''}`}
                                id="start_time"
                                name="start_time"
                                value={form.start_time}
                                onChange={handleChange}
                                disabled={loading}
                            />
                            {errors.start_time && <div className="invalid-feedback">{errors.start_time}</div>}
                        </div>

                        {/* Heure d'arrivée */}
                        <div className="col-md-4 mt-3">
                            <label htmlFor="end_time" className="form-label">
                                Heure d'arrivée <span className="text-danger">*</span>
                            </label>
                            <input 
                                type="time" 
                                className={`form-control ${errors.end_time ? 'is-invalid' : ''}`}
                                id="end_time"
                                name="end_time"
                                value={form.end_time}
                                onChange={handleChange}
                                disabled={loading}
                            />
                            {errors.end_time && <div className="invalid-feedback">{errors.end_time}</div>}
                        </div>
                    </div>

                    <div className="row">
                        {/* Nombre de places */}
                        <div className="col-md-6 mt-3">
                            <label htmlFor="seats_available" className="form-label">
                                Nombre de places disponibles <span className="text-danger">*</span>
                            </label>
                            <input 
                                type="number" 
                                className={`form-control ${errors.seats_available ? 'is-invalid' : ''}`}
                                id="seats_available"
                                name="seats_available"
                                value={form.seats_available}
                                onChange={handleChange}
                                min="1"
                                max="8"
                                placeholder="Ex: 3"
                                disabled={loading}
                            />
                            {errors.seats_available && <div className="invalid-feedback">{errors.seats_available}</div>}
                        </div>

                        {/* Type de prix */}
                        <div className="col-md-6 mt-3">
                            <label htmlFor="price_type" className="form-label">
                                Type de prix <span className="text-danger">*</span>
                            </label>
                            <select 
                                className={`form-control ${errors.price_type ? 'is-invalid' : ''}`}
                                id="price_type"
                                name="price_type"
                                value={form.price_type}
                                onChange={handleChange}
                                disabled={loading}
                            >
                                <option value="DYNAMIQUE">Prix calculé automatiquement</option>
                                <option value="FIXE">Prix fixé par moi</option>
                            </select>
                            {errors.price_type && <div className="invalid-feedback">{errors.price_type}</div>}
                        </div>
                    </div>

                    {/* Prix fixe (affiché seulement si FIXE est sélectionné) */}
                    {form.price_type === "FIXE" && (
                        <div className="row">
                            <div className="col-md-6 mt-3">
                                <label htmlFor="price" className="form-label">
                                    Prix par personne (FCFA) <span className="text-danger">*</span>
                                </label>
                                <input 
                                    type="number" 
                                    className={`form-control ${errors.price ? 'is-invalid' : ''}`}
                                    id="price"
                                    name="price"
                                    value={form.price}
                                    onChange={handleChange}
                                    min="0"
                                    step="50"
                                    placeholder="Ex: 1000"
                                    disabled={loading}
                                />
                                {errors.price && <div className="invalid-feedback">{errors.price}</div>}
                            </div>
                        </div>
                    )}

                    {/* Utiliser des informations de véhicule personnalisées */}
                    <div className="mt-4">
                        <div className="card">
                            <div className="card-body">
                                <div className="form-check">
                                    <input 
                                        type="checkbox" 
                                        className="form-check-input"
                                        id="use_custom_vehicle_info"
                                        name="use_custom_vehicle_info"
                                        checked={form.use_custom_vehicle_info}
                                        onChange={handleChange}
                                        disabled={loading}
                                    />
                                    <label className="form-check-label" htmlFor="use_custom_vehicle_info">
                                        <strong>Saisir les informations du véhicule manuellement</strong>
                                    </label>
                                </div>

                                {/* Informations véhicule personnalisées */}
                                {form.use_custom_vehicle_info && (
                                    <div className="row mt-3">
                                        <div className="col-md-6 mt-2">
                                            <label htmlFor="custom_vehicle_brand" className="form-label">
                                                Marque du véhicule <span className="text-danger">*</span>
                                            </label>
                                            <input 
                                                type="text" 
                                                className={`form-control ${errors.custom_vehicle_brand ? 'is-invalid' : ''}`}
                                                id="custom_vehicle_brand"
                                                name="custom_vehicle_brand"
                                                value={form.custom_vehicle_brand}
                                                onChange={handleChange}
                                                placeholder="Ex: Toyota"
                                                disabled={loading}
                                            />
                                            {errors.custom_vehicle_brand && <div className="invalid-feedback">{errors.custom_vehicle_brand}</div>}
                                        </div>

                                        <div className="col-md-6 mt-2">
                                            <label htmlFor="custom_vehicle_model" className="form-label">
                                                Modèle du véhicule <span className="text-danger">*</span>
                                            </label>
                                            <input 
                                                type="text" 
                                                className={`form-control ${errors.custom_vehicle_model ? 'is-invalid' : ''}`}
                                                id="custom_vehicle_model"
                                                name="custom_vehicle_model"
                                                value={form.custom_vehicle_model}
                                                onChange={handleChange}
                                                placeholder="Ex: Corolla"
                                                disabled={loading}
                                            />
                                            {errors.custom_vehicle_model && <div className="invalid-feedback">{errors.custom_vehicle_model}</div>}
                                        </div>

                                        <div className="col-md-6 mt-2">
                                            <label htmlFor="custom_vehicle_plate" className="form-label">
                                                Plaque d'immatriculation
                                            </label>
                                            <input 
                                                type="text" 
                                                className="form-control"
                                                id="custom_vehicle_plate"
                                                name="custom_vehicle_plate"
                                                value={form.custom_vehicle_plate}
                                                onChange={handleChange}
                                                placeholder="Ex: AB-123-CD"
                                                disabled={loading}
                                            />
                                        </div>

                                        <div className="col-md-6 mt-2">
                                            <label htmlFor="custom_vehicle_seats" className="form-label">
                                                Capacité totale du véhicule <span className="text-danger">*</span>
                                            </label>
                                            <input 
                                                type="number" 
                                                className={`form-control ${errors.custom_vehicle_seats ? 'is-invalid' : ''}`}
                                                id="custom_vehicle_seats"
                                                name="custom_vehicle_seats"
                                                value={form.custom_vehicle_seats}
                                                onChange={handleChange}
                                                min="2"
                                                max="9"
                                                placeholder="Ex: 5"
                                                disabled={loading}
                                            />
                                            {errors.custom_vehicle_seats && <div className="invalid-feedback">{errors.custom_vehicle_seats}</div>}
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Description */}
                    <div className="mt-3">
                        <label htmlFor="description" className="form-label">Conditions et remarques</label>
                        <textarea 
                            className="form-control"
                            id="description"
                            name="description"
                            value={form.description}
                            onChange={handleChange}
                            rows="3"
                            placeholder="Ex: Non fumeur, départ précis à l'heure, bagage léger uniquement..."
                            disabled={loading}
                        />
                    </div>

                    {/* Bouton de soumission */}
                    <div className="mt-4 mb-5">
                        <button 
                            type="submit" 
                            className="btn btn-success btn-lg px-5 py-2"
                            disabled={loading}
                        >
                            {loading ? (
                                <>
                                    <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                    Publication en cours...
                                </>
                            ) : (
                                <>
                                    <i className="fas fa-paper-plane me-2"></i>
                                    Publier l'offre
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </>
    );
}

export default PublishOffer;