import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Button from "../components/Button";
import Return from "../components/Return";

function ChangePassword() {
    const navigate = useNavigate();
    const [visible, setVisible] = useState(false);
    const [oldPassword, setOldPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState(false);

    useEffect(() => {
        if (success) {
            navigate("/PasswordChanged");
        }
    }, [success, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        if (newPassword !== confirmPassword) {
            setError("Les mots de passe ne correspondent pas.");
            return;
        }

        const token = localStorage.getItem("authToken");
        if (!token) {
            setError("Utilisateur non connecté.");
            return;
        }

        setLoading(true);

        try {
            const response = await fetch("http://localhost:8000/accounts/password/change/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    old_password: oldPassword,
                    new_password: newPassword,
                    new_password2: confirmPassword
                })
            });

            const text = await response.text();
            let data = {};

            if (text) {
                try{
                    data = JSON.parse(text);
                } catch (e) {
                    console.error("Réponse non JSON :", text);
                    throw new Error("Réponse invalide reçu du serveur.");
                }
            } 

            if (!response.ok) {
                throw new Error(data.detail || data.error || text || "Une erreur s'est produite.");
            }

            setSuccess(true);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center h-screen bg-gray-100 font-manrope">
            <Return />
            <h2 className="text-3xl mb-6">Changer le mot de passe</h2>

            <form className="w-full max-w-md space-y-4" onSubmit={handleSubmit}>
                <input
                    type={visible ? "text" : "password"}
                    placeholder="Ancien mot de passe"
                    value={oldPassword}
                    onChange={(e) => setOldPassword(e.target.value)}
                    required
                    className="w-full p-3 border rounded"
                />
                <input
                    type={visible ? "text" : "password"}
                    placeholder="Nouveau mot de passe"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    required
                    className="w-full p-3 border rounded"
                />
                <input
                    type={visible ? "text" : "password"}
                    placeholder="Confirmer le mot de passe"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    className="w-full p-3 border rounded"
                />

                <div className="flex items-center">
                    <input
                        type="checkbox"
                        checked={visible}
                        onChange={() => setVisible(!visible)}
                        className="mr-2"
                    />
                    <label>Afficher les mots de passe</label>
                </div>

                {error && <p className="text-red-500">{error}</p>}

                <Button
                    type="submit"
                    disabled={loading}
                    text={loading ? "Chargement..." : "Changer"}
                    bg="bg-blue-500"
                    textCol="text-white"
                />
            </form>
        </div>
    );
}
export default   ChangePassword;    