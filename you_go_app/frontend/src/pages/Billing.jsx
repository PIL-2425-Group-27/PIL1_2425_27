import React, { useState } from "react";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import { useNavigate } from "react-router-dom";

// ✅ import du fichier SVG
import arrowBack from "../assets/icons/arrow_back.svg";

const invoices = [
  {
    id: 1,
    date: "10/06/2024",
    trajet: "Cotonou → Calavi",
    conducteur: "Marie Dupont",
    passager: "Jean Martin",
    total: 2500,
  },
  {
    id: 2,
    date: "08/06/2024",
    trajet: "Porto-Novo → Cotonou",
    conducteur: "Paul Agbo",
    passager: "Sarah Kone",
    total: 1500,
  },
];

export default function Billing() {
  const [selectedDate, setSelectedDate] = useState("");
  const navigate = useNavigate();

  const filteredInvoices = selectedDate
    ? invoices.filter((f) => f.date === selectedDate)
    : invoices;

  const generatePDF = async (invoice) => {
    const input = document.getElementById(`invoice-${invoice.id}`);
    const canvas = await html2canvas(input);
    const imgData = canvas.toDataURL("image/png");

    const pdf = new jsPDF();
    pdf.addImage("/logo.svg", "SVG", 10, 10, 40, 15);
    pdf.addImage(imgData, "PNG", 10, 30, 190, 0);
    pdf.save(`facture-${invoice.id}.pdf`);
  };

  return (
    <div className="p-4">
      {/* En-tête avec flèche (arrow_back) et logo */}
      <div className="flex items-center gap-2 mb-6">
        <img
          src={arrowBack}
          alt="Retour"
          onClick={() => navigate(-1)}
          className="h-6 w-6 cursor-pointer"
        />
        <img src="/logo.svg" alt="Logo" className="h-8" />
      </div>

      <h2 className="text-2xl font-bold mb-4">Mes Factures</h2>

      <input
        type="date"
        value={selectedDate}
        onChange={(e) => setSelectedDate(e.target.value)}
        className="border p-2 rounded mb-6"
      />

      {filteredInvoices.map((invoice) => (
        <div
          key={invoice.id}
          id={`invoice-${invoice.id}`}
          className="border rounded p-4 mb-4 shadow"
        >
          <p className="font-semibold">Facture #{invoice.id}</p>
          <p>Date : {invoice.date}</p>
          <p>Trajet : {invoice.trajet}</p>
          <p>Conducteur : {invoice.conducteur}</p>
          <p>Passager : {invoice.passager}</p>
          <p className="text-green-600 font-semibold">
            Total : {invoice.total.toLocaleString()} F CFA
          </p>

          <button
            onClick={() => generatePDF(invoice)}
            className="mt-4 bg-yellow-400 hover:bg-yellow-500 text-black font-semibold py-1 px-3 rounded"
          >
            Télécharger PDF
          </button>
        </div>
      ))}
    </div>
  );
}
