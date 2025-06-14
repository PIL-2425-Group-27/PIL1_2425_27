
function Photo(props) {
    return (
        <>
            <div
                className="w-[18vh] flex flex-col items-center relative">
                <img
                    className="w-full aspect-square rounded-full border-4 border-[#bebebe]"
                    src={props.picture}
                    alt="profile Picture"
                />
            </div>
        </>
    );
} export default Photo