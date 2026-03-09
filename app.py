import streamlit as st
import pandas as pd
import random

# 1. CONFIGURARE PAGINĂ
st.set_page_config(page_title="Sistem Expert - Matematica Nutriției", page_icon="⚖️", layout="wide")

# 2. BAZĂ DE DATE EXTINSĂ (Extrase din Pag. 32-107)
# Kcal per 100g de produs finit conform rețetelor calculate din surse
db_alimente = {
    "Mic Dejun": {
        "Omletă cu brânză": 156, "Budincă Chia": 105.4, "Brioșe legume": 95, 
        "Humus clasic": 230.9, "Ouă fierte": 155, "Pâine integrală": 223.3,
        "Cremă urdă mărar": 137, "Zacuscă vinete": 92
    },
    "Gustări": {
        "Smoothie Verde": 54.2, "Kinder Felie Lapte": 135.88, "Măr verde": 52, 
        "Banana": 89, "Iaurt grecesc 2%": 69, "Brioșe Spanac": 247.46,
        "Migdale": 575, "Nuci": 654, "Grapefruit": 32, "Căpșuni": 32
    },
    "Prânz": {
        "Tocană de legume": 29.15, "Mâncare de linte": 188.41, "Orez integral legume": 150.4,
        "Piept curcan grătar": 107, "Somon file": 208, "Rasol vită": 133,
        "Supă pui": 24.14, "Iahnie fasole": 154.1, "Mămăligă": 66
    },
    "Cină": {
        "Salată ton avocado": 158, "Cod la grătar": 107, "Supă cremă conopidă": 86.8,
        "Creveți rucola": 85, "Zucchini grătar": 17, "Paste integrale": 340,
        "Salată pui crudități": 110, "Piure mazăre": 84
    }
}

# 3. SECURITATE (Pag. 154)
if "login" not in st.session_state: st.session_state.login = False
if not st.session_state.login:
    st.title("🔐 Acces Protejat")
    parola = st.text_input("Introduceți parola de acces:", type="password")
    if st.button("Autentificare"):
        if parola == "nutrifit2026":
            st.session_state.login = True
            st.rerun()
        else: st.error("Parolă incorectă!")
    st.stop()

# 4. PARAMETRI CLIENT (Metodologia Vasile Bogdan)
st.sidebar.header("👤 Profil Client")
nume = st.sidebar.text_input("Nume Client", "Maria")
greutate = st.sidebar.number_input("Greutate kg", 40, 200, 70)
inaltime = st.sidebar.number_input("Înălțime cm", 130, 220, 170)
varsta = st.sidebar.number_input("Vârstă", 18, 95, 35)
sex = st.sidebar.radio("Sex", ["Masculin", "Feminin"])

# Indici Corespunzători (IC) - Pag. 11-12
ic_map = {"Sedentar": 25, "Ușor": 30, "Mediu": 35, "Mare": 40, "Sportiv": 45}
activitate = st.sidebar.selectbox("Activitate (IC)", list(ic_map.keys()))
ic = ic_map[activitate]

# REZOLVAREA ERORII: Definim intervalul corect conform Pag. 72 & 150
deficit = st.sidebar.select_slider("Deficit Caloric (Kcal)", options=)

# 5. LOGICA MATEMATICĂ (Pag. 11-17)
# Formula RMB
if varsta >= 65: # Pag. 50
    rmb_f = 0.9 if sex == "Masculin" else 0.8
else: # Pag. 13
    rmb_f = 1.0 if sex == "Masculin" else 0.8
rmb = rmb_f * greutate * 24

# Target Caloric (GA x IC - Deficit)
tnc_mentinere = greutate * ic
target = tnc_mentinere - deficit

# Protecție Metabolică: Nu sub RMB! (Pag. 13, 150)
if target < rmb: target = rmb

# Calcul Nutrienți (Pag. 15-17)
p_gr = greutate * (1.7 if ic >= 35 else 1.2)
l_gr = greutate * (1.0 if ic >= 35 else 0.8)
c_gr = (target - (p_gr * 4) - (l_gr * 9)) / 4

# 6. INTERFAȚĂ ȘI AGENT GENERATOR
st.title(f"⚖️ Plan Nutrițional Matematic: {nume}")
c1, c2, c3 = st.columns(3)
c1.metric("Țintă Zilnică", f"{target:.0f} Kcal")
c2.metric("RMB (Minim)", f"{rmb:.0f} Kcal")
c3.metric("Proteine", f"{p_gr:.0f} g")

if st.button("🤖 Agent AI: Generează Plan 7 Zile (5 Mese)"):
    zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
    # Distribuție calorică: MD(25%), G1(10%), PZ(35%), G2(10%), CN(20%) - Pag. 159
    dist = {"Mic Dejun": 0.25, "Gustare 1": 0.10, "Prânz": 0.35, "Gustare 2": 0.10, "Cină": 0.20}
    
    plan_saptamanal = []
    for zi in zile:
        for masa, proc in dist.items():
            cat = "Gustări" if "Gustare" in masa else masa
            aliment = random.choice(list(db_alimente[cat].keys()))
            kcal_100 = db_alimente[cat][aliment]
            
            kcal_masa = target * proc
            gramaj = (kcal_masa / kcal_100) * 100
            
            plan_saptamanal.append({
                "Zi": zi, "Masă": masa, "Aliment": aliment, 
                "Cantitate": f"{gramaj:.0f}g", "Kcal": int(kcal_masa)
            })

    df = pd.DataFrame(plan_saptamanal)
    for zi in zile:
        with st.expander(f"📅 Meniu {zi}"):
            st.table(df[df["Zi"] == zi][["Masă", "Aliment", "Cantitate", "Kcal"]])
