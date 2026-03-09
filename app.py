import streamlit as st
import pandas as pd
from io import BytesIO

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="centered")

# --- FUNCȚII UTILITARE ---
def convert_df_to_excel(df_to_convert):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_to_convert.to_excel(writer, index=False, sheet_name='Date_Procesate')
        worksheet = writer.sheets['Date_Procesate']
        for i, col in enumerate(df_to_convert.columns):
            column_len = max(df_to_convert[col].astype(str).str.len().max(), len(col)) + 2
            worksheet.set_column(i, i, column_len)
    return output.getvalue()

def check_password():
    """Returnează True dacă utilizatorul a introdus parola corectă."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # Interfața de Login
    st.title("🔐 Acces Securizat")
    password = st.text_input("Introdu parola pentru a accesa datele:", type="password")
    
    if st.button("Autentificare"):
        if password == "maria2024":  # <--- AICI MODIFICI PAROLA DORITĂ
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ Parolă incorectă!")
    return False

# --- LOGICA APLICAȚIEI ---

if check_password():
    # Tot ce este aici apare DOAR dacă parola este corectă
    st.markdown("# 📊 Finalizare și Export Date")
    st.write("Verifică datele de mai jos înainte de a genera fișierul Excel final.")

    # 1. Datele
    data = {
        "ID": [1, 2, 3, 4],
        "Descriere": ["Produs A", "Produs B", "Serviciu C", "Mentenanță"],
        "Cantitate": [10, 5, 2, 1],
        "Pret Unitar (RON)": [100, 250, 1500, 500]
    }
    df = pd.DataFrame(data)

    # 2. Logica de calcul
    df["Total Fara TVA"] = df["Cantitate"] * df["Pret Unitar (RON)"]
    df["TVA (19%)"] = df["Total Fara TVA"] * 0.19
    df["Total de Plata"] = df["Total Fara TVA"] + df["TVA (19%)"]

    # 3. Afișare Tabel
    st.subheader("Previzualizare Tabel")
    st.dataframe(df, use_container_width=True)

    st.divider()

    # 4. Secțiunea de Export
    st.markdown("### 💾 Exportă Rezultatele")
    
    nume_fisier = st.text_input("Numele fișierului pentru salvare:", value="raport_final_maria")
    
    excel_data = convert_df_to_excel(df)

    st.download_button(
        label="📥 Descarcă fișierul Excel (.xlsx)",
        data=excel_data,
        file_name=f"{nume_fisier}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Opțional: Buton de Logout
    if st.sidebar.button("Ieșire (Logout)"):
        st.session_state["password_correct"] = False
        st.rerun()
