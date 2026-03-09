import streamlit as st
import pandas as pd

# 1. CONFIGURARE PAGINĂ
st.set_page_config(page_title="Sistem Expert Nutriție - Vasile Bogdan", page_icon="⚖️", layout="wide")

# 2. SECURITATE (Aplicația cere parola stabilită în curs)
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Acces Protejat - Matematica Nutriției")
    parola = st.text_input("Introduceți parola de acces:", type="password")
    if st.button("Autentificare"):
        if parola == "nutrifit2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Parolă incorectă!")
    st.stop()

# 3. GESTIONARE CLIENȚI (Permite lucrul cu mai mulți utilizatori)
st.sidebar.title("👥 Gestiune Clienți")
nume_client = st.sidebar.text_input("Nume Client curent:", placeholder="Ex: Maria Ionescu")

if not nume_client:
    st.info("Introduceți numele clientului în bara laterală pentru a începe.")
    st.stop()

# 4. BAZA DE DATE REȚETE (Kcal/100g extrase din Pag. 32-107)
baza_alimente = {
    "Tocană de legume": 29.15, "Mâncare de linte": 188.41, "Humus": 230.9,
    "Orez integral cu legume": 150.4, "Salată de ton": 158.0, "Omletă": 155.0,
    "Smoothie Verde": 54.2, "Smoothie Fructe Pădure": 114.6, "Smoothie Mango & Cătină": 94.2,
    "Kinder Felie de Lapte": 135.88, "Brioșe Spanac & Banană": 247.46, "Budincă Chia": 105.4,
    "Somon file": 208.0, "Iaurt grecesc 2%": 69.0, "Banana": 89.0, "Pâine integrală": 223.3
}

# 5. FUNCȚII DE CALCUL (Metodologia originală din manual)
def calcul_rmb(greutate, sex, varsta):
    factor = (0.9 if sex == "Masculin" else 0.8) if varsta >= 65 else (1.0 if sex == "Masculin" else 0.8)
    return factor * greutate * 24 # Pag. 12 & 50

# --- INTERFAȚA PRINCIPALĂ ---
st.title(f"⚖️ Plan Nutrițional: {nume_client}")
tab1, tab2, tab3 = st.tabs(["📊 Calculator & IMC", "🔍 Evaluare Evoluție", "🍱 Plan Alimentar"])

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
            # Necesar caloric fix copii (Pag. 25)
            if varsta < 7: tnc = 1400
            elif varsta < 10: tnc = 1800
            elif varsta < 14: tnc = 2500 if sex == "Masculin" else 2250
            else: tnc = 3250 if sex == "Masculin" else 2400
        else:
            activitate = st.selectbox("Activitate (IC)", ["Sedentar (25)", "Ușor (30)", "Mediu (35)", "Mare (40)"])
            ic = int(activitate.split("(")[2].split(")"))
            tnc = greutate * ic # Formula GA x IC (Pag. 8)

        obiectiv = st.radio("Obiectiv", ["Menținere", "Scădere", "Creștere"])
        target = tnc
        if obiectiv == "Scădere": target -= 500
        elif obiectiv == "Creștere": target += 500

    if st.button("Generează Analiză"):
        rmb = calcul_rmb(greutate, sex, varsta)
        bmi = greutate / ((inaltime/100)**2)
        st.subheader("Rezultate")
        st.metric("Target Zilnic", f"{target:.0f} kcal")
        st.info(f"BMI actual: {bmi:.1f}")
        if target < rmb: st.warning(f"Atenție: Target sub RMB ({rmb:.0f} kcal)!")

with tab3:
    st.subheader("Configurare Meniu")
    md = st.selectbox("Alege Mic Dejun", ["Omletă", "Smoothie Verde", "Budincă Chia"])
    # Calcul gramaj automat conform Pag. 117
    g_md = (target * 0.25 / baza_alimente[md]) * 100
    st.success(f"Pentru Mic Dejun consumați: **{g_md:.0f} g** de {md}")
