import { useEffect, useState } from "react";
import Button from "../components/Button";
import HistoryItem from "../components/HistoryItem";
import Return from "../components/Return";
import Title from "../components/Title";
import Loading from "./Loading";
import axios from "axios";

function History() {
    let theme = false
    const [statut, setStatut] = useState('PASSAGER')
    const action = statut === 'passager' ? 'Publier une demande' : 'Publier une offre';
    const link = statut === 'passager' ? '/PublishRequest' : '/PublishOffer';
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState()
    const [labels, setLabels] = useState([])
    const [total_km, setTotal_km] = useState([])
    const [total_reviews, setTotal_reviews] = useState(0)
    const [total_trajets, setTotal_trajets] = useState([])
    const [reviews_given, setReviewsGiven] = useState([]);
    const [stats, setStats] = useState([]);

    const token = localStorage.getItem("authToken");
    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const res = await axios.get("http://localhost:8000/reviews/stats/", {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });

                const labels = res.data.labels;
                const total_km = res.data.total_km;
                const total_trajets = res.data.total_trajets;
                const reviews_given = res.data.reviews_given;

                const structuredStats = labels.map((label, i) => ({
                    label,
                    km: total_km[i],
                    trajets: total_trajets[i],
                    reviews: reviews_given[i],
                }));

                setStats(structuredStats);

                // Other existing setState calls
                setLabels(labels);
                setTotal_km(total_km);
                setTotal_reviews(res.data.total_reviews_received);
                setTotal_trajets(total_trajets);
            } catch (error) {
                console.error("Failed to fetch user:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchHistory();
    }, []);


    if (loading) {
        return <Loading />;
    }


    return (
        <>
            <div
                className={`relative w-full h-screen ${theme == false ? 'bg-white' : 'bg-[#2d2d2d] text-white'} flex flex-col items-center justify-evenly py-10`}
            >
                <Return link={'/'} theme={theme} />
                <Title content={'Historique'} floating={true} />
                <div className="w-full h-full flex flex-col items-center justify-start py-[8vh] gap-[1vh] ">
                    {stats.map(({ label, km, trajets, reviews }) => (
                        <HistoryItem theme={theme} label={label} km={km} trajets = {trajets} reviews ={reviews}/>
                    ))}

                </div>
                <div className="fixed bottom-[8vh] right-[8vw] w-[8vh] aspect-square rounded-full bg-red-400 flex flex-col items-center justify-center">
                    <img
                        className="w-1/2"
                        src="./src/assets/icons/delete2.svg" />
                </div>
            </div>
        </>
    );
}

export default History;