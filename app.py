import streamlit as st
import pandas as pd
import random

# 1. CONFIGURARE PAGINĂ
st.set_page_config(page_title="Sistem Expert - Matematica Nutriției", page_icon="⚖️", layout="wide")

# 2. BAZĂ DE DATE EXTINSĂ (Extrase din Pag. 32-128)
# Structură: "Aliment": [Kcal/100g, Proteine, Lipide, Glucide]
db_alimente = {
    "Mic Dejun": {
        "Omletă cu brânză": [156, 12.6, 10.6, 1.2], "Budincă Chia": [105.4, 4.22, 6.69, 10.52],
        "Brioșe legume": [95.0, 10.2, 3.4, 5.5], "Fulgi de ovăz cu lapte": [1, 6-8],
        "Humus clasic": [230.9, 8.07, 15.16, 19.09], "Pâine integrală cu avocado": [7, 9, 10]
    },
    "Gustări": {
        "Smoothie Verde": [54.2, 1.6, 0.08, 10.08], "Kinder Felie Lapte": [135.88, 13, 6.25, 6.5],
        "Măr verde": [52, 0.3, 0.2, 13.8], "Banana": [89, 1.1, 0.3, 22.8],
        "Iaurt grecesc 2%": [69, 5.3, 3, 5.9], "Migdale crude": [11, 12],
        "Brioșe Spanac & Banană": [247.46, 3.82, 33.54, 11]
    },
    "Prânz": {
        "Tocană de legume": [29.15, 0.81, 0.85, 4.41], "Mâncare de linte": [188.41, 11.28, 2.71, 31.99],
        "Orez integral cu legume": [150.4, 3.7, 2.5, 28.2], "Piept de pui grătar": [165, 31, 3.6, 0],
        "Somon file": [5, 13], "Rasol vită": [133, 22.6, 4.6, 0]
    },
    "Cină": {
        "Salată de ton cu avocado": [158.0, 6.0, 12.0, 5.0], "Cod la grătar": [107.0, 24.0, 1.0, 0.0],
        "Supă de pui": [24.14, 2.15, 0.7, 0.28], "Zucchini la grătar": [17, 1.2, 0.2, 3.1],
        "Creveți rucola": [13-15], "Iahnie de fasole": [154.1, 6.4, 6, 19.2]
    }
}

# 3. SECURITATE (Pag. 135)
if "login" not in st.session_state: st.session_state.login = False
if not st.session_state.login:
    st.title("🔐 Acces Protejat")
    parola = st.text_input("Parolă", type="password")
    if st.button("Autentificare"):
        if parola == "nutrifit2026":
            st.session_state.login = True
            st.rerun()
        else: st.error("Parolă incorectă")
    st.stop()

# 4. PARAMETRI CALCULATOR (Metodologia Vasile Bogdan)
st.sidebar.header("👤 Profil Client")
nume = st.sidebar.text_input("Nume Client", "Maria")
greutate = st.sidebar.number_input("Greutate kg", 40, 200, 70)
inaltime = st.sidebar.number_input("Înălțime cm", 130, 220, 170)
varsta = st.sidebar.number_input("Vârstă", 18, 95, 35)
sex = st.sidebar.radio("Sex", ["Masculin", "Feminin"])

# Indici Corespunzători (IC) - Pag. 8
ic_valuri = {"Sedentar": 25, "Ușor": 30, "Mediu": 35, "Mare": 40, "Foarte Mare": 45}
activitate = st.sidebar.selectbox("Activitate", list(ic_valuri.keys()))
ic = ic_valuri[activitate]

# REZOLVAREA ERORII: Definim intervalul 500-1000 Kcal (Pag. 9, 131)
deficit = st.sidebar.select_slider("Deficit Caloric (Kcal)", options=)

# 5. LOGICA MATEMATICĂ
# Formula RMB (Pag. 9, 19, 20)
factor_rmb = (0.9 if sex == "Masculin" else 0.8) if varsta >= 65 else (1.0 if sex == "Masculin" else 0.8)
rmb = factor_rmb * greutate * 24

# Formula TNC Mentinere (GA x IC) [1, 4]
tnc_mentinere = greutate * ic
target_final = tnc_mentinere - deficit

# Protecție Metabolică: Nu sub RMB! [2, 16]
if target_final < rmb: target_final = rmb

# Calcul Macronutrienți (Pag. 11, 12, 13)
prot_g = greutate * (1.7 if ic >= 35 else 1.2)
lip_g = greutate * (1.0 if ic >= 35 else 0.8)
gluc_kcal = target_final - (prot_g * 4) - (lip_g * 9)
gluc_g = gluc_kcal / 4

# 6. INTERFAȚĂ REZULTATE
st.title(f"🍎 Plan Nutrițional Matematic: {nume}")
c1, c2, c3 = st.columns(3)
c1.metric("Țintă Zilnică", f"{target_final:.0f} Kcal")
c2.metric("RMB (Minim)", f"{rmb:.0f} Kcal")
c3.metric("Status Proteic", f"{prot_g:.1f} g")

# 7. GENERATOR AUTOMAT 7 ZILE (Agent AI)
if st.button("🤖 Agent AI: Generează Plan 7 Zile (5 Mese)"):
    zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
    # Distribuție calorică pe mese [17]
    distributie = {"Mic Dejun": 0.25, "Gustare 1": 0.10, "Prânz": 0.35, "Gustare 2": 0.10, "Cină": 0.20}
    
    plan_saptamanal = []
    for zi in zile:
        for masa, procent in distributie.items():
            cat = "Gustări" if "Gustare" in masa else masa
            preparat = random.choice(list(db_alimente[cat].keys()))
            kcal_100g = db_alimente[cat][preparat]
            
            kcal_masa = target_final * procent
            gramaj = (kcal_masa / kcal_100g) * 100
            
            plan_saptamanal.append({
                "Zi": zi, "Masă": masa, "Aliment": preparat, 
                "Cantitate": f"{gramaj:.0f}g", "Kcal": int(kcal_masa)
            })

    df = pd.DataFrame(plan_saptamanal)
    for zi in zile:
        with st.expander(f"📅 Meniu {zi}"):
            st.table(df[df["Zi"] == zi][["Masă", "Aliment", "Cantitate", "Kcal"]])
