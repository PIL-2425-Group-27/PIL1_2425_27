import React from "react";
import Navbar from "../components/Navbar";
// import { useTheme } from "../context/ThemeContext"; // supprimé

const Settings = () => {
  // Valeurs par défaut (temporairement)
  const darkMode = false;
  const toggleTheme = () => {};

  return (
    <div className={`${darkMode ? "bg-black text-white" : "bg-white text-black"} min-h-screen`}>
      <Navbar currentPage="settings" />

      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">Paramètres</h1>

        <div className="flex items-center space-x-4">
          <span>Thème :</span>
          <button
            onClick={toggleTheme}
            className="px-4 py-2 border rounded hover:bg-gray-200 dark:hover:bg-gray-700"
          >
            {darkMode ? "Mode clair" : "Mode sombre"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Settings;
