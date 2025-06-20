function Notification(props) {
    let floating = props.floating == true ? 'absolute' : '';
    return (
        <>
            <a
                className={` top-[2vh] right-[2vh] ${floating}`}
                href={props.link}>
                <div className={`w-[10vw] max-w-14 aspect-square rounded-full flex flex-row items-center justify-center ${props.theme==false?'bg-[#ffffff]':'bg-none invert-100'} ${props.icon}`}>
                    <img
                        className={`w-2/3 aspect-square`}
                        src={props.icon} />
                </div>
            </a>
        </>
    );
} export default Notification