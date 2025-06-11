import { useState } from "react";
import Button from "../components/Button";

function Checkbox(props) {
    const [checked, setchecked] = useState(props.checked)
    let bg = checked == true ? 'bg-red-400' : ''
    return (
        <>
            <div className="flex flex-row w-full items-center justify-start pl-8 gap-4" >
                <input
                    onClick={()=>{setchecked(!checked);console.log(checked)}}
                    className={`appearance-none max-w-6 rounded-full border-2 border-green-500 aspect-square ${bg}`}
                    type="checkbox"
                    name={props.name}
                    id="checkbox"
                    value={props.val}
                />
                <label
                    htmlFor="checkbox"
                    className="text-2xl font-semibold">{props.text}</label>
            </div>
        </>
    );
}

export default Checkbox;