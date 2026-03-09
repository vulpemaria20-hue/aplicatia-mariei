import streamlit as st
import pandas as pd

# CONFIGURARE PAGINĂ
st.set_page_config(page_title="Sistem Expert - Matematica Nutriției", layout="wide")

# INITIALIZARE SESIUNE PENTRU CLIENȚI
if "baza_clienti" not in st.session_state:
    st.session_state.baza_clienti = {}

# --- INTERFAȚĂ DE AUTENTIFICARE ---
st.sidebar.title("🔐 Administrare Clienți")
nume_client = st.sidebar.text_input("Nume și Prenume Client", placeholder="Ex: Ion Popescu")

if not nume_client:
    st.info("Introduceți numele clientului în bara laterală pentru a începe.")
    st.stop()

# AFISARE NUME ÎN TITLU
st.title(f"⚖️ Plan Nutrițional: {nume_client}")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📊 Calculator Metabolic", "🔍 Evaluare Evoluție", "🍱 Plan Alimentar"])

# ====================================================
# TAB 1: CALCULATOR METABOLIC
# ====================================================
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        greutate = st.number_input("Greutate Actuală (kg)", 40.0, 250.0, 70.0)
        inaltime = st.number_input("Înălțime (cm)", 140, 220, 170)
        varsta = st.number_input("Vârstă", 18, 90, 35)
        sex = st.radio("Sex", ["Masculin", "Feminin"])

    with col2:
        # Opțiuni extrase din pag. 11 a manualului
        activitate = st.selectbox("Nivel Activitate (Indice Corespunzător)", [
            "Sedentar (25-30 kcal/kg)", 
            "Ușor (30-35 kcal/kg)", 
            "Mediu (35-40 kcal/kg)", 
            "Mare (40-45 kcal/kg)", 
            "Foarte Mare (45-50 kcal/kg)"
        ])
        
        # CORECPȚIA ERORII TypeError: extragem prima cifră din interval
        ic = int(activitate.split("(")[2].split("-"))
        
        # Formula Vasile Bogdan (GA x IC) [5]
        tnc = greutate * ic 
        
        obiectiv = st.selectbox("Obiectiv", ["Menținere", "Scădere în greutate", "Creștere în greutate"])
        target = tnc
        if obiectiv == "Scădere în greutate": target -= 500
        elif obiectiv == "Creștere în greutate": target += 500

    if st.button("Calculează și Salvează Profil"):
        # Calcul RMB conform formulei din pag. 12
        factor_rmb = 1.0 if sex == "Masculin" else 0.8
        rmb = factor_rmb * greutate * 24
        
        # Salvare în baza de date locală
        st.session_state.baza_clienti[nume_client] = {"target": target, "greutate": greutate}
        
        st.success(f"Analiză finalizată pentru **{nume_client}**")
        c1, c2 = st.columns(2)
        c1.metric("Target Zilnic", f"{target:.0f} kcal")
        c2.metric("RMB (Metabolism Bazal)", f"{rmb:.0f} kcal")
        
        if target < rmb:
            st.warning("⚠️ Atenție! Deficitul este prea mare. Nu scădeți sub RMB! [6]")

# ====================================================
# TAB 2: EVALUARE (Plicometrie & Circumferințe)
# ====================================================
with tab2:
    st.subheader(f"Evoluție la 2 săptămâni: {nume_client}")
    st.write("Măsurătorile trebuie corelate obligatoriu pentru a verifica dacă pierderea este din grăsime, nu din mușchi [3, 7].")
    
    c1, c2 = st.columns(2)
    with c1:
        talie = st.number_input("Circumferință Talie (cm)", 40, 150)
        coapsa = st.number_input("Circumferință Coapsă (cm)", 20, 100)
    with c2:
        # Plicometrie (cele 4 zone indicate în manual [7])
        p_tri = st.number_input("Pliu Triceps (mm)", 0.0, 50.0)
        p_abd = st.number_input("Pliu Abdomen (mm)", 0.0, 50.0)
        st.info(f"Monitorizare: Talie {talie} cm | Pliuri { (p_tri + p_abd)/2 } mm")

# ====================================================
# TAB 3: PLAN ALIMENTAR (Exemple din manual)
# ====================================================
with tab3:
    st.subheader(f"Meniu Personalizat pentru {nume_client}")
    # Aici poți integra logica de gramaje generată anterior
    st.write(f"Utilizați targetul de **{target:.0f} kcal** pentru a calcula gramajele rețetelor.")
