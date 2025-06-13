function Return(props) {
    return (
        <>
            <div className="flex flex-row items-start px-2.5 absolute top-12 left-3">
                <a
                    className="flex flex-row text-sm font-bold"
                    href={props.link!=undefined? props.link:'/'}><img
                        className="w-5 aspect-square"
                        src="./src/assets/icons/left-arrow.svg"
                        alt="return" />Retour
                </a>
            </div>
        </>
    )
}export default Return