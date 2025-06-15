import Button from '../components/Button';
import Chart from '../components/Chart';
import Navbar from '../components/Navbar';

function Home() {
    let user = "<User>"
    let action = 'Publier une offre'
    let link = '/PublishOffer'
    const historyList = [
        {
            id: 0,
            content: 'Trajet Parana-ENA',
            duration: '30 min',
            link: '',
        },
        {
            id: 1,
            content: 'Trajet IITA-FASEG',
            duration: '45 min',
            link: '',
        },
        {
            id: 2,
            content: 'Trajet Calavi-ENA',
            duration: '25 min',
            link: '',
        },
    ]
    return (
        <>
            <div className='relative w-full h-screen flex flex-col items-center animate-fade'>
                <div className='w-full  bg-[#ffcd74] rounded-b-3xl px-[4vw] pt-[4vh] pb-[4vw] flex flex-col justify-center gap-[3vh]'>
                    <h1 className='text-3xl font-bold mt-8 text-white'>Bonjour {user}</h1>
                    <a className='absolute top-[4vh] right-[2vh] text-3xl'>search</a>
                    <Chart />
                </div>
                <div className='relative w-9/10 px-4 py-10 bg-[#e8e8e8] rounded-3xl mt-9 flex flex-col'>
                    <h1 className=' absolute top-0 left-0 text-xl font-semibold p-4'>Activité Récente</h1>
                    {historyList.map((item, index) => (
                        <div
                            key={index}
                            className='flex flex-row items-center gap-2 mt-4'>
                            <div className='w-6 aspect-square bg-amber-300'>ii</div>
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