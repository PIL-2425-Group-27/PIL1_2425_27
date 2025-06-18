import { useRef, useState } from "react";
import Button from "../components/Button";
import Return from "../components/Return";

function Verification({ userEmail }) {
  const inputsRef = useRef([]);
  const [code, setCode] = useState(["", "", "", ""]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const theme = false;

  const handleChange = (e, index) => {
    const val = e.target.value;
    if (!/^\d?$/.test(val)) return;

    const newCode = [...code];
    newCode[index] = val;
    setCode(newCode);

    if (val && index < 3) {
      inputsRef.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (e, index) => {
    if (e.key === "Backspace" && !code[index] && index > 0) {
      inputsRef.current[index - 1]?.focus();
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const otp = code.join("");
    if (otp.length < 4) {
      setError("Veuillez entrer le code complet.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/accounts/password/reset/confirm/",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code: otp, email: userEmail }),
        }
      );

      if (response.ok) {
        alert("Code validé avec succès !");
        // Ici, tu peux rediriger vers la page de changement de mot de passe par exemple
      } else {
        const data = await response.json();
        setError(data.error || "Code invalide ou expiré.");
      }
    } catch (err) {
      console.error("Vérification échouée :", err);
      setError("Erreur lors de la vérification.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full h-screen bg-white flex flex-col items-center justify-center gap-6 animate-fade font-manrope">
      <Return link={"/Login"} theme={theme} />
      <div className="w-full h-fit pl-10 flex flex-row items-center justify-start">
        <h1 className="text-3xl font-bold">Vérification</h1>
      </div>
      <div className="w-6/10 aspect-square">
        <img src="./src/assets/img/OTP.svg" alt="OTP Illustration" />
      </div>
      <p className="text-gray-500 text-sm text-center max-w-xs">
        Veuillez entrer le code à 4 chiffres envoyé à votre adresse e-mail.
      </p>

      <form onSubmit={handleSubmit} className="flex flex-col items-center gap-6">
        <div className="flex gap-4">
          {code.map((digit, index) => (
            <input
              key={index}
              ref={(el) => (inputsRef.current[index] = el)}
              type="text"
              inputMode="numeric"
              maxLength={1}
              className="w-12 h-12 text-center border-2 rounded-md text-xl border-gray-300 focus:border-yellow-400 focus:outline-none"
              value={digit}
              onChange={(e) => handleChange(e, index)}
              onKeyDown={(e) => handleKeyDown(e, index)}
            />
          ))}
        </div>

        {error && <p className="text-red-500 text-sm">{error}</p>}

        <Button
          text={loading ? "Vérification..." : "Valider"}
          textCol={"text-white"}
          bg={loading ? "bg-gray-400" : "bg-[#ffcd74]"}
          type={"submit"}
          disabled={loading}
        />
      </form>
    </div>
  );
}

export default Verification;