
function Photo(props) {
    return (
        <>
            <img
                className="w-1/3 aspect-square rounded-full border-4 border-green-400"
                src={props.picture}
                alt="profile Picture"
            />
        </>
    );
} export default Photo