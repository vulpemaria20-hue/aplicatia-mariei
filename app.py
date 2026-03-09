import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from fpdf import FPDF
import base64

# 1. CONFIGURARE PAGINĂ
st.set_page_config(page_title="Sistem Expert Nutriție", page_icon="🥗", layout="wide")

# 2. BAZA DE DATE (Extensibilă la 500 alimente)
# Structură: "Nume": {"kcal": val, "p": val, "l": val, "g": val} la 100g
if "baza_alimente" not in st.session_state:
    st.session_state.baza_alimente = {
        "Tocană de legume": {"kcal": 29.15, "p": 0.81, "l": 0.85, "g": 4.41},
        "Mâncare de linte": {"kcal": 188.41, "p": 11.28, "l": 2.71, "g": 31.99},
        "Iahnie de fasole": {"kcal": 282.28, "p": 17.31, "l": 5.0, "g": 37.81},
        "Somon file": {"kcal": 127.0, "p": 20.5, "l": 4.5, "g": 0.2},
        "Piept de pui (grătar)": {"kcal": 119.0, "p": 22.5, "l": 2.5, "g": 0.5},
        "Omletă": {"kcal": 155.0, "p": 12.6, "l": 10.6, "g": 1.1},
        "Humus": {"kcal": 230.9, "p": 8.07, "l": 15.16, "g": 19.09},
        "Orez integral cu legume": {"kcal": 150.4, "p": 3.7, "l": 2.5, "g": 28.2},
        "Salată de ton": {"kcal": 158.0, "p": 6.0, "l": 12.0, "g": 5.0},
        "Banana": {"kcal": 89.0, "p": 1.1, "l": 0.3, "g": 22.8},
        "Iaurt grecesc 2%": {"kcal": 65.0, "p": 8.0, "l": 2.0, "g": 3.7},
        "Kinder Felie de Lapte": {"kcal": 135.88, "p": 13.0, "l": 6.25, "g": 6.5},
        # Se pot adăuga restul până la 500 prin import CSV sau manual
    }

# 3. SECURITATE
if "login" not in st.session_state: st.session_state.login = False
if not st.session_state.login:
    st.title("🔐 Acces Protejat")
    pwd = st.text_input("Parolă:", type="password")
    if st.button("Log In"):
        if pwd == "nutrifit2026":
            st.session_state.login = True
            st.rerun()
        else: st.error("Incorect!")
    st.stop()

# 4. LOGICĂ CALCUL MATEMATIC
def calculeaza_macro(kcal_tinta, food_name, ratio):
    target_masa = kcal_tinta * ratio
    info = st.session_state.baza_alimente[food_name]
    gramaj = (target_masa / info["kcal"]) * 100
    p = (info["p"] * gramaj) / 100
    l = (info["l"] * gramaj) / 100
    g = (info["g"] * gramaj) / 100
    return round(gramaj), round(p, 1), round(l, 1), round(g, 1)

# 5. INTERFAȚA
st.sidebar.title("👤 Gestiune Client")
nume = st.sidebar.text_input("Nume Client:", "Client Nou")
if "istoric" not in st.session_state:
    st.session_state.istoric = pd.DataFrame(columns=["Data", "Greutate", "Talie"])

tab1, tab2, tab3, tab4 = st.tabs(["📊 Calculator", "📋 Fișă & Istoric", "🍱 Plan Zilnic", "PDF"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        sex = st.radio("Sex:", ["Masculin", "Feminin"])
        greutate = st.number_input("Greutate (kg):", 30.0, 200.0, 75.0)
        inaltime = st.number_input("Înălțime (cm):", 100, 220, 175)
        varsta = st.number_input("Vârstă:", 10, 100, 30)
    with c2:
        ic_val = st.select_slider("Nivel Activitate (IC):", options=[25, 30, 35, 40, 45, 50])
        obiectiv = st.selectbox("Obiectiv:", ["Slăbire (-500)", "Menținere", "Masă Musculară (+500)"])
        
    rmb = (greutate * 24) if sex == "Masculin" else (greutate * 0.8 * 24)
    tnc = greutate * ic_val
    target = tnc
    if obiectiv == "Slăbire": target = max(tnc - 500, rmb)
    elif obiectiv == "Masă Musculară": target = tnc + 500
    
    st.metric("Target Zilnic:", f"{target:.0f} kcal")
    if target <= rmb: st.warning("⚠️ Atenție: Targetul este la nivelul Metabolismului Bazal!")

with tab2:
    st.subheader("Fișă Client și Evoluție")
    with st.form("progres"):
        data_ev = st.date_input("Data:")
        gr_ev = st.number_input("Greutate actuală:", 30.0, 200.0, greutate)
        talie_ev = st.number_input("Circumferință Talie (cm):", 40, 150, 80)
        if st.form_submit_button("Salvează în istoric"):
            new_data = pd.DataFrame({"Data": [data_ev], "Greutate": [gr_ev], "Talie": [talie_ev]})
            st.session_state.istoric = pd.concat([st.session_state.istoric, new_data], ignore_index=True)
    
    if not st.session_state.istoric.empty:
        fig = px.line(st.session_state.istoric, x="Data", y="Greutate", title="Evoluție Greutate")
        st.plotly_chart(fig)

with tab3:
    st.subheader("Configurare Meniu")
    ratios = {"Mic Dejun": 0.25, "Prânz": 0.35, "Cină": 0.25, "Gustare": 0.15}
    alegeri = {}
    
    for masa, ratio in ratios.items():
        alegeri[masa] = st.selectbox(f"Alege pentru {masa}:", list(st.session_state.baza_alime.keys()), key=masa)
    
    rezultate = []
    for masa, food in alegeri.items():
        g, p, l, carbo = calculeaza_macro(target, food, ratios[masa])
        rezultate.append({"Masă": masa, "Aliment": food, "Gramaj": f"{g}g", "P": p, "L": l, "G": carbo, "Kcal": round(target*ratios[masa])})
    
    df_plan = pd.DataFrame(rezultate)
    st.table(df_plan)

with tab4:
    st.subheader("Export PDF")
    if st.button("Generează Raport PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, f"Plan Nutritional - {nume}", ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, f"Target: {target:.0f} kcal | IMC: {greutate/((inaltime/100)**2):.1f}", ln=True)
        pdf.ln(10)
        
        for res in rezultate:
            text = f"{res['Masă']}: {res['Aliment']} - {res['Gramaj']} (P:{res['P']}, L:{res['L']}, G:{res['G']})"
            pdf.cell(200, 10, text, ln=True)
            
        pdf_output = pdf.output(dest='S').encode('latin-1')
        b64 = base64.b64encode(pdf_output).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="Plan_{nume}.pdf">Descarcă PDF</a>'
        st.markdown(href, unsafe_allow_html=True)

# 6. AGENT AI (Schiță Logică)
st.sidebar.markdown("---")
if st.sidebar.button("🤖 Agent AI: Optimizează Meniul"):
    st.sidebar.write("Agentul sugerează: Crește aportul de proteine la prânz pentru a susține obiectivul de masă musculară.")
