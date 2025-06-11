
function Button(props) {
    // let icon = "./src/assets/icons/logout.svg"
    let hidden = props.icon == '' || props.icon == undefined ? 'hidden' : '';
    return (
        <>
            <a
                className="w-9/12 flex flex-col items-center"
                href="/Register">
                <button
                    onClick={props.onClick}
                    type={props.type}
                    className={`w-full max-w-lg h-13 rounded-4xl text-white flex flex-row items-center justify-center gap-2.5 ${props.bg} ${props.anim}`}
                ><p
                    className={`text-xl ${props.textCol}`}
                >{props.text}
                    </p>
                    <img
                        className={`w-[10%] ${hidden}`}
                        src={props.icon}
                        alt="icon" />
                </button>
            </a>
        </>
    )
} export default Button