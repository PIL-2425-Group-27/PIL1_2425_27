import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

function Button(props) {
    // let icon = "./src/assets/icons/logout.svg"
    const btn = useRef(null)
    const [isClicked, setIsClicked] = useState(false)
    let hidden = props.icon == '' || props.icon == undefined ? 'hidden' : '';
    
    return (
        <>
            <a
                disabled={props.disabled}
                href={props.link}
                className="w-full flex flex-col items-center justify-center">
                <button
                    ref={btn}
                    onClick={props.onClick}
                    type={props.type}
                    className={`w-9/12 max-w-lg h-13 rounded-4xl text-xl ${props.textCol} flex flex-row items-center justify-center gap-2.5 ${props.bg} ${props.anim} active:bg-${props.activeCol || '#ffffff'}`}
                >{props.text}
                    <img
                        className={`w-[6vw] ${hidden}`}
                        src={props.icon}
                        alt="icon" />
                </button>
            </a>
        </>
    )
} export default Button