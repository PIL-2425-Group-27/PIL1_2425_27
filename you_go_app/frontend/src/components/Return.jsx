import { useNavigate } from "react-router-dom"

function Return(props) {
    const navigate = useNavigate()
    return (
        <>
            <div className={`flex flex-row ${props.theme == false ? '' : 'bg-none invert-100'} items-start px-2.5 absolute top-[3.5vh] left-3`}>
                <a
                    className="flex flex-row text-2sm font-bold"
                    onClick={()=>navigate(-1)}>
                    <img
                        className="w-6 aspect-square"
                        src="../src/assets/icons/arrow_back.svg"
                        alt="return" />
                </a>
            </div>
        </>
    )
} export default Return