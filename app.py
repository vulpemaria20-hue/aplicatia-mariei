import streamlit as st
import pandas as pd
import random

# 1. CONFIGURARE ȘI BAZĂ DE DATE (EXTENSIBILĂ LA 500)
st.set_page_config(page_title="Sistem Expert Nutriție AI", layout="wide")

if "baza_alimente" not in st.session_state:
    st.session_state.baza_alimente = {
        "Proteine": {
            "Piept de pui": {"kcal": 119, "p": 22.5, "l": 2.5, "g": 0.5},
            "Somon": {"kcal": 127, "p": 20.5, "l": 4.5, "g": 0.2},
            "Curcan": {"kcal": 104, "p": 24.0, "l": 0.7, "g": 0.0},
            "Ou fiert": {"kcal": 155, "p": 12.6, "l": 10.6, "g": 1.1},
            "Tofu": {"kcal": 91, "p": 10, "l": 6, "g": 2},
            "Brânză vaci slabă": {"kcal": 80, "p": 16, "l": 0.5, "g": 3}
        },
        "Carbohidrați": {
            "Orez Basmati": {"kcal": 121, "p": 2.5, "l": 0.3, "g": 27.0},
            "Quinoa": {"kcal": 120, "p": 4.4, "l": 1.9, "g": 21.3},
            "Cartof dulce": {"kcal": 86, "p": 1.6, "l": 0.1, "g": 20.1},
            "Hrișcă": {"kcal": 92, "p": 3.4, "l": 0.6, "g": 19.9},
            "Paste integrale": {"kcal": 124, "p": 5.3, "l": 0.5, "g": 26.5}
        },
        "Rețete Compuse/Gătite": {
            "Tocană de legume": {"kcal": 29.15, "p": 0.81, "l": 0.85, "g": 4.41},
            "Iahnie de fasole": {"kcal": 154, "p": 6.4, "l": 6.0, "g": 19.2},
            "Mâncare de linte": {"kcal": 116, "p": 9.0, "l": 0.4, "g": 20.0},
            "Supă cremă legume": {"kcal": 45, "p": 1.5, "l": 2.0, "g": 5.5},
            "Humus": {"kcal": 230, "p": 8, "l": 15, "g": 19}
        }
    }

# 2. IDENTIFICARE CLIENT (SIDEBAR)
st.sidebar.title("👤 Management Client")
nume_client = st.sidebar.text_input("Nume Complet Client:", placeholder="Ex: Maria Ionescu")

if not nume_client:
    st.warning("⬅️ Introduceți numele clientului în bara laterală pentru a activa aplicația.")
    st.stop()

# 3. CALCULATOR METABOLIC (CALORII INIȚIALE)
st.title(f"Planificator Nutrițional: {nume_client}")

col1, col2 = st.columns(2)
with col1:
    sex = st.selectbox("Sex", ["Feminin", "Masculin"])
    greutate = st.number_input("Greutate Actuală (kg)", 30.0, 200.0, 70.0)
    inaltime = st.number_input("Înălțime (cm)", 100, 230, 170)
    varsta = st.number_input("Vârstă (ani)", 15, 90, 30)

with col2:
    ic = st.select_slider("Nivel Activitate (IC)", options=[25, 30, 35, 40, 45, 50], value=30, 
                          help="25-30: Sedentar, 35-40: Mediu, 45-50: Foarte Activ")
    obiectiv = st.radio("Obiectiv Principal", ["Menținere", "Slăbire", "Masă Musculară"])
    
    deficit = 0
    if obiectiv == "Slăbire":
        deficit = st.slider("Alege Deficitul Caloric (kcal)", 500, 1000, 500)
    elif obiectiv == "Masă Musculară":
        deficit = -500 # Surplus

# LOGICĂ MATEMATICĂ
rmb = (greutate * 24) if sex == "Masculin" else (greutate * 0.8 * 24)
initiale_mentinere = greutate * ic
target_final = initiale_mentinere - deficit

st.info(f"**Analiză Metabolică:** Menținere la {int(initiale_mentinere)} kcal | RMB: {int(rmb)} kcal")
st.success(f"### Target Zilnic Final: {int(target_final)} kcal")

# 4. AGENT AI ȘI GENERARE MENIU
st.divider()
st.header("🤖 Agent AI: Generare Meniu Personalizat")

if st.button("Generează Plan Alimentar Automat"):
    # Colectăm toate alimentele într-o listă pentru Agentul AI
    toate_alimentele = []
    for cat in st.session_state.baza_alimente:
        for nume, date in st.session_state.baza_alimente[cat].items():
            toate_alimentele.append({"nume": nume, **date})

    # Distribuția caloriilor pe mese
    distributie = {"Mic Dejun": 0.25, "Prânz": 0.35, "Cină": 0.25, "Gustări": 0.15}
    meniu_rezultat = []

    for masa, procent in distributie.items():
        kcal_masa = target_final * procent
        # Agentul AI alege un aliment aleatoriu (poate fi filtrat ulterior pe preferințe)
        ales = random.choice(toate_alimentele)
        
        # Calcul gramaj și macro
        gramaj = (kcal_masa / ales["kcal"]) * 100
        p = (ales["p"] * gramaj) / 100
        l = (ales["l"] * gramaj) / 100
        g = (ales["g"] * gramaj) / 100
        
        meniu_rezultat.append({
            "Masă": masa,
            "Aliment": ales["nume"],
            "Gramaj": f"{int(gramaj)}g",
            "Proteine (g)": round(p, 1),
            "Lipide (g)": round(l, 1),
            "Glucide (g)": round(g, 1),
            "Kcal": int(kcal_masa)
        })

    st.table(pd.DataFrame(meniu_rezultat))
    st.caption(f"Plan generat automat pentru {nume_client} conform Matematicii Nutriției.")

# 5. LISTA COMPLETĂ DE ALIMENTE (PENTRU CONSULTARE)
with st.expander("📂 Vezi Baza de Date (Alimente și Rețete)"):
    for cat, items in st.session_state.baza_alimente.items():
        st.write(f"**{cat}**")
        st.json(items)
