import Navbar from "../components/Navbar";
function RideDetails() {
    const RideDetails = () => {
        const ride = {
            start_point: "",
            end_point: "",
            start_time: "",
            driverName: "",
            seats_available: "",
            vehiculesmodel: "",
            price_type: "",
            rating: "",
        };
    }
    return (
        <>
            <h1 className='text-green-400'>Ride details Page</h1>
            <Navbar/>
            <div className="max-w-xl mx-auto p-6 mt-10 bg-white rounded-2xl shadow-md border border-gray-200">
                <h2 className="text-2xl font-bold text-blue-600 mb-4">Détails du trajet</h2>
                <div className="mb-2">
                    <span className="font-semibold">Point de départ :</span> {ride.start_point}
                </div>
                 <div className="mb-2">
                    <span className="font-semibold">Point d'arrivée :</span> {ride.end_point}
                </div>
                 <div className="mb-2">
                    <span className="font-semibold">Date + Heure de départ :</span> {ride.start_time}
                </div>
                 <div className="mb-2">
                    <span className="font-semibold">Nom du conducteur :</span> {ride.driverName}
                </div>
                 <div className="mb-2">
                    <span className="font-semibold">Nombres de places disponibles :</span> {ride.seats_available}
                </div>
                 <div className="mb-2">
                    <span className="font-semibold">Modèle du véhicule :</span> {ride.vehiculesmodel}
                </div>
                 <div className="mb-2">
                    <span className="font-semibold">Nature du prix :</span> {ride.price_type}
                </div>
                 <div className="mb-2">
                    <span className="font-semibold">Note du conducteur :</span> {ride.rating}
                </div>
                <button className="w-full bg-blue-600 text-white py-2 rounded-xl hover:bg-blue-700 transition">Réserver ce trajet</button>
            </div>
        </>
    );
}

export default RideDetails;