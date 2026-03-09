import streamlit as st
import pandas as pd

# CONFIGURARE PAGINĂ
st.set_page_config(page_title="Sistem Expert Nutriție - Vasile Bogdan", page_icon="⚖️", layout="wide")

# --- BAZA DE DATE REȚETE ȘI ALIMENTE (Date din Pag. 32-107) ---
baza_alimente = {
    "Tocană de legume": 29.15, "Mâncare de linte": 188.41, "Humus": 230.9,
    "Orez integral cu legume": 150.4, "Iahnie de fasole": 154.1, "Supă de pui": 24.14,
    "Salată de ton cu avocado": 158.0, "Omletă simplă": 155.0, "Piept de pui grătar": 165.0,
    "Somon file": 208.0, "Cartofi dulci copți": 116.0, "Iaurt grecesc 2%": 69.0,
    "Banana": 89.0, "Migdale crude": 575.0, "Pâine integrală": 223.3,
    "Smoothie Verde": 54.2, "Smoothie Fructe Pădure": 114.6, "Smoothie Mango & Cătină": 94.2,
    "Kinder Felie de Lapte": 135.88, "Brioșe Spanac & Banană": 247.46, "Budincă Chia & Zmeură": 105.4,
    "Brioșe din Legume": 95.0, "Cod la grătar": 107.0, "Budincă Brânză Vaci": 164.0
}

# --- FUNCȚII DE CALCUL CONFORM SURSELOR ---

def calcul_rmb(greutate, sex, varsta):
    if varsta >= 65: # RMB Seniori (Pag. 50/12)
        return (0.9 if sex == "Masculin" else 0.8) * greutate * 24
    else: # RMB Adulți (Pag. 12/1)
        return (1.0 if sex == "Masculin" else 0.8) * greutate * 24

def interpreteaza_imc(varsta, sex, imc):
    if varsta < 18: # Tabel BMI Copii (Pag. 54/12)
        tabel = {
            "Masculin": {2: 18.8, 8: 19.3, 14: 24.8, 18: 27.9},
            "Feminin": {2: 18.7, 8: 19.8, 14: 26.0, 18: 28.7}
        }
        limit_obez = tabel[sex].get(varsta, 25.0)
        return "Obezitate" if imc >= limit_obez else "Normoponderal/Altul"
    else: # Tabel IMC Adulți (Pag. 52/12)
        if imc < 18.5: return "Subponderal"
        elif imc < 25: return "Normoponderal"
        elif imc < 30: return "Supraponderal"
        else: return "Obezitate"

# --- INTERFAȚĂ ---
st.title("⚖️ Sistem Expert - Matematica Nutriției")
st.sidebar.header("🔐 Autentificare")
parola = st.sidebar.text_input("Cod acces", type="password")

if parola == "nutrifit2026":
    tab1, tab2, tab3 = st.tabs(["📊 Calculator & IMC", "🔍 Evaluare Evoluție", "🍱 Plan Alimentar"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            greutate = st.number_input("Greutate Actuală (kg)", 10.0, 200.0, 75.0)
            inaltime = st.number_input("Înălțime (cm)", 80, 230, 175)
            varsta = st.number_input("Vârstă", 2, 100, 35)
            sex = st.radio("Sex", ["Masculin", "Feminin"])
        
        with col2:
            activitate = st.selectbox("Nivel Activitate (IC)", 
                ["Sedentar (25-30)", "Ușor (30-35)", "Mediu (35-40)", "Mare (40-45)", "Foarte Mare (45-50)"])
            ic = int(activitate.split("(")[1].split("-"))
            tnc = greutate * ic # Formula GA x IC (Pag. 8/7)
            obiectiv = st.selectbox("Obiectiv", ["Menținere", "Scădere", "Creștere"])
            
            target = tnc
            if obiectiv == "Scădere": target -= 500
            elif obiectiv == "Creștere": target += 500

        if st.button("Calculează"):
            bmi = greutate / ((inaltime/100)**2)
            rmb = calcul_rmb(greutate, sex, varsta)
            status = interpreteaza_imc(varsta, sex, bmi)
            
            st.success(f"**Target Zilnic:** {target:.0f} kcal")
            # LINIA CORECTATĂ MAI JOS:
            st.info(f"**Indice de Masă Corporală:** {bmi:.1f} ({status})")
            if target < rmb:
                st.warning(f"Atenție: Target sub RMB ({rmb:.0f} kcal)!")

    with tab2:
        st.subheader("🔍 Evaluare o dată la 2 săptămâni (Pag. 113)")
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Circumferințe (cm)**")
            talie = st.number_input("Talie")
            coapsa = st.number_input("Coapsă")
        with c2:
            st.write("**Plicometrie (mm)**")
            p_tri = st.number_input("Triceps")
            p_abd = st.number_input("Abdomen")
            st.info(f"Media pliurilor: {(p_tri + p_abd)/2:.1f} mm")

    with tab3:
        st.subheader(f"🍱 Meniu adaptat pentru {target:.0f} kcal")
        dist = {"MD": 0.25, "G1": 0.10, "PZ": 0.35, "G2": 0.10, "CN": 0.20}
        
        col_m, col_g = st.columns(2)
        with col_m:
            md_sel = st.selectbox("Mic Dejun", ["Omletă simplă", "Smoothie Verde", "Budincă Chia & Zmeură"])
            pz_sel = st.selectbox("Prânz", ["Tocană de legume", "Somon file", "Mâncare de linte"])
        with col_g:
            g1_sel = st.selectbox("Gustare 1", ["Banana", "Smoothie Fructe Pădure", "Migdale crude"])
            cn_sel = st.selectbox("Cină", ["Supă de pui", "Cod la grătar", "Salată de ton cu avocado"])

        def calc_g(aliment, ratio):
            return (target * ratio / baza_alimente[aliment]) * 100

        res = pd.DataFrame({
            "Masă": ["Mic Dejun", "Gustare 1", "Prânz", "Cină"],
            "Preparat": [md_sel, g1_sel, pz_sel, cn_sel],
            "Gramaj Recomandat": [f"{calc_g(md_sel, dist['MD']):.0f}g", f"{calc_g(g1_sel, dist['G1']):.0f}g", 
                                 f"{calc_g(pz_sel, dist['PZ']):.0f}g", f"{calc_g(cn_sel, dist['CN']):.0f}g"]
        })
        st.table(res)
else:
    st.warning("Introduceți parola corectă în bara laterală.")
