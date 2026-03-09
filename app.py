import React, { useState } from 'react';
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';

const GestionareDateExcel = () => {
  // 1. Datele tale (pot veni dintr-un API sau formular)
  const [produse, setProduse] = useState([
    { id: 1, nume: "Laptop Pro", pret: 4500, cantitate: 2 },
    { id: 2, nume: "Monitor 4K", pret: 1800, cantitate: 5 },
    { id: 3, nume: "Tastatură Mecanică", pret: 450, cantitate: 10 },
  ]);

  const [numeFisier, setNumeFisier] = useState("Raport_Vanzari_2024");

  // 2. Funcția de Export cu procesare de date
  const handleExport = () => {
    // Adăugăm calcule automate înainte de export (ex: Total per rând)
    const dateProcesate = produse.map(p => ({
      "ID Produs": p.id,
      "Denumire": p.nume,
      "Preț Unitar (RON)": p.pret,
      "Cantitate": p.cantitate,
      "Total Fără TVA": p.pret * p.cantitate,
      "Total cu TVA (19%)": (p.pret * p.cantitate) * 1.19
    }));

    // Crearea worksheet-ului
    const worksheet = XLSX.utils.json_to_sheet(dateProcesate);
    
    // Setăm lățimea coloanelor pentru a arăta bine în Excel
    worksheet['!cols'] = [
      { wch: 10 }, { wch: 25 }, { wch: 15 }, { wch: 10 }, { wch: 15 }, { wch: 18 }
    ];

    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Inventar");

    // Generăm buffer-ul Excel
    const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
    
    // Creăm Blob-ul și salvăm fișierul
    const data = new Blob([excelBuffer], { type: 'application/octet-stream' });
    saveAs(data, `${numeFisier}.xlsx`);
  };

  return (
    <div style={{ family: 'Arial', padding: '40px', maxWidth: '800px', margin: 'auto' }}>
      <h2>Panou Management Date</h2>
      
      {/* Input pentru personalizarea numelui fișierului */}
      <div style={{ marginBottom: '20px' }}>
        <label>Nume fișier export: </label>
        <input 
          type="text" 
          value={numeFisier} 
          onChange={(e) => setNumeFisier(e.target.value)}
          style={{ padding: '8px', marginLeft: '10px', borderRadius: '4px', border: '1px solid #ccc' }}
        />
      </div>

      {/* Tabel Vizualizare */}
      <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '20px' }}>
        <thead>
          <tr style={{ backgroundColor: '#f4f4f4' }}>
            <th style={tableStyle}>Produs</th>
            <th style={tableStyle}>Preț</th>
            <th style={tableStyle}>Cantitate</th>
          </tr>
        </thead>
        <tbody>
          {produse.map(p => (
            <tr key={p.id}>
              <td style={tableStyle}>{p.nume}</td>
              <td style={tableStyle}>{p.pret} RON</td>
              <td style={tableStyle}>{p.cantitate}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Buton de Finalizare și Export */}
      <button 
        onClick={handleExport}
        style={{
          backgroundColor: '#1D6F42',
          color: 'white',
          padding: '12px 24px',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer',
          fontSize: '16px',
          fontWeight: 'bold',
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}
      >
        📥 Finalizează și Exportă în Excel
      </button>
    </div>
  );
};

const tableStyle = {
  border: '1px solid #ddd',
  padding: '12px',
  textAlign: 'left'
};

export default GestionareDateExcel;
