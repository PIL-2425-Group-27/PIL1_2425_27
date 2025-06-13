import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

function Button(props) {
    // let icon = "./src/assets/icons/logout.svg"
    const btn = useRef(null)
    const [isClicked, setIsClicked] = useState(false)
    let hidden = props.icon == '' || props.icon == undefined ? 'hidden' : '';
    const navigate = useNavigate();
    const condition = props.submitted == true && isClicked;
    useEffect(() => {
        const element = btn.current
        if (element) {
            element.addEventListener('click', (e) => {
                console.log(e.target == element);
                setIsClicked(e.target == element);
                console.log(isClicked);
                if (condition) {
                    navigate(props.link);
                }
            }, [condition, navigate]);
        }
    })
    return (
        <>
            <button
                ref={btn}
                onClick={props.onClick}
                type={props.type}
                className={`w-9/12 max-w-lg h-13 rounded-4xl text-xl ${props.textCol} flex flex-row items-center justify-center gap-2.5 ${props.bg} ${props.anim}`}
            >{props.text}
                <img
                    className={`w-[10%] ${hidden}`}
                    src={props.icon}
                    alt="icon" />
            </button>
        </>
    )
} export default Button