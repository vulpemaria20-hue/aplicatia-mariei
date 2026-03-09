import streamlit as st
import pandas as pd

# CONFIGURARE PAGINĂ
st.set_page_config(page_title="Nutriția Matematică - Sistem Expert", page_icon="⚖️", layout="wide")

# --- BAZA DE DATE REȚETE (Kcal/100g conform Pag. 32-107) ---
baza_alimente = {
    "Tocană de legume": 29.15, "Mâncare de linte": 188.41, "Humus": 230.9,
    "Orez integral cu legume": 150.4, "Supă de pui": 24.14, "Salată de ton": 158.0,
    "Omletă simplă": 155.0, "Piept de pui grătar": 165.0, "Somon file": 208.0,
    "Smoothie Verde": 54.2, "Smoothie Fructe Pădure": 114.6, "Smoothie Mango & Cătină": 94.2,
    "Kinder Felie de Lapte": 135.88, "Brioșe Spanac & Banană": 247.46, "Budincă Chia & Zmeură": 105.4,
    "Brioșe din Legume": 95.0, "Cod la grătar": 107.0, "Iaurt grecesc 2%": 69.0, "Banana": 89.0
}

# --- FUNCȚII DE CALCUL ---
def calcul_rmb(greutate, sex, varsta):
    if varsta >= 65: # Formula RMB Seniori (Pag. 50)
        factor = 0.9 if sex == "Masculin" else 0.8
    else: # Formula RMB Adulți (Pag. 10)
        factor = 1.0 if sex == "Masculin" else 0.8
    return factor * greutate * 24

# --- GESTIONARE SESIUNE CLIENȚI ---
if "baza_clienti" not in st.session_state:
    st.session_state.baza_clienti = {}

# --- BARA LATERALĂ (LOGISTICĂ CLIENȚI) ---
st.sidebar.title("👥 Gestiune Clienți")
nume_client = st.sidebar.text_input("Nume Client", placeholder="Introduceți numele...")
if not nume_client:
    st.info("Introduceți numele clientului pentru a activa sistemul.")
    st.stop()

# --- INTERFAȚA PRINCIPALĂ ---
st.title(f"⚖️ Analiză Nutrițională: {nume_client}")
tab1, tab2, tab3 = st.tabs(["📊 Calculator & IMC", "🔍 Evaluare Evoluție", "🍱 Plan Alimentar"])

# TAB 1: CALCULATOR METABOLIC
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        tip = st.selectbox("Categorie", ["Adult (18-65)", "Senior (>65)", "Copil/Adolescent"])
        greutate = st.number_input("Greutate (kg)", 10.0, 250.0, 70.0)
        inaltime = st.number_input("Înălțime (cm)", 80, 230, 170)
        varsta = st.number_input("Vârstă (ani)", 2, 100, 35)
        sex = st.radio("Sex", ["Masculin", "Feminin"])
    
    with c2:
        if tip == "Copil/Adolescent":
            st.info("Necesar caloric fix conform vârstei (Pag. 26).")
            if varsta < 7: tnc = 1400
            elif varsta < 10: tnc = 1800
            elif varsta < 14: tnc = 2500 if sex == "Masculin" else 2250
            else: tnc = 3250 if sex == "Masculin" else 2400
        else:
            activitate = st.selectbox("Activitate (IC)", [
                "Sedentar (25-30 kcal/kg)", "Ușor (30-35 kcal/kg)", 
                "Mediu (35-40 kcal/kg)", "Mare (40-45 kcal/kg)"
            ])
            # REZOLVARE EROARE: folosim index [2] și split corect
            ic = int(activitate.split("(")[2].split("-")) 
            tnc = greutate * ic # Formula GA x IC (Pag. 8)

        obiectiv = st.radio("Obiectiv", ["Menținere", "Scădere", "Creștere"])
        target = tnc
        if obiectiv == "Scădere": target -= 500
        elif obiectiv == "Creștere": target += 500

    if st.button("Generează Raport"):
        rmb = calcul_rmb(greutate, sex, varsta)
        bmi = greutate / ((inaltime/100)**2)
        st.session_state.baza_clienti[nume_client] = {"target": target, "bmi": bmi}
        
        st.subheader("Rezultate Raport")
        res1, res2 = st.columns(2)
        res1.metric("Target Zilnic", f"{target:.0f} kcal")
        res2.metric("RMB (Bazal)", f"{rmb:.0f} kcal")
        if target < rmb:
            st.error(f"⚠️ Atenție! Targetul este sub RMB ({rmb:.0f}). Risc de încetinire metabolică!")

# TAB 2: EVALUARE EVOLUȚIE (Pag. 67-113)
with tab2:
    st.subheader(f"Monitorizare Progres: {nume_client}")
    col_pliuri, col_circ = st.columns(2)
    with col_pliuri:
        st.write("**Plicometrie (mm)**")
        p_abd = st.number_input("Abdomen", 0.0, 60.0)
        p_tri = st.number_input("Triceps", 0.0, 60.0)
        media = (p_abd + p_tri) / 2
        st.info(f"Media pliurilor: {media:.1f} mm")
    with col_circ:
        st.write("**Circumferințe (cm)**")
        talie = st.number_input("Talie", 40, 150)
        st.write("Evaluarea se face la fiecare 2 săptămâni.")

# TAB 3: PLAN ALIMENTAR
with tab3:
    st.subheader(f"Configurare Meniu: {target:.0f} kcal")
    dist = {"MD": 0.25, "G1": 0.10, "PZ": 0.35, "G2": 0.10, "CN": 0.20}
    
    # Selecție rețete profesionale
    col_a, col_b = st.columns(2)
    with col_a:
        md_sel = st.selectbox("Mic Dejun (25%)", ["Omletă simplă", "Smoothie Verde", "Budincă Chia & Zmeură", "Brioșe din Legume"])
        pz_sel = st.selectbox("Prânz (35%)", ["Tocană de legume", "Mâncare de linte", "Somon file", "Orez integral cu legume"])
    with col_b:
        g1_sel = st.selectbox("Gustare (10%)", ["Banana", "Smoothie Fructe Pădure", "Brioșe Spanac & Banană"])
        cn_sel = st.selectbox("Cină (20%)", ["Salată de ton", "Supă de pui", "Cod la grătar"])

    # Calcul gramaje automate (Formula Pag. 117)
    def calc_g(food, ratio):
        return (target * ratio / baza_alimente.get(food, 100)) * 100

    plan_df = pd.DataFrame({
        "Masa": ["Mic Dejun", "Gustare 1", "Prânz", "Cină"],
        "Preparat": [md_sel, g1_sel, pz_sel, cn_sel],
        "Gramaj": [f"{calc_g(md_sel, dist['MD']):.0f} g", f"{calc_g(g1_sel, dist['G1']):.0f} g", 
                   f"{calc_g(pz_sel, dist['PZ']):.0f} g", f"{calc_g(cn_sel, dist['CN']):.0f} g"]
    })
    st.table(plan_df)
