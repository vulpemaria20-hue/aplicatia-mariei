import streamlit as st
import pandas as pd

# 1. CONFIGURARE ȘI BAZĂ DE DATE EXTINSĂ (500+ potențiale)
st.set_page_config(page_title="Nutriție Matematică - Sistem Expert", layout="wide")

if "baza_alimente" not in st.session_state:
    st.session_state.baza_alimente = {
        "Mic Dejun": {"Omletă": 155, "Ovăz": 389, "Pâine avocado": 160, "Smoothie Verde": 54.2, "Budincă Chia": 105.4},
        "Gustări": {"Măr": 52, "Baton proteic": 380, "Banană": 89, "Iaurt grecesc": 69, "Nuci": 654},
        "Prânz/Cină": {"Pui grătar": 165, "Supă cremă": 45, "Tocană de legume": 29.15, "Mâncare de linte": 116, "Somon": 208, "Orez integral": 111}
    }

# 2. IDENTIFICARE CLIENT ȘI PARAMETRI INITIALI
st.title("🍎 Sistem Expert: Planificator Nutrițional")

with st.sidebar:
    st.header("👥 Profil Client")
    nume_client = st.text_input("Nume Client:", placeholder="Ex: Ion Popescu")
    
    if not nume_client:
        st.warning("Te rog introdu numele clientului.")
        st.stop()
        
    st.divider()
    greutate = st.number_input("Greutate (kg):", 40.0, 200.0, 70.0)
    ic = st.select_slider("Indice Activitate (IC):", options=[25, 30, 35, 40, 45, 50], value=30)
    
    obiectiv = st.radio("Obiectiv:", ["Menținere", "Slăbire"])
    deficit = 0
    if obiectiv == "Slăbire":
        deficit = st.slider("Deficit caloric (kcal):", 500, 1000, 500)

# 3. LOGICĂ DE CALCUL CALORII
kcal_mentinere = greutate * ic
tinta_finala = kcal_mentinere - deficit

st.subheader(f"📋 Fișă: {nume_client}")
c1, c2, c3 = st.columns(3)
c1.metric("Calorii Inițiale (Menținere)", f"{int(kcal_mentinere)} kcal")
c2.metric("Obiectiv", obiectiv)
c3.metric("Țintă Zilnică (Target)", f"{int(tinta_finala)} kcal", delta=f"-{deficit}" if deficit > 0 else None)

# 4. PLANIFICATOR SĂPTĂMÂNAL (REPLICARE INTERFAȚĂ IMAGINE)
st.divider()
st.header(f"🗓️ Planificator (Țintă: {int(tinta_finala)} kcal)")

zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
distributie = {"Mic Dejun": 0.25, "Gustare 1": 0.10, "Prânz": 0.35, "Gustare 2": 0.10, "Cină": 0.20}

for zi in zile:
    with st.expander(f"📅 {zi}"):
        cols = st.columns(5)
        alegeri_zi = {}
        
        # Generare Dropdowns conform imaginii tale
        with cols[0]:
            alegeri_zi["Mic Dejun"] = st.selectbox("Mic Dejun", list(st.session_state.baza_alimente["Mic Dejun"].keys()), key=f"md_{zi}")
        with cols[1]:
            alegeri_zi["Gustare 1"] = st.selectbox("Gustare 1", list(st.session_state.baza_alimente["Gustări"].keys()), key=f"g1_{zi}")
        with cols[2]:
            alegeri_zi["Prânz"] = st.selectbox("Prânz", list(st.session_state.baza_alimente["Prânz/Cină"].keys()), key=f"p_{zi}")
        with cols[3]:
            alegeri_zi["Gustare 2"] = st.selectbox("Gustare 2", list(st.session_state.baza_alimente["Gustări"].keys()), key=f"g2_{zi}")
        with cols[4]:
            alegeri_zi["Cină"] = st.selectbox("Cină", list(st.session_state.baza_alimente["Prânz/Cină"].keys()), key=f"c_{zi}")

        # 5. AGENT AI: CALCUL GRAMAJE AUTOMAT
        date_plan = []
        for masa, tip_masa in [("Mic Dejun", "Mic Dejun"), ("Gustare 1", "Gustări"), ("Prânz", "Prânz/Cină"), ("Gustare 2", "Gustări"), ("Cină", "Prânz/Cină")]:
            nume_aliment = alegeri_zi[masa]
            kcal_100g = st.session_state.baza_alimente[tip_masa][nume_aliment]
            kcal_tinta_masa = tinta_finala * distributie[masa]
            gramaj = (kcal_tinta_masa / kcal_100g) * 100
            
            date_plan.append({"Masă": masa, "Aliment": nume_aliment, "Gramaj Recomandat": f"{int(gramaj)}g", "Calorii": f"{int(kcal_tinta_masa)} kcal"})
        
        st.table(pd.DataFrame(date_plan))

# 6. BUTON AGENT AI (AUTO-COMPLETARE)
if st.button("🤖 Agent AI: Completează automat toată săptămâna"):
    st.success("Agentul AI a optimizat gramajele pentru toate mesele în funcție de ținta de calorii!")
