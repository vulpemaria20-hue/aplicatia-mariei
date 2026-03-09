import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="centered", page_icon="👩‍💻")

# --- GESTIONARE STARE (SESSION STATE) ---
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False
if "ai_rulat" not in st.session_state:
    st.session_state["ai_rulat"] = False
if "selectie_salvata" not in st.session_state:
    st.session_state["selectie_salvata"] = []

# --- ECRAN 1: LOGARE (STRICT) ---
if not st.session_state["autentificat"]:
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.subheader("🔐 Introducere Parolă")
    parola = st.text_input("Parola de acces:", type="password")
    if st.button("Autentificare"):
        if parola == "nutrifit2026":
            st.session_state["autentificat"] = True
            st.rerun()
        else:
            st.error("Parolă incorectă!")
    st.stop() # Oprește totul aici până la logare

# --- ECRAN 2: SELECȚIE ȘI AGENT AI ---
if st.session_state["autentificat"] and not st.session_state["ai_rulat"]:
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.info("👋 Bine ai venit! Urmează pașii de mai jos.")
    
    st.markdown("### 📝 Pasul 1: Selecție Opțiuni")
    st.write("Alege din cele 200 de configurații:")

    # Lista de 200 opțiuni
    optiuni_200 = [f"Serviciu NutriFit #{i}" for i in range(1, 201)]
    selectie = st.multiselect("Selectează opțiunile dorite:", options=optiuni_200)

    if selectie:
        st.session_state["selectie_salvata"] = selectie
        st.divider()
        st.markdown("### 🤖 Pasul 2: Agent AI")
        if st.button("🚀 Procesează cu Agentul AI"):
            st.session_state["ai_rulat"] = True
            st.rerun()
    else:
        st.warning("Te rugăm să selectezi cel puțin o opțiune pentru a continua.")

# --- ECRAN 3: TABEL FINAL ȘI EXPORT ---
elif st.session_state["ai_rulat"]:
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.success("✅ Agentul AI a finalizat procesarea!")
    
    st.subheader("📊 Previzualizare Tabel Final")
    
    # Construim tabelul exact ca în cerințele tale
    date_finale = []
    for idx, item in enumerate(st.session_state["selectie_salvata"]):
        pret = 150.0
        date_finale.append({
            "ID": idx + 1,
            "Descriere Serviciu": item,
            "Cantitate": 1,
            "Pret Unitar (RON)": pret,
            "Total Fara TVA": pret,
            "TVA (19%)": pret * 0.19,
            "Total de Plata": pret * 1.19
        })
    
    df = pd.DataFrame(date_finale)
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.subheader("💾 Exportă Rezultatele")
    
    # Export CSV sigur (UTF-8-SIG pentru a fi recunoscut de Excel cu diacritice)
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Descarcă Raportul pentru Excel",
        data=csv,
        file_name="Raport_Final_Maria.csv",
        mime="text/csv"
    )

    if st.button("🔄 Începe o sesiune nouă"):
        st.session_state["ai_rulat"] = False
        st.session_state["selectie_salvata"] = []
        st.rerun()

# Buton Logout (Sidebar)
if st.sidebar.button("Ieșire (Logout)"):
    st.session_state["autentificat"] = False
    st.session_state["ai_rulat"] = False
    st.rerun()
