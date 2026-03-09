import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="NutriFit Maria", layout="centered", page_icon="🥗")

# --- MEMORIA APLICAȚIEI ---
if "logat" not in st.session_state:
    st.session_state["logat"] = False
if "pas" not in st.session_state:
    st.session_state["pas"] = "selectie"

# --- ECRAN 0: LOGIN (Blocaj total) ---
if not st.session_state["logat"]:
    st.title("🥗 NutriFit Maria")
    parola = st.text_input("Parola de acces:", type="password")
    if st.button("Intră în Aplicație"):
        if parola == "nutrifit2026":
            st.session_state["logat"] = True
            st.rerun()
        else:
            st.error("Parolă incorectă!")
    st.stop()

# --- ECRAN 1: SELECȚIE ALIMENTE ---
placeholder = st.empty() # Acesta este secretul pentru curățarea ecranului

if st.session_state["pas"] == "selectie":
    with placeholder.container():
        st.title("👩‍💻 Aplicația Mariei")
        st.subheader("Pasul 1: Selectează alimentele pentru meniu")
        
        # Lista de 200 de opțiuni cerută
        optiuni = [f"Aliment/Preparat #{i}" for i in range(1, 201)]
        alegeri = st.multiselect("Alege din cele 200 de variante:", options=optiuni)

        if alegeri:
            st.divider()
            st.subheader("Pasul 2: Agent AI")
            if st.button("🤖 Generează Planul pe 7 Zile"):
                st.session_state["meniu_ales"] = alegeri
                st.session_state["pas"] = "final"
                st.rerun()
        else:
            st.info("Selectează minim un aliment pentru a activa Agentul AI.")

# --- ECRAN 2: MENIU PE 7 ZILE (Apare DOAR după procesare) ---
elif st.session_state["pas"] == "final":
    with placeholder.container():
        st.title("📅 Planul tău NutriFit pe 7 Zile")
        st.success("Agentul AI a organizat selecția ta într-un plan săptămânal.")

        # Organizăm alimentele pe zile (Luni-Duminică)
        zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
        alimente = st.session_state["meniu_ales"]
        
        # Generăm tabelul final (fără prețuri, doar nutriție)
        plan_final = []
        for i, zi in enumerate(zile):
            # Luăm câte un aliment din listă pentru fiecare zi
            articol = alimente[i % len(alimente)] 
            plan_final.append({
                "Ziua": zi,
                "Mic Dejun": "Omletă/Iaurt (Bază)",
                "Prânz (Ales de tine)": articol,
                "Cină": "Salată ușoară"
            })

        df = pd.DataFrame(plan_final)
        st.table(df) # Afișare tabelară curată

        st.divider()
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Descarcă Meniul (PDF/Excel)", data=csv, file_name="Meniu_Nutrifit.csv")
        
        if st.button("🔄 Începe un meniu nou"):
            st.session_state["pas"] = "selectie"
            st.rerun()

# Buton de Logout în lateral
if st.sidebar.button("Logout"):
    st.session_state["logat"] = False
    st.rerun()
