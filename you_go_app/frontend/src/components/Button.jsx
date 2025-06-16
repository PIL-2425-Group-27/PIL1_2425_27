import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

function Button(props) {
    // let icon = "./src/assets/icons/logout.svg"
    const btn = useRef(null)
    const [isClicked, setIsClicked] = useState(false)
    let hidden = props.icon == '' || props.icon == undefined ? 'hidden' : '';
    const navigate = useNavigate();
    let condition = true;
    useEffect(() => {
        const element = btn.current
        if (element) {
            element.addEventListener('click', (e) => {
                console.log(e.target == element);
                setIsClicked(e.target == element);
                console.log('clicked:'+ isClicked);
                console.log(props.submitted);
                condition = props.submitted && (e.target == element);
                if (condition) {
                    navigate(props.link);
                }
            }, [(condition), navigate]);
        }
    })
    return (
        <>
            <a
                className="w-full flex flex-col items-center justify-center">
                <button
                    ref={btn}
                    onClick={props.onClick}
                    type={props.type}
                    className={`w-9/12 max-w-lg h-13 rounded-4xl text-xl ${props.textCol} flex flex-row items-center justify-center gap-2.5 ${props.bg} ${props.anim} active:bg-[#e6b765]`}
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