function NavItem(props) {
    return (
        <>
            <a href={props.link}>
                <div
                    className="w-16 aspect-square flex flex-col items-center justify-center">
                    <img
                        className={`w-1/2 aspect-square ${props.filter}`}
                        src={props.icon}
                        alt="icon" />
                    <p className="text-gray-800 font-semibold text-2sm">{props.content}</p>
                    <div className={`w-3 aspect-square rounded-full bg-[#ffcd74] ${props.active?'':'hidden'}`}>

                    </div>
                </div>
            </a>

        </>
    );
} export default NavItem