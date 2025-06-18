import { useState,useEffect } from 'react';
import Button from '../components/Button';
import Chart from '../components/Chart';
import Navbar from '../components/Navbar';
import Notification from '../components/Notification';
import axios from 'axios';
import Loading from './Loading';



function Home() {
    let theme = false
    const [statut, setStatut] = useState('PASSAGER')
    const action = statut === 'passager' ? 'Publier une demande' : 'Publier une offre';
    const link = statut === 'passager' ? '/PublishRequest' : '/PublishOffer';
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState()
    const [total_km, setTotal_km] = useState([])
    console.log(user);
    const token = localStorage.getItem("authToken");
    const [historyList, setHistoryList] = useState([]);

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
                console.log(res.data);
                setTotal_km(res.data.total_km)
                
            } catch (error) {
                console.error("Failed to fetch user:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchHistory();
    }, []);
    

    if (loading) {
        return <Loading/>;
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
                    <Chart km={total_km}/>
                </div>
                <div className='relative w-9/10 px-4 py-10 bg-[#e8e8e8] rounded-3xl mt-9 flex flex-col'>
                    <h1 className=' absolute top-0 left-0 text-xl font-semibold p-4'>Activité Récente</h1>
                    {historyList.map((item, index) => (
                        <div
                            key={index}
                            className='flex flex-row items-center gap-2 mt-4'>
                            <div className='w-4 h-4 bg-[url(./src/assets/icons/checked.svg)] bg-center bg-contain'></div>
                            <h1 className='text-2xl'>
                                <span className='font-semibold'>
                                    {item.content}
                                </span>
                                {' : ' + item.duration}
                            </h1>
                        </div>
                    ))}
                    <a
                        className='w-fit mx-10 mt-5 underline underline-offset-2'
                        href='/History'
                    >Voir plus</a>
                </div>
                <Button text={action} textCol={'text-white mt-8'} bg={'bg-[#ffcd74]'} submitted={true} link={link} />
                <Navbar active={'home'} />
            </div>
        </>
    );
}

export default Home