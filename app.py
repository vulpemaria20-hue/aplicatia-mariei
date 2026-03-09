import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="centered")

# --- ETAPA 0: LOGARE (Blocaj Total) ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.title("👩‍💻 Aplicația Mariei")
    parola = st.text_input("Introdu parola de acces:", type="password")
    if st.button("Conectare"):
        if parola == "nutrifit2026":
            st.session_state["auth"] = True
            st.rerun()
        else:
            st.error("Parolă incorectă")
    st.stop()

# --- ETAPA 1: SELECȚIE (Cele 200 de opțiuni) ---
if "raport_gata" not in st.session_state:
    st.title("👩‍💻 Aplicația Mariei")
    st.subheader("Pasul 1: Selectează alimentele pentru meniu")
    
    # Lista de 200 de opțiuni (alimente/meniuri)
    optiuni_nutritie = [f"Opțiunea {i}: Preparat NutriFit Personalizat" for i in range(1, 201)]
    
    selectie = st.multiselect("Alege din cele 200 de variante:", options=optiuni_nutritie)

    if selectie:
        st.divider()
        st.subheader("Pasul 2: Agent AI")
        if st.button("🤖 Procesează cu Agentul AI"):
            st.session_state["lista_finala"] = selectie
            st.session_state["raport_gata"] = True
            st.rerun()
    else:
        st.info("Selectează minim un aliment pentru a activa Agentul AI.")

# --- ETAPA 2: RAPORTUL DE EXPORTAT ---
else:
    st.title("👩‍💻 Raport Nutriție Final")
    st.success("Agentul AI a generat meniul pe baza selecției tale.")

    # Creăm tabelul simplu pentru export
    date_meniu = []
    for idx, aliment in enumerate(st.session_state["lista_finala"]):
        date_meniu.append({
            "Nr. Crt": idx + 1,
            "Aliment/Preparat": aliment,
            "Observații AI": "Consum recomandat conform planului"
        })
    
    df = pd.DataFrame(date_meniu)
    st.table(df) # Afișăm meniul ales

    st.divider()
    
    # Butonul de Export
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Exportă Raportul (Excel/CSV)",
        data=csv,
        file_name="Meniu_Maria_Nutrifit.csv",
        mime="text/csv"
    )

    if st.button("🔄 Crează un meniu nou"):
        st.session_state["raport_gata"] = False
        st.rerun()

# Buton Logout
if st.sidebar.button("Ieșire"):
    st.session_state["auth"] = False
    st.rerun()
