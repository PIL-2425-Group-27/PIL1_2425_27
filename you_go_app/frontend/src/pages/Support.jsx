import Button from "../components/Button";
import Return from "../components/Return";
import Title from "../components/Title";

function Support() {
    return (
        <>
            <div className="w-full h-screen flex flex-col items-center">
                <Return link={'/Profile'}/>
                <Title content={'Support client'} floating={true}/>
                <div className="w-full h-full flex flex-col items-center justify-center">
                    <div className="w-full h-fit flex flex-row items-center justify-center">
                    <h1 className="px-6 text-4xl font-semibold text-center">Comment pouvons-nous vous aider?</h1>
                </div>
                <div className="w-2/3 flex flex-row items-center justify-center">
                    <img
                        src="./src/assets/img/support.svg"
                        alt="" />
                </div>
                <div className="w-full h-fit flex flex-row items-center justify-center mb-8">
                    <h1 className="text-xl w-2/3 text-center text-gray-500">Discutez avec notre IA à votre disposition pour répondre à toutes vos préoccupations. </h1>
                </div>
                <Button text={"Discuter avec l'IA"} textCol={'text-white font-semibold'} bg={'bg-[#ffcd74]'} submitted={true} link={'/ChatSupportClient'} />
                </div>
            </div>
        </>
    );
}

export default Support;