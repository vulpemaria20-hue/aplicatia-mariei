import streamlit as st
import pandas as pd
from io import BytesIO

# Configurare pagină (opțional)
st.set_page_config(page_title="Aplicația Mariei", layout="centered")

def main():
    st.title("📊 Finalizare și Export Date")
    st.write("Verifică datele de mai jos înainte de a genera fișierul Excel final.")

    # 1. Datele tale (Exemplu de tabel - aici poți pune datele tale reale)
    data = {
        "ID": [1, 2, 3, 4],
        "Descriere": ["Produs A", "Produs B", "Serviciu C", "Mentenanță"],
        "Cantitate": [10, 5, 2, 1],
        "Pret Unitar (RON)": [100, 250, 1500, 500]
    }

    df = pd.DataFrame(data)

    # 2. Logica de calcul (Calculăm Totalul automat)
    df["Total Fara TVA"] = df["Cantitate"] * df["Pret Unitar (RON)"]
    df["TVA (19%)"] = df["Total Fara TVA"] * 0.19
    df["Total de Plata"] = df["Total Fara TVA"] + df["TVA (19%)"]

    # Afișarea tabelului în interfață
    st.subheader("Previzualizare Tabel")
    st.dataframe(df, use_container_width=True)

    # 3. Secțiunea de Export
    st.divider()
    st.subheader("💾 Exportă Rezultatele")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nume_fisier = st.text_input("Numele fișierului:", "raport_final_maria")
    
    with col2:
        # Funcție pentru conversia în Excel (folosind librăria xlsxwriter)
        def convert_df_to_excel(df_to_convert):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_to_convert.to_excel(writer, index=False, sheet_name='Date_Procesate')
                
                # Accesăm obiectul workbook pentru a adăuga formatări dacă e nevoie
                workbook = writer.book
                worksheet = writer.sheets['Date_Procesate']
                
                # Ajustăm automat lățimea coloanelor
                for i, col in enumerate(df_to_convert.columns):
                    column_len = max(df_to_convert[col].astype(str).str.len().max(), len(col)) + 2
                    worksheet.set_column(i, i, column_len)
            
            return output.getvalue()

        excel_data = convert_df_to_excel(df)

        # Butonul de descărcare (fără emoji-uri problematice în codul de bază)
        st.download_button(
            label="Descarca fisierul Excel",
            data=excel_data,
            file_name=f"{nume_fisier}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
