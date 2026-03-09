import streamlit as st
import pandas as pd

# 1. CONFIGURARE PAGINĂ
st.set_page_config(page_title="Nutriția Matematică - Sistem Expert", page_icon="🍎", layout="wide")

# 2. SISTEM DE SECURITATE
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Acces Protejat - Sistem Expert")
    parola_introdusa = st.text_input("Introduceți parola de acces:", type="password")
    if st.button("Autentificare"):
        if parola_introdusa == "nutrifit2026":
            st.session_state.login = True
            st.experimental_rerun()
        else:
            st.error("Parolă incorectă!")
    st.stop()

# 3. GESTIONARE CLIENȚI
st.sidebar.title("👥 Gestiune Clienți")
nume_client = st.sidebar.text_input("Nume Client curent:", placeholder="Ex: Ion Popescu")

if not nume_client:
    st.info("Vă rugăm să introduceți numele clientului în bara laterală pentru a începe.")
    st.stop()

# 4. BAZA DE DATE REȚETE
baza_alimente = {
    "Tocană de legume": 29.15, "Mâncare de linte": 188.41, "Humus": 230.9,
    "Orez integral cu legume": 150.4, "Salată de ton": 158.0, "Omletă": 155.0,
    "Smoothie Verde": 54.2, "Smoothie Fructe Pădure": 114.6, "Smoothie Mango & Cătină": 94.2,
    "Kinder Felie de Lapte": 135.88, "Brioșe Spanac & Banană": 247.46, "Budincă Chia": 105.4,
    "Brioșe din Legume": 95.0, "Somon file": 208.0, "Iaurt grecesc 2%": 69.0, "Banana": 89.0,
    "Cod la grătar": 150.0  # am adăugat pentru cină
}

# 5. FUNCȚII DE CALCUL
def calcul_rmb(greutate, sex, varsta):
    if varsta >= 65:
        factor = 0.9 if sex == "Masculin" else 0.8
    else:
        factor = 1.0 if sex == "Masculin" else 0.8
    return factor * greutate * 24

# --- INTERFAȚA PRINCIPALĂ ---
st.title(f"⚖️ Plan Nutrițional Personalizat: {nume_client}")
tab1, tab2, tab3 = st.tabs(["📊 Calculator & IMC", "🔍 Evaluare Evoluție", "🍱 Plan Alimentar"])

# TAB 1: CALCULATOR METABOLIC
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        tip = st.selectbox("Categorie", ["Adult (18-65)", "Senior (>65)", "Copil/Adolescent"])
        greutate = st.number_input("Greutate (kg)", 10.0, 250.0, 70.0)
        inaltime = st.number_input("Înălțime (cm)", 80, 230, 170)
        varsta = st.number_input("Vârstă (ani)", 2, 100, 35)
        sex = st.radio("Sex", ["Masculin", "Feminin"])
    
    with col2:
        if tip == "Copil/Adolescent":
            if varsta < 7: tnc = 1400
            elif varsta < 10: tnc = 1800
            elif varsta < 14: tnc = 2500 if sex == "Masculin" else 2250
            else: tnc = 3250 if sex == "Masculin" else 2400
        else:
            activitate = st.selectbox("Nivel Activitate (IC)", [
                "Sedentar (25-30 kcal/kg)", "Ușor (30-35 kcal/kg)", 
                "Mediu (35-40 kcal/kg)", "Mare (40-45 kcal/kg)"
            ])
            # Extrage valoarea medie din intervalul kcal/kg
            ic_text = activitate.split("(")[1].split(" ")[0]  # "25-30"
            ic_min, ic_max = map(int, ic_text.split("-"))
            ic = (ic_min + ic_max) / 2
            tnc = greutate * ic

        obiectiv = st.radio("Obiectiv", ["Menținere", "Scădere", "Creștere"])
        target = tnc
        if obiectiv == "Scădere": target -= 500
        elif obiectiv == "Creștere": target += 500

    if st.button("Generează Analiză"):
        rmb = calcul_rmb(greutate, sex, varsta)
        bmi = greutate / ((inaltime/100)**2)
        
        st.subheader(f"Rezultate pentru {nume_client}")
        r1, r2 = st.columns(2)
        r1.metric("Target Zilnic", f"{target:.0f} kcal")
        r2.metric("RMB (Metabolism Bazal)", f"{rmb:.0f} kcal")
        
        if target < rmb:
            st.error(f"⚠️ Atenție! Targetul de {target:.0f} kcal este sub RMB. Risc de încetinire metabolică!")

# TAB 2: EVALUARE EVOLUȚIE
with tab2:
    st.subheader("Evaluarea se face la fiecare 2 săptămâni")
    c_pliuri, c_circ = st.columns(2)
    with c_pliuri:
        st.write("**Plicometrie (mm)**")
        p_tri = st.number_input("Pliu Triceps", 0.0)
        p_abd = st.number_input("Pliu Abdomen", 0.0)
    with c_circ:
        st.write("**Circumferințe (cm)**")
        talie = st.number_input("Talie", 40)
    st.info("Pierderea corectă implică scăderea greutății simultan cu a taliei.")

# TAB 3: PLAN ALIMENTAR
with tab3:
    st.subheader(f"Meniu adaptat la {target:.0f} kcal")
    dist = {"MD": 0.25, "G1": 0.10, "PZ": 0.35, "G2": 0.10, "CN": 0.20}
    
    col_a, col_b = st.columns(2)
    with col_a:
        md = st.selectbox("Mic Dejun (25%)", ["Omletă", "Smoothie Verde", "Budincă Chia", "Brioșe din Legume"])
        pz = st.selectbox("Prânz (35%)", ["Tocană de legume", "Mâncare de linte", "Somon file", "Orez integral cu legume"])
    with col_b:
        g1 = st.selectbox("Gustare (10%)", ["Banana", "Smoothie Fructe Pădure", "Brioșe Spanac & Banană"])
        cn = st.selectbox("Cină (20%)", ["Salată de ton", "Cod la grătar"])

    def calc_g(food, ratio):
        return (target * ratio / baza_alimente[food]) * 100

    plan_df = pd.DataFrame({
        "Masă": ["Mic Dejun", "Gustare", "Prânz", "Cină"],
        "Preparat": [md, g1, pz, cn],
        "Gramaj Recomandat": [f"{calc_g(md, dist['MD']):.0f}g", f"{calc_g(g1, dist['G1']):.0f}g", 
                             f"{calc_g(pz, dist['PZ']):.0f}g", f"{calc_g(cn, dist['CN']):.0f}g"]
    })
    st.table(plan_df)
