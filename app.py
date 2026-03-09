import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="NutriFit - Management Date", layout="centered", page_icon="🍏")

# --- SISTEM DE AUTENTIFICARE ---
def check_auth():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.title("🔐 Acces NutriFit 2026")
        user_password = st.text_input("Introdu parola de acces:", type="password")
        
        if st.button("Autentificare"):
            if user_password == "nutrifit2026":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Parolă incorectă!")
        return False
    return True

# --- LOGICA PRINCIPALĂ ---
if check_auth():
    if st.sidebar.button("Ieșire (Logout)"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.markdown("# 📊 Finalizare și Export Date")
    
    # 1. Datele
    data = {
        "ID": [1, 2, 3, 4],
        "Descriere": ["Abonament Fit", "Consultanță Nutriție", "Suplimente Vitamine", "Plan Personalizat"],
        "Cantitate": [12, 5, 20, 3],
        "Pret Unitar (RON)": [200, 150, 85, 450]
    }
    df = pd.DataFrame(data)

    # 2. Calcule Automate
    df["Total Fara TVA"] = df["Cantitate"] * df["Pret Unitar (RON)"]
    df["TVA (19%)"] = df["Total Fara TVA"] * 0.19
    df["Total Final (RON)"] = df["Total Fara TVA"] + df["TVA (19%)"]

    # 3. Prezentare Tabel
    st.subheader("📋 Previzualizare Date")
    st.dataframe(df, use_container_width=True)

    st.divider()

    # 4. Zona de Export (Format CSV - Cel mai sigur)
    st.subheader("💾 Exportă Raportul")
    
    nume_fisier = st.text_input("Denumire fișier:", value="Raport_NutriFit_2026")
    
    # Transformăm tabelul în format CSV (text) pe care Excel îl citește nativ
    csv = df.to_csv(index=False).encode('utf-8-sig')

    st.download_button(
        label="Descarcă Raport (Format CSV/Excel)",
        data=csv,
        file_name=f"{nume_fisier}.csv",
        mime="text/csv",
        help="Acest fișier se deschide direct cu Excel."
    )
    
    st.info("💡 Sfat: După ce deschizi fișierul în Excel, îl poți salva ca 'Excel Workbook (.xlsx)' folosind 'Save As'.")
