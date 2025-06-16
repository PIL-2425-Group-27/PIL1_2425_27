import FAQItem from "../components/FAQItem";
import Return from "../components/Return";
import Title from "../components/Title";
FAQItem

function FAQ() {
    let theme =true
    const faqList = [
        {
            id: 0,
            question: "C'est quoi YouGo?",
            answer: '30 min',
        },
        {
            id: 1,
            question: "Votre trajet a duré 35 minutes.",
            answer: '45 min',
        },
        {
            id: 2,
            question: "Veuillez noter votre conducteur",
            answer: '25 min',
        },
        {
            id: 3,
            question: "Votre conducteur vient dans 15 minutes",
            answer: '50 min',
        },
        {
            id: 4,
            question: "Vous avez un match avec un conducteur. Visitez son profil",
            answer: '1 heure',
        },
        {
            id: 5,
            question: "Placeholder",
            answer: '10 min',
        },
        {
            id: 6,
            question: "Placeholder",
            answer: '39 min',
        },
    ]

    return (
        <>
            <div
                className={`w-full h-screen ${theme==false?'bg-[#e8e8e8]':'bg-[#2d2d2d] text-white'} flex flex-col items-center justify-evenly py-10`}
            >
                <Return link={'/Profile'} theme={theme}/>
                <Title content={'FAQs'} floating={true} />
                <div className="w-full h-full flex flex-col items-center justify-start pt-[8vh] gap-[1vh]">
                    {faqList.map((faqItem) =>
                        <FAQItem key={faqItem.id} question={faqItem.question.length <= 45 ? faqItem.question : faqItem.question.slice(0, 45) + '...'} answer={faqItem.answer} theme={theme}/>
                    )}

                </div>
            </div>
        </>
    );
}

export default FAQ;