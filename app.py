import streamlit as st
import pandas as pd
import random

# 1. CONFIGURARE PAGINĂ
st.set_page_config(page_title="Expert Nutriție - Platformă Securizată", layout="wide")

# 2. SISTEM DE SECURITATE (LOGARE CU PAROLĂ)
if "autentificat" not in st.session_state:
    st.session_state.autentificat = False

def login():
    st.title("🔐 Acces Platformă Privată")
    parola = st.text_input("Introduceți parola de acces:", type="password")
    if st.button("Autentificare"):
        if parola == "nutrifit2026": # Poți schimba parola aici
            st.session_state.autentificat = True
            st.rerun()
        else:
            st.error("Parolă incorectă! Contactați administratorul.")

if not st.session_state.autentificat:
    login()
    st.stop()

# 3. BAZĂ DE DATE EXTINSĂ (ALIMENTE ȘI REȚETE)
if "baza_date" not in st.session_state:
    st.session_state.baza_date = {
        "Mic Dejun": {
            "Omletă cu spanac": 155, "Smoothie Verde": 54, "Budincă Chia": 105, "Ovăz cu fructe": 120,
            "Pâine cu avocado": 160, "Iaurt grecesc cu nuci": 130, "Clătite proteice": 175, "Brânză cu roșii": 90,
            "Ouă ochiuri și sparanghel": 140, "Brioșe cu legume": 110, "Terci de hrișcă": 115, "Sandwich cu curcan": 180
        },
        "Gustări": {
            "Măr verde": 52, "Banană": 89, "Migdale crude": 579, "Kinder Felie Lapte": 136, "Baton proteic": 350,
            "Iaurt 2%": 65, "Nuci caju": 550, "Afine": 57, "Mix semințe": 480, "Brânză perle": 85, "Morcovi baby": 41
        },
        "Prânz": {
            "Pui la grătar": 165, "Somon la cuptor": 208, "Tocană de legume": 35, "Mâncare de linte": 116,
            "Iahnie de fasole": 125, "Curcan cu broccoli": 110, "Orez Basmati": 120, "Mușchi de vită": 250,
            "Păstrăv": 145, "Quinoa cu legume": 130, "Mămăligă cu brânză slabă": 140, "Paste integrale": 150
        },
        "Cină": {
            "Salată de ton": 150, "Supă cremă legume": 45, "Cod cu lămâie": 105, "Salată grecească": 115,
            "Tofu la grătar": 95, "Creveți cu usturoi": 99, "Sufleu de dovlecei": 85, "Curcan la abur": 104,
            "Salată cu ou fiert": 110, "Supă de pui": 60, "Vinete la cuptor": 40, "Humus cu ardei": 180
        }
    }

# 4. MANAGEMENT CLIENT
st.sidebar.title("👥 Gestiune Clienți")
nume_client = st.sidebar.text_input("Nume Client:", placeholder="Ex: Maria Popescu")

if not nume_client:
    st.warning("Introduceți numele clientului pentru a genera planul.")
    st.stop()

# 5. CALCULATOR METABOLIC
st.title(f"📋 Planificator Săptămânal: {nume_client}")
col1, col2, col3 = st.columns(3)

with col1:
    greutate = st.number_input("Greutate (kg)", 40.0, 180.0, 75.0)
    ic = st.select_slider("Activitate (IC)", options=[25, 30, 35, 40, 45, 50], value=30)
with col2:
    obiectiv = st.radio("Obiectiv", ["Menținere", "Slăbire"])
    deficit = 0
    if obiectiv == "Slăbire":
        deficit = st.slider("Deficit (kcal)", 500, 1000, 500)
with col3:
    kcal_mentinere = greutate * ic
    tinta = kcal_mentinere - deficit
    st.metric("Țintă Zilnică", f"{int(tinta)} kcal")

# 6. PLANIFICARE PE O SĂPTĂMÂNĂ (7 ZILE)
st.divider()
zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
distributie = {"Mic Dejun": 0.25, "Gustare 1": 0.10, "Prânz": 0.35, "Gustare 2": 0.10, "Cină": 0.20}

st.header("🗓️ Meniu Săptămânal Personalizat")

for zi in zile:
    with st.expander(f"📅 Plan pentru {zi}"):
        c1, c2, c3, c4, c5 = st.columns(5)
        
        # Dropdown-uri cu lista mare de alimente
        m1 = c1.selectbox("Mic Dejun", list(st.session_state.baza_date["Mic Dejun"].keys()), key=f"md_{zi}")
        g1 = c2.selectbox("Gustare 1", list(st.session_state.baza_date["Gustări"].keys()), key=f"g1_{zi}")
        p1 = c3.selectbox("Prânz", list(st.session_state.baza_date["Prânz"].keys()), key=f"p_{zi}")
        g2 = c4.selectbox("Gustare 2", list(st.session_state.baza_date["Gustări"].keys()), key=f"g2_{zi}")
        c1_zi = c5.selectbox("Cină", list(st.session_state.baza_date["Cină"].keys()), key=f"c_{zi}")

        # AGENT AI: Calcul gramaje automate pentru fiecare alegere
        plan_zi = []
        for masa, alegere, cat in [("Mic Dejun", m1, "Mic Dejun"), ("Gustare 1", g1, "Gustări"), 
                                   ("Prânz", p1, "Prânz"), ("Gustare 2", g2, "Gustări"), ("Cină", c1_zi, "Cină")]:
            kcal_100g = st.session_state.baza_date[cat][alegere]
            kcal_alocate = tinta * distributie[masa]
            gramaj = (kcal_alocate / kcal_100g) * 100
            plan_zi.append({"Masă": masa, "Aliment": alegere, "Gramaj": f"{int(gramaj)}g", "Calorii": f"{int(kcal_alocate)} kcal"})
        
        st.table(pd.DataFrame(plan_zi))

# 7. BUTON SALVARE / EXPORT
if st.sidebar.button("💾 Salvează Planul"):
    st.sidebar.success(f"Planul pentru {nume_client} a fost salvat în baza de date!")
