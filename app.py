import streamlit as st
import pandas as pd
from io import BytesIO

# 1. Configurare Pagină
st.set_page_config(page_title="NutriFit - Management Date", layout="centered", page_icon="🍏")

# --- FUNCȚIE EXPORT EXCEL ---
def generate_excel(df_to_convert):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_to_convert.to_excel(writer, index=False, sheet_name='Rezultate_NutriFit')
        
        # Ajustare automată coloane pentru un aspect profesional
        worksheet = writer.sheets['Rezultate_NutriFit']
        for i, col in enumerate(df_to_convert.columns):
            column_len = max(df_to_convert[col].astype(str).str.len().max(), len(col)) + 2
            worksheet.set_column(i, i, column_len)
    return output.getvalue()

# --- SISTEM DE AUTENTIFICARE ---
def check_auth():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.title("🔐 Acces NutriFit 2026")
        
        # Câmpul de introducere parolă
        user_password = st.text_input("Introdu parola de acces:", type="password")
        
        if st.button("Autentificare"):
            # Parola ceruta de tine
            if user_password == "nutrifit2026":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Parolă incorectă. Te rugăm să încerci din nou.")
        return False
    return True

# --- LOGICA PRINCIPALĂ ---
if check_auth():
    # Meniu lateral pentru Logout
    if st.sidebar.button("Ieșire (Logout)"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.markdown("# 📊 Finalizare și Export Date")
    st.info("Acces autorizat. Datele de mai jos sunt gata pentru procesarea finală.")

    # 1. Definire Date (Poți înlocui acest dicționar cu datele tale reale)
    data = {
        "ID": [1, 2, 3, 4],
        "Descriere": ["Abonament Fit", "Consultanță Nutriție", "Suplimente Vitamine", "Plan Personalizat"],
        "Cantitate": [12, 5, 20, 3],
        "Pret Unitar (RON)": [200, 150, 85, 450]
    }
    df = pd.DataFrame(data)

    # 2. Calcule Automate (Logica de Business)
    df["Total Fara TVA"] = df["Cantitate"] * df["Pret Unitar (RON)"]
    df["TVA (19%)"] = df["Total Fara TVA"] * 0.19
    df["Total Final (RON)"] = df["Total Fara TVA"] + df["TVA (19%)"]

    # 3. Prezentare Tabel
    st.subheader("📋 Previzualizare Date")
    st.dataframe(df, use_container_width=True)

    st.divider()

    # 4. Zona de Export
    st.subheader("💾 Exportă în Excel")
    
    col_name, col_btn = st.columns([2, 1])
    
    with col_name:
        nume_fisier = st.text_input("Denumire fișier:", value="Raport_NutriFit_2026")
    
    # Pregătire fișier Excel
    excel_binary = generate_excel(df)

    with col_btn:
        st.write("") # Spațiere pentru aliniere cu input-ul
        st.write("") 
        st.download_button(
            label="Descarcă Excel",
            data=excel_binary,
            file_name=f"{nume_fisier}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    st.success(f"Gata! Poți descărca fișierul sub numele: {nume_fisier}.xlsx")
