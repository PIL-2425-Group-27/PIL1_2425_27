import Navbar from "../components/Navbar";
function Login() {
    return (
        <>
            <div className="w-full h-screen bg-white flex flex-col md:bg-amber-300 lg:bg-green-300">
                <form
                    className="w-full h-fit flex flex-col items-center bg-amber-50"
                    action=""
                    method="post"
                >
                    <div className="w-9/12 max-w-lg h-11 bg-blue-400 rounded-4xl flex flex-row items-center justify-between px-4">
                        <input
                            placeholder="Prenom"
                            type="text"
                            name="fistname"
                            id="firstname"
                        />
                    </div>
                    <div className="w-9/12 max-w-lg h-11 bg-blue-400 rounded-4xl flex flex-row items-center justify-between px-4">
                        <input
                            placeholder="Nom"
                            type="text"
                            name="lastname"
                            id="lastname"
                        />
                    </div>
                    <div className="w-9/12 max-w-lg h-11 bg-blue-400 rounded-4xl flex flex-row items-center justify-between px-4">
                        <input
                            placeholder="Numero de telephone"
                            type="tel"
                            name="phone"
                            id="phone"
                        />
                    </div>
                    <div className="w-9/12 max-w-lg h-11 bg-blue-400 rounded-4xl flex flex-row items-center justify-between px-4">
                        <input
                            placeholder="Mot de passe"
                            type="text"
                            name="password"
                            id="password"
                        />
                    </div>
                </form>
            </div>
        </>
    );
}

export default Login;