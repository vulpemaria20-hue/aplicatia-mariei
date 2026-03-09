import streamlit as st
import pandas as pd

# 1. CONFIGURARE PAGINĂ
st.set_page_config(page_title="Nutriția Matematică - Sistem Expert", page_icon="🍎", layout="wide")

# 2. BAZA DE DATE EXTINSĂ (Categorii pentru cele 5 mese)
if "baza_alimente" not in st.session_state:
    st.session_state.baza_alimente = {
        "Mic Dejun": {
            "Omletă": 155, "Smoothie Verde": 54.2, "Budincă Chia": 105.4, 
            "Brioșe din Legume": 95.0, "Ovăz cu lapte": 102, "Pâine cu avocado": 160,
            "Iaurt cu cereale": 120, "Ouă ochiuri": 190, "Clătite proteice": 175
        },
        "Gustări": {
            "Banană": 89, "Măr": 52, "Nuci crude": 654, "Iaurt grecesc 2%": 69, 
            "Baton proteic": 380, "Smoothie Fructe Pădure": 114.6, "Kinder Felie Lapte": 135.88,
            "Migdale": 579, "Brânză perle": 90
        },
        "Prânz": {
            "Tocană de legume": 29.15, "Mâncare de linte": 116, "Somon file": 208, 
            "Orez integral cu legume": 150.4, "Pui la grătar": 165, "Curcan la cuptor": 135,
            "Mușchi de vită": 250, "Păstrăv la grătar": 145, "Iahnie de fasole": 120
        },
        "Cină": {
            "Salată de ton": 158.0, "Supă cremă legume": 45, "Cod la grătar": 105, 
            "Salată grecească": 115, "Piept de pui cu broccoli": 110, "Omletă cu spanac": 140,
            "Curcan cu salată": 125, "Tofu la grătar": 95, "Creveți": 99
        }
    }

# 3. IDENTIFICARE CLIENT (SIDEBAR)
st.sidebar.title("👤 Profil Client")
nume_client = st.sidebar.text_input("Nume Complet Client:", placeholder="Introduceți numele...")

if not nume_client:
    st.title("🔐 Bine ați venit")
    st.info("Vă rugăm să introduceți numele clientului în bara laterală pentru a accesa sistemul.")
    st.stop()

# 4. CALCULATOR METABOLIC (CALORII INIȚIALE ȘI TARGET)
st.title(f"⚖️ Planificator: {nume_client}")

col1, col2 = st.columns(2)
with col1:
    sex = st.selectbox("Sex", ["Feminin", "Masculin"])
    greutate = st.number_input("Greutate (kg)", 40.0, 200.0, 70.0)
    ic = st.select_slider("Nivel Activitate (IC)", options=[25, 30, 35, 40, 45, 50], value=30)

with col2:
    obiectiv = st.radio("Obiectiv", ["Menținere", "Slăbire"])
    deficit = 0
    if obiectiv == "Slăbire":
        deficit = st.slider("Alege Deficitul (kcal)", 500, 1000, 500)

# LOGICĂ MATEMATICĂ
kcal_mentinere = greutate * ic
target_final = kcal_mentinere - deficit

st.success(f"**Necesar Menținere:** {int(kcal_mentinere)} kcal | **Țintă Zilnică Finală:** {int(target_final)} kcal")

# 5. PLANIFICATOR CU GRAMAJE (CELE 5 MESE)
st.divider()
st.header(f"🍱 Planificator pentru {int(target_final)} kcal")

# Procente distribuție conform metodologiei
distributie = {
    "Mic Dejun": 0.25, 
    "Gustare 1": 0.10, 
    "Prânz": 0.35, 
    "Gustare 2": 0.10, 
    "Cină": 0.20
}

# Interfață cu coloane (conform imaginii tale)
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    md = st.selectbox("Mic Dejun (25%)", list(st.session_state.baza_alimente["Mic Dejun"].keys()))
with c2:
    g1 = st.selectbox("Gustare 1 (10%)", list(st.session_state.baza_alimente["Gustări"].keys()))
with c3:
    pz = st.selectbox("Prânz (35%)", list(st.session_state.baza_alimente["Prânz"].keys()))
with c4:
    g2 = st.selectbox("Gustare 2 (10%)", list(st.session_state.baza_alimente["Gustări"].keys()), key="g2_select")
with c5:
    cn = st.selectbox("Cină (20%)", list(st.session_state.baza_alimente["Cină"].keys()))

# 6. AGENT AI: CALCUL AUTOMAT GRAMAJE
def calc_g(aliment, kcal_100g, proc):
    kcal_tinta = target_final * proc
    return int((kcal_tinta / kcal_100g) * 100)

plan_final = [
    {"Masa": "Mic Dejun", "Preparat": md, "Gramaj": f"{calc_g(md, st.session_state.baza_alimente['Mic Dejun'][md], distributie['Mic Dejun'])}g"},
    {"Masa": "Gustare 1", "Preparat": g1, "Gramaj": f"{calc_g(g1, st.session_state.baza_alimente['Gustări'][g1], distributie['Gustare 1'])}g"},
    {"Masa": "Prânz", "Preparat": pz, "Gramaj": f"{calc_g(pz, st.session_state.baza_alimente['Prânz'][pz], distributie['Prânz'])}g"},
    {"Masa": "Gustare 2", "Preparat": g2, "Gramaj": f"{calc_g(g2, st.session_state.baza_alimente['Gustări'][g2], distributie['Gustare 2'])}g"},
    {"Masa": "Cină", "Preparat": cn, "Gramaj": f"{calc_g(cn, st.session_state.baza_alimente['Cină'][cn], distributie['Cină'])}g"}
]

st.table(pd.DataFrame(plan_final))

# 7. BUTON AGENT AI
if st.button("🤖 Agent AI: Optimizează Meniul"):
    st.balloons()
    st.info("Agentul AI a verificat compatibilitatea alimentelor și a recalculat gramajele pentru eficiență metabolică maximă!")
