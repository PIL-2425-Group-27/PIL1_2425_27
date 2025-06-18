import { useState, useEffect } from 'react';
import Button from '../components/Button';
import Chart from '../components/Chart';
import Navbar from '../components/Navbar';
import Notification from '../components/Notification';
import axios from 'axios';
import Loading from './Loading';



function Home() {
    let theme = false
    const [statut, setStatut] = useState('PASSAGER')
    const action = statut === 'PASSAGER' ? 'Publier une demande' : 'Publier une offre';
    const link = statut === 'PASSAGER' ? '/PublishRequest' : '/PublishOffer';
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState()
    const [labels, setLabels] = useState([])
    const [total_km, setTotal_km] = useState([])
    const [total_reviews, setTotal_reviews] = useState(0)
    const [total_trajets, setTotal_trajets] = useState([])
    const [reviews_given, setReviewsGiven] = useState([]);
    const [stats, setStats] = useState([]);

    console.log(user);
    const token = localStorage.getItem("authToken");

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const res = await axios.get("http://localhost:8000/accounts/profile/", {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                setUser(res.data.first_name || res.data.username || "Utilisateur");
                setStatut(res.data.role || "passager"); // adapt to your serializer
            } catch (error) {
                console.error("Failed to fetch user:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchUser();
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
            <div className='relative w-full h-screen flex flex-col items-center animate-fade'>
                <div className='relative w-full  bg-[#ffcd74] rounded-b-3xl px-[4vw] pt-[4vh] pb-[4vw] flex flex-col justify-center gap-[3vh]'>
                    <Notification floating={true} icon={'./src/assets/icons/notification.svg'} link={'/Notifications'} theme={theme} />
                    <h1 className='text-3xl font-bold mt-8 text-white'>Bonjour {user}</h1>
                    <a
                        href='/SearchRides'
                        className='absolute w-[10vw] aspect-square mt-8 top-[4vh] right-[2vh] flex flex-col items-center justify-center'>
                        <img
                            className='w-full'
                            src="./src/assets/icons/search.svg"
                            alt="search" />
                    </a>
                    <Chart km={total_km} />
                </div>
                <div className='relative w-9/10 px-4 py-10 bg-[#e8e8e8] rounded-3xl mt-9 flex flex-col'>
                    <h1 className=' absolute top-0 left-0 text-xl font-semibold p-4'>Activité Récente</h1>
                    {stats.slice(0, 3).map(({ label, km, trajets, reviews }) => (
                        <div key={label} className='flex flex-col gap-1 mt-4 p-3 bg-white rounded-xl shadow-sm'>
                            <h2 className='text-lg font-semibold text-gray-700'>{label}</h2>
                            <p className='text-sm text-gray-600'>Kilomètres parcourus : <span className='font-medium'>{km} km</span></p>
                            <p className='text-sm text-gray-600'>Trajets effectués : <span className='font-medium'>{trajets}</span></p>
                            <p className='text-sm text-gray-600'>Avis donnés : <span className='font-medium'>{reviews}</span></p>
                        </div>
                    ))}

                    <a
                        className='w-fit mx-10 mt-5 underline underline-offset-2'
                        href='/History'
                    >Voir plus</a>
                </div>
                <Button text={action} textCol={'text-white mt-8 mb-[8em]'} bg={'bg-[#ffcd74]'} submitted={true} link={link} />
                <Navbar active={'home'} />
            </div>
        </>
    );
}

export default Home