
function Photo(props) {
    return (
        <>
            <div
                className="w-[18vh] flex flex-col items-center relative">
                <img
                    className="w-full aspect-square rounded-full border-4 border-[#ffcd74]"
                    src={props.picture}
                    alt="profile Picture"
                />
                <div className="w-[20%] rounded-full aspect-square bg-amber-400 absolute bottom-3 right-3">

                </div>
            </div>
        </>
    );
} export default Photo