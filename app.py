import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="NutriFit Maria", layout="centered", page_icon="🥗")

# --- CONTROLUL ETAPELOR ---
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False
if "etapa_curenta" not in st.session_state:
    st.session_state["etapa_curenta"] = "selectie"

# --- PASUL 0: LOGARE ---
if not st.session_state["autentificat"]:
    st.title("🥗 Aplicația Mariei")
    st.subheader("Autentificare necesară")
    parola = st.text_input("Parola de acces:", type="password")
    if st.button("Conectare"):
        if parola == "nutrifit2026":
            st.session_state["autentificat"] = True
            st.rerun()
        else:
            st.error("Parolă incorectă!")
    st.stop()

# --- PASUL 1: SELECȚIE ALIMENTE ---
if st.session_state["etapa_curenta"] == "selectie":
    st.title("👩‍💻 Aplicația Mariei")
    st.subheader("Pasul 1: Selectează alimentele pentru meniu")
    
    # Generăm lista de 200 de opțiuni
    optiuni_200 = [f"Aliment/Preparat #{i}" for i in range(1, 201)]
    alegeri = st.multiselect("Alege din cele 200 de variante:", options=optiuni_200)

    if alegeri:
        st.divider()
        st.subheader("Pasul 2: Agent AI")
        if st.button("🤖 Generează Planul pe 7 Zile"):
            st.session_state["alimente_selectate"] = alegeri
            st.session_state["etapa_curenta"] = "raport"
            st.rerun()
    else:
        st.info("Selectează minim un aliment pentru a activa Agentul AI.")

# --- PASUL 2: RAPORT FINAL (Meniu 7 Zile) ---
elif st.session_state["etapa_curenta"] == "raport":
    st.title("📅 Planul tău NutriFit pe 7 Zile")
    st.success("Agentul AI a generat meniul săptămânal!")

    zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
    selectie = st.session_state["alimente_selectate"]
    
    plan_zile = []
    for i, zi in enumerate(zile):
        # Alocăm alimentele selectate pe zilele săptămânii
        articol = selectie[i % len(selectie)]
        plan_zile.append({
            "Ziua": zi,
            "Sugestie Meniu": articol,
            "Recomandare": "Consum conform planului"
        })

    df = pd.DataFrame(plan_zile)
    st.table(df) # Afișăm tabelul curat de nutriție

    st.divider()
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Descarcă Meniul (Excel)", data=csv, file_name="Meniu_7_Zile.csv")
    
    if st.button("🔄 Start Nou"):
        st.session_state["etapa_curenta"] = "selectie"
        st.rerun()

# Buton Logout
if st.sidebar.button("Logout"):
    st.session_state["autentificat"] = False
    st.rerun()
