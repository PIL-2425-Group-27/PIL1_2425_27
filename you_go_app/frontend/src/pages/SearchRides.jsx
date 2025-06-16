import Navbar from "../components/Navbar";
import Return from "../components/Return";
import SearchBar from "../components/SearchBar";
import Title from "../components/Title";

function SearchRides() {
    let theme = false
    return (
        <>
            <div className={`w-full h-screen flex flex-col ${theme == false ? 'bg-white' : 'bg-[#2d2d2d] text-white'} items-center justify-center`}>
                <Return theme={theme} />
                <Title content={'Rechercher'} floating={true} />
                <SearchBar theme={theme}/>
                <div
                    className="w-full"
                >

                </div>
            </div>

        </>
    );
}

export default SearchRides;