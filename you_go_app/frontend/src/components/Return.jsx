function Return(props) {
    return (
        <>
            <div className="flex flex-row items-start px-2.5 absolute top-[3.5vh] left-3">
                <a
                    className="flex flex-row text-2sm font-bold"
                    href={props.link!=undefined? props.link:'/'}><img
                        className="w-6 aspect-square"
                        src="./src/assets/icons/arrow_back.svg"
                        alt="return" />
                </a>
            </div>
        </>
    )
}export default Return