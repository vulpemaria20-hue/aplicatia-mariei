import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="centered", page_icon="👩‍💻")

# --- VERIFICARE STRICTĂ PAROLĂ ---
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False

if not st.session_state["autentificat"]:
    # Această parte este singura vizibilă la început
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.subheader("🔐 Acces Securizat")
    
    parola = st.text_input("Introdu parola:", type="password")
    
    if st.button("Intră în Aplicație"):
        if parola == "nutrifit2026":
            st.session_state["autentificat"] = True
            st.rerun()
        else:
            st.error("❌ Parolă incorectă!")
    
    # OPRIM TOTUL AICI. Nimic de mai jos nu va fi citit de browser
    st.stop()

# --- DIN ACEST PUNCT UTILIZATORUL ESTE LOGAT ---

if "etapa" not in st.session_state:
    st.session_state["etapa"] = "selectie"

# Meniu lateral pentru Ieșire
if st.sidebar.button("Logout"):
    st.session_state["autentificat"] = False
    st.rerun()

st.markdown("# 👩‍💻 Aplicația Mariei")

# ETAPA DE SELECȚIE (Apare prima după login)
if st.session_state["etapa"] == "selectie":
    st.info("👋 Bine ai venit! Urmează pașii de mai jos.")
    st.markdown("### 📝 Pasul 1: Selecție Opțiuni")
    
    # Lista de 200 opțiuni solicitată
    optiuni_200 = [f"Serviciu NutriFit #{i}" for i in range(1, 201)]
    selectie = st.multiselect("Alege din cele 200 de configurații:", options=optiuni_200)

    if selectie:
        st.divider()
        st.markdown("### 🤖 Pasul 2: Activare Agent AI")
        if st.button("Procesează cu Agentul AI"):
            st.session_state["date_finale"] = selectie
            st.session_state["etapa"] = "export"
            st.rerun()

# ETAPA DE TABEL ȘI EXPORT (Apare doar după butonul AI)
elif st.session_state["etapa"] == "export":
    st.success("✅ Agentul AI a finalizat procesarea!")
    
    st.subheader("📊 Previzualizare Tabel")
    
    # Construim tabelul exact ca în prima ta imagine
    rows = []
    for idx, item in enumerate(st.session_state["date_finale"]):
        pret = 150.0
        rows.append({
            "ID": idx + 1,
            "Descriere": item,
            "Cantitate": 1,
            "Pret Unitar (RON)": pret,
            "Total Fara TVA": pret,
            "TVA (19%)": pret * 0.19,
            "Total de Plata": pret * 1.19
        })
    
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.subheader("💾 Exportă Rezultatele")
    
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Descarcă CSV/Excel",
        data=csv,
        file_name="Raport_Maria_Nutrifit.csv",
        mime="text/csv"
    )

    if st.button("🔄 Start Nou"):
        st.session_state["etapa"] = "selectie"
        st.rerun()
