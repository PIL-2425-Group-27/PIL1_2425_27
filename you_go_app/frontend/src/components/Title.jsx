
function Title(props) {
    let floating = props.floating == true ? 'absolute' : '';
    return (
        <>
            <div className="w-2/3 flex flex-row items-center justify-center gap-2 mt-2">
                <h1 className={`top-[3vh] text-2xl text-center font-bold ${floating}`}>
                    {props.content}
                </h1>
                <img
                    className={`w-5 aspect-square rounded-full bg-blue-400 ${props.visible? '':'hidden'}`}
                    src={props.image} />
            </div>
            <p
                className="text-lg text-gray-500 font-semibold"
            >{props.subContent}</p>
        </>
    );
} export default Title