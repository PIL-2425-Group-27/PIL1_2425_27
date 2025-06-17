import Button from "../components/Button";
import NotificationItem from "../components/NotificationItem";
import Return from "../components/Return";
import Title from "../components/Title";

function Notifications() {
    let theme= true
    const notificationList = [
        {
            id:0,
            content:'Votre requete a ete vue par 55 personnes.',
            time:'12:13',
            link:'',
        },
        {
            id:1,
            content:'Votre trajet a duré 35 minutes.',
            time:'11:58',
            link:'',
        },
        {
            id:2,
            content:'Veuillez noter votre conducteur',
            time:'11:45',
            link:'',
        },
        {
            id:3,
            content:'Votre conducteur vient dans 15 minutes',
            time:'11:20',
            link:'',
        },
        {
            id:4,
            content:'Vous avez un match avec un conducteur. Visitez son profil',
            time:'10:30',
            link:'',
        },
        {
            id:5,
            content:'Placeholder',
            time:'10:07',
            link:'',
        },
        {
            id:6,
            content:'Placeholder',
            time:'06:05',
            link:'',
        },
    ]
    
    return (
        <>
            <div
                className={`w-full h-screen ${theme == false ? 'bg-white' : 'bg-[#2d2d2d] text-white'} flex flex-col items-center justify-evenly py-10`}
            >
                <Return link={'/'}/>
                <Title content={'Notifications'} floating={true} />
                <div className="w-full h-full flex flex-col items-center justify-start pt-[8vh] gap-[1vh]">
                    {notificationList.map((notification)=>
                    <NotificationItem key ={notification.id}  pos={notificationList.indexOf(notification)}  content = {notification.content.length <= 45?notification.content:notification.content.slice(0,45)+'...'} time = {notification.time} notifs = {notificationList} theme={theme}/>
                )}

                </div>
            </div>
        </>
    );
}

export default Notifications;