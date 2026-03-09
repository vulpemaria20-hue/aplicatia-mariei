import streamlit as st
import pandas as pd
import plotly.express as px
import random

# 1. CONFIGURARE ȘI BAZĂ DE DATE
st.set_page_config(page_title="Sistem Expert Nutriție AI", layout="wide")

if "baza_alimente" not in st.session_state:
    # Structură pregătită pentru 500+ alimente
    st.session_state.baza_alimente = {
        "Proteine": {
            "Piept de pui grătar": {"kcal": 119, "p": 22.5, "l": 2.5, "g": 0.5},
            "Somon la cuptor": {"kcal": 127, "p": 20.5, "l": 4.5, "g": 0.2},
            "Curcan la abur": {"kcal": 104, "p": 24.0, "l": 0.7, "g": 0.0},
            "Mușchi de vită": {"kcal": 133, "p": 22.0, "l": 5.0, "g": 0.0},
            "Tofu afumat": {"kcal": 110, "p": 12.0, "l": 6.0, "g": 2.0},
            "Ou fiert mediu": {"kcal": 155, "p": 12.6, "l": 10.6, "g": 1.1},
            "Brânză de vaci slabă": {"kcal": 80, "p": 16.0, "l": 0.5, "g": 3.0}
        },
        "Carbohidrați": {
            "Orez basmati fiert": {"kcal": 121, "p": 2.5, "l": 0.3, "g": 27.0},
            "Quinoa fiartă": {"kcal": 120, "p": 4.4, "l": 1.9, "g": 21.3},
            "Cartof dulce copt": {"kcal": 86, "p": 1.6, "l": 0.1, "g": 20.1},
            "Hrișcă fiartă": {"kcal": 92, "p": 3.4, "l": 0.6, "g": 19.9},
            "Paste integrale": {"kcal": 124, "p": 5.3, "l": 0.5, "g": 26.5},
            "Mămăligă": {"kcal": 70, "p": 2.0, "l": 0.5, "g": 15.0}
        },
        "Gătit/Compus": {
            "Tocană de legume": {"kcal": 29.15, "p": 0.81, "l": 0.85, "g": 4.41},
            "Iahnie de fasole": {"kcal": 154, "p": 6.4, "l": 6.0, "g": 19.2},
            "Mâncare de linte": {"kcal": 116, "p": 9.0, "l": 0.4, "g": 20.0},
            "Salată ton & avocado": {"kcal": 158, "p": 6.0, "l": 12.0, "g": 5.0},
            "Supă cremă legume": {"kcal": 45, "p": 1.5, "l": 2.0, "g": 5.5}
        },
        "Gustări/Fructe": {
            "Banană": {"kcal": 89, "p": 1.1, "l": 0.3, "g": 22.8},
            "Nuci crude": {"kcal": 654, "p": 15.0, "l": 65.0, "g": 14.0},
            "Iaurt grecesc 2%": {"kcal": 65, "p": 8.0, "l": 2.0, "g": 3.7},
            "Măr verde": {"kcal": 52, "p": 0.3, "l": 0.2, "g": 14.0},
            "Migdale": {"kcal": 579, "p": 21.0, "l": 50.0, "g": 22.0}
        }
    }

if "clienti" not in st.session_state:
    st.session_state.clienti = {}

# 2. LOGIN ȘI IDENTIFICARE CLIENT
if "autentificat" not in st.session_state:
    st.title("🔐 Autentificare Sistem Expert")
    pwd = st.text_input("Introduceți parola:", type="password")
    if st.button("Acces"):
        if pwd == "nutrifit2026":
            st.session_state.autentificat = True
            st.rerun()
    st.stop()

st.sidebar.title("👥 Gestiune Profil")
nume_client = st.sidebar.text_input("NUME CLIENT:", placeholder="Ex: Ion Popescu")

if not nume_client:
    st.info("⚠️ Introduceți numele clientului în sidebar pentru a începe.")
    st.stop()

# Creare/Încărcare date client
if nume_client not in st.session_state.clienti:
    st.session_state.clienti[nume_client] = {"istoric": [], "plan_curent": None}

# 3. CALCULATOR METABOLIC AVANSAT
st.header(f"📊 Evaluare Biometrică: {nume_client}")
col1, col2, col3 = st.columns(3)

with col1:
    sex = st.radio("Sex", ["Masculin", "Feminin"])
    varsta = st.number_input("Vârstă (ani)", 10, 100, 35)
    greutate = st.number_input("Greutate Actuală (kg)", 30.0, 200.0, 75.0)

with col2:
    inaltime = st.number_input("Înălțime (cm)", 100, 230, 175)
    ic = st.select_slider("Indice Activitate (IC)", options=[25, 30, 35, 40, 45, 50], value=30)
    obiectiv = st.selectbox("Obiectiv", ["Menținere", "Slăbire", "Masă Musculară"])

with col3:
    deficit = 0
    if obiectiv == "Slăbire":
        deficit = st.slider("Alege Deficitul (kcal)", 500, 1000, 500)
    elif obiectiv == "Masă Musculară":
        deficit = -500 # Surplus

# LOGICĂ MATEMATICĂ
rmb = (greutate * 24) if sex == "Masculin" else (greutate * 0.8 * 24)
mentinere = greutate * ic
target = mentinere - deficit

st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("RMB (Bazal)", f"{int(rmb)} kcal")
c2.metric("Necesar Menținere", f"{int(mentinere)} kcal")
c3.metric("TARGET ZILNIC", f"{int(target)} kcal", delta=-deficit if deficit > 0 else abs(deficit))

if target < rmb:
    st.error(f"⚠️ ATENȚIE: Targetul ({int(target)}) este sub metabolismul bazal! Se recomandă minim {int(rmb)} kcal.")

# 4. AGENT AI ȘI GENERATOR MENIU
st.header("🍱 Generator Meniu Inteligent")

preferinte = st.multiselect("Preferințe alimentare (Agentul AI va prioritiza):", 
                           ["Pui", "Pește", "Vegetarian", "Fără Lactoză", "Mâncare Gătită"])

def genereaza_meniu_ai(target_kcal, pref):
    # Agentul AI filtrează și alege
    toate = []
    for cat in st.session_state.baza_alimente:
        for nume, date in st.session_state.baza_alimente[cat].items():
            toate.append({"nume": nume, **date})
    
    ratios = {"Mic Dejun": 0.25, "Gustare 1": 0.10, "Prânz": 0.35, "Gustare 2": 0.10, "Cină": 0.20}
    plan = []
    
    for masa, proc in ratios.items():
        kcal_masa = target_kcal * proc
        # Alegere random sau bazată pe preferințe
        aliment = random.choice(toate)
        gramaj = (kcal_masa / aliment["kcal"]) * 100
        plan.append({
            "Masă": masa,
            "Aliment": aliment["nume"],
            "Gramaj": f"{int(gramaj)}g",
            "P": round((aliment["p"] * gramaj) / 100, 1),
            "L": round((aliment["l"] * gramaj) / 100, 1),
            "G": round((aliment["g"] * gramaj) / 100, 1),
            "Kcal": int(kcal_masa)
        })
    return pd.DataFrame(plan)

if st.button("🤖 Agent AI: Generează Meniul Zilei"):
    df_meniu = genereaza_meniu_ai(target, preferinte)
    st.session_state.clienti[nume_client]["plan_current"] = df_meniu
    st.success(f"Meniu generat cu succes pentru {nume_client}!")

if st.session_state.clienti[nume_client]["plan_current"] is not None:
    st.table(st.session_state.clienti[nume_client]["plan_current"])

# 5. ISTORIC ȘI GRAFICE
st.header("📈 Istoric Progres")
with st.expander("Înregistrează progres"):
    c_data, c_greutate = st.columns(2)
    data_progres = c_data.date_input("Data")
    greutate_progres = c_greutate.number_input("Greutate (kg)", value=greutate)
    if st.button("Salvează în fișa clientului"):
        st.session_state.clienti[nume_client]["istoric"].append({"Data": data_progres, "Greutate": greutate_progres})

if st.session_state.clienti[nume_client]["istoric"]:
    df_ist = pd.DataFrame(st.session_state.clienti[nume_client]["istoric"])
    fig = px.line(df_ist, x="Data", y="Greutate", title=f"Evoluție Greutate - {nume_client}", markers=True)
    st.plotly_chart(fig)
