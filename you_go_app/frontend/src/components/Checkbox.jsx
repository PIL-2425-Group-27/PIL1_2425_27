import { useState } from "react";
import Button from "../components/Button";

function Checkbox(props) {
    const [checked, setchecked] = useState(props.checked)
    let bg = props.selected == true ? 'bg-[url(./src/assets/icons/checked.svg)]' : ''
    
    const handleCheckboxChange = (e) => {
        setchecked(e.target.checked);
        // console.log(e.target.value)
        props.passer(e.target.value)
    };

    return (
        <>
            <div className="flex flex-row w-full items-center justify-start pl-8 gap-4" >
                <input
                    onChange={handleCheckboxChange}
                    className={`appearance-none max-w-6 rounded-full border-2 border-[#ffcd74] aspect-square ${bg} bg-center bg-contain`}
                    type="checkbox"
                    name={props.name}
                    id={props.val}
                    value={props.val}
                    checked={checked}
                />
                <label
                    htmlFor={props.val}
                    className="text-2xl font-semibold">{props.text}</label>
            </div>
        </>
    );
}

export default Checkbox;