import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import base64

# --- CONFIGURARE ---
st.set_page_config(page_title="Expert Nutriție Pro", layout="wide")

# --- BAZA DE DATE (Exemplu extins - se pot adăuga până la 500) ---
if "baza_alimente" not in st.session_state:
    st.session_state.baza_alimente = {
        "Proteine": {
            "Piept de pui (grătar)": {"kcal": 119, "p": 22.5, "l": 2.5, "g": 0.5},
            "Somon file": {"kcal": 127, "p": 20.5, "l": 4.5, "g": 0.2},
            "Mușchi de porc": {"kcal": 145, "p": 21, "l": 5.5, "g": 1.5},
            "Ou fiert": {"kcal": 155, "p": 12.6, "l": 10.6, "g": 1.1},
            "Tofu": {"kcal": 91, "p": 10, "l": 6, "g": 2},
        },
        "Carbohidrați/Leguminoase": {
            "Orez integral": {"kcal": 111, "p": 2.6, "l": 0.9, "g": 23},
            "Mâncare de linte": {"kcal": 188.41, "p": 11.28, "l": 2.71, "g": 31.99},
            "Iahnie de fasole": {"kcal": 282.28, "p": 17.31, "l": 5.0, "g": 37.81},
            "Cartof dulce copt": {"kcal": 86, "p": 1.6, "l": 0.1, "g": 20.1},
            "Quinoa fiartă": {"kcal": 65, "p": 7.5, "l": 2.4, "g": 1.6},
        },
        "Rețete Compuse/Mese": {
            "Tocană de legume": {"kcal": 29.15, "p": 0.81, "l": 0.85, "g": 4.41},
            "Humus": {"kcal": 230.9, "p": 8.07, "l": 15.16, "g": 19.09},
            "Salată de ton": {"kcal": 158, "p": 6, "l": 12, "g": 5},
            "Supă cremă legume": {"kcal": 16.65, "p": 0.46, "l": 0.48, "g": 2.52},
        },
        "Gustări/Desert": {
            "Banana": {"kcal": 89, "p": 1.1, "l": 0.3, "g": 22.8},
            "Nuci crude": {"kcal": 654, "p": 15.2, "l": 65.2, "g": 13.7},
            "Kinder Felie Lapte (Proteic)": {"kcal": 135.88, "p": 13, "l": 6.25, "g": 6.5},
            "Iaurt grecesc 2%": {"kcal": 65, "p": 8, "l": 2, "g": 3.7},
        }
    }

# --- GESTIUNE SESIUNE ---
if "clienti" not in st.session_state: st.session_state.clienti = {}
if "login" not in st.session_state: st.session_state.login = False

# --- LOGIN ---
if not st.session_state.login:
    st.title("🔐 Autentificare")
    if st.text_input("Parolă", type="password") == "nutrifit2026":
        if st.button("Intră"):
            st.session_state.login = True
            st.rerun()
    st.stop()

# --- SIDEBAR: SELECTARE CLIENT ---
st.sidebar.title("👥 Management Clienți")
nume_client = st.sidebar.text_input("Caută/Adaugă Client:", placeholder="Nume Complet")

if nume_client:
    if nume_client not in st.session_state.clienti:
        st.session_state.clienti[nume_client] = {"istoric": [], "biometrie": {}}
        st.sidebar.success(f"Client nou creat: {nume_client}")
    
    current_client = st.session_state.clienti[nume_client]
else:
    st.warning("Introduceți numele clientului pentru a începe.")
    st.stop()

# --- INTERFAȚĂ PRINCIPALĂ ---
st.title(f"Planificator: {nume_client}")
tab_calc, tab_plan, tab_progres = st.tabs(["📊 Calculator Metabolic", "🍱 Planificator Mese", "📈 Progres & Istoric"])

# --- TAB 1: CALCULATOR ---
with tab_calc:
    col1, col2 = st.columns(2)
    with col1:
        sex = st.selectbox("Sex", ["Masculin", "Feminin"])
        greutate = st.number_input("Greutate (kg)", 30.0, 200.0, 70.0)
        inaltime = st.number_input("Înălțime (cm)", 100, 220, 170)
        varsta = st.number_input("Vârstă", 10, 100, 30)
    with col2:
        ic = st.select_slider("Activitate (IC)", options=[25, 30, 35, 40, 45, 50])
        obiectiv = st.radio("Obiectiv", ["Slăbire", "Menținere", "Masă Musculară"])

    rmb = (greutate * 24) if sex == "Masculin" else (greutate * 0.8 * 24)
    target = greutate * ic
    if obiectiv == "Slăbire": target = max(target - 500, rmb)
    elif obiectiv == "Masă Musculară": target += 500
    
    st.metric("Necesar Zilnic", f"{target:.0f} kcal")
    current_client["biometrie"] = {"target": target, "greutate": greutate}

# --- TAB 2: PLANIFICATOR (ALIMENTARE DIN BAZA DE DATE) ---
with tab_plan:
    st.subheader("Construiește meniul din baza de date")
    
    # Creăm o listă unică cu toate alimentele din toate categoriile
    toate_alimentele = {}
    for cat in st.session_state.baza_alimente:
        toate_alimentele.update(st.session_state.baza_alimente[cat])
    
    list_nume_alimente = list(toate_alimentele.keys())
    
    ratios = {"Mic Dejun (25%)": 0.25, "Prânz (35%)": 0.35, "Cină (25%)": 0.25, "Gustare (15%)": 0.15}
    meniu_ales = []

    for masa, proc in ratios.items():
        c_m1, c_m2 = st.columns([2, 1])
        with c_m1:
            aliment = st.selectbox(f"Selectează {masa}:", list_nume_alimente, key=f"sel_{masa}")
        
        info = toate_alimentele[aliment]
        calorii_alocate = target * proc
        gramaj = (calorii_alocate / info["kcal"]) * 100
        p = (info["p"] * gramaj) / 100
        l = (info["l"] * gramaj) / 100
        g = (info["g"] * gramaj) / 100
        
        meniu_ales.append({
            "Masa": masa, "Aliment": aliment, "Gramaj": f"{int(gramaj)}g", 
            "P (g)": round(p, 1), "L (g)": round(l, 1), "G (g)": round(g, 1), "Kcal": int(calorii_alocate)
        })

    df_meniu = pd.DataFrame(meniu_ales)
    st.table(df_meniu)

# --- TAB 3: ISTORIC ---
with tab_progres:
    if st.button("Salvează Greutatea Azi"):
        current_client["istoric"].append({"Data": pd.Timestamp.now().strftime("%Y-%m-%d"), "Greutate": greutate})
        st.success("Date salvate!")
    
    if current_client["istoric"]:
        df_ist = pd.DataFrame(current_client["istoric"])
        st.plotly_chart(px.line(df_ist, x="Data", y="Greutate", title=f"Evoluție {nume_client}"))
