function Option(props) {
    return (
        <>
            <a href={props.link}>
                <div
                    className="flex flex-row items-center px-8 py-1 "
                >
                    <div
                        className="w-12 aspect-square rounded-full bg-[#ffcb74] flex flex-col items-center justify-center">
                        <img
                            className="w-2/3 aspect-square"
                            src={props.icon}
                            alt="icon" />
                    </div>
                    <h1 className="w-full text-left text-xl px-1.5 font-semibold">
                        {props.content}
                    </h1>
                    <img
                        className="w-6 aspect-square"
                        src='./src/assets/icons/right-arrow-light.svg'
                        alt="icon" />
                </div>
            </a>

        </>
    );
} export default Option