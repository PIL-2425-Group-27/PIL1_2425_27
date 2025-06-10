function Option(props) {
    return (
        <>
            <div>
                <img
                    className="w-1/3 aspect-square rounded-full border-4 border-green-400"
                    src={props.icon}
                    alt="icon"
                />
            </div>

        </>
    );
} export default Option