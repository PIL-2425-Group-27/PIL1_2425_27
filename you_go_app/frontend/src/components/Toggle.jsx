function Toggle(props) {
    
    return (
        <>
            <a href={props.link}
            onClick={props.onclick}
            >
                <div
                    className="flex flex-row items-center px-8 py-1 "
                >
                    <div
                        className="w-14 aspect-square rounded-full bg-[#d4d4d4] flex flex-col items-center justify-center">
                        <img
                            className="w-2/3 aspect-square"
                            src={props.icon}
                            alt="icon" />
                    </div>
                    <h1 className="w-full text-left text-xl px-1.5 font-semibold">
                        {props.content}
                    </h1>
                </div>
            </a>

        </>
    );
} export default Toggle