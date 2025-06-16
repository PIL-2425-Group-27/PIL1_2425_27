import Button from "../components/Button";
import HistoryItem from "../components/HistoryItem";
import Return from "../components/Return";
import Title from "../components/Title";

function History() {
    let theme = true
    const historyList = [
        {
            id: 0,
            content: 'Votre requete a ete vue par 55 personnes.',
            duration: '30 min',
            link: '',
        },
        {
            id: 1,
            content: 'Votre trajet a duré 35 minutes.',
            duration: '45 min',
            link: '',
        },
        {
            id: 2,
            content: 'Veuillez noter votre conducteur',
            duration: '25 min',
            link: '',
        },
        {
            id: 3,
            content: 'Votre conducteur vient dans 15 minutes',
            duration: '50 min',
            link: '',
        },
        {
            id: 4,
            content: 'Vous avez un match avec un conducteur. Visitez son profil',
            duration: '1 heure',
            link: '',
        },
        {
            id: 5,
            content: 'Placeholder',
            duration: '10 min',
            link: '',
        },
        {
            id: 6,
            content: 'Placeholder',
            duration: '39 min',
            link: '',
        },
    ]

    return (
        <>
            <div
                className={`relative w-full h-screen ${theme == false ? 'bg-white' : 'bg-[#2d2d2d] text-white'} flex flex-col items-center justify-evenly py-10`}
            >
                <Return link={'/Profile'} theme={theme}/>
                <Title content={'Historique'} floating={true} />
                <div className="w-full h-full flex flex-col items-center justify-start pt-[8vh] gap-[1vh]">
                    {historyList.map((historyItem) =>
                        <HistoryItem key={historyItem.id} content={historyItem.content.length <= 45 ? historyItem.content : historyItem.content.slice(0, 45) + '...'} duration={historyItem.duration} />
                    )}

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