import streamlit as st
import pandas as pd
import random

# 1. CONFIGURARE PAGINĂ
st.set_page_config(page_title="Sistem Expert - Matematica Nutriției", page_icon="⚖️", layout="wide")

# 2. BAZĂ DE DATE EXTINSĂ (Extrase din Pag. 32-107)
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

# 3. SECURITATE
if "login" not in st.session_state: 
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Acces Protejat")
    parola = st.text_input("Introduceți parola de acces:", type="password")
    if st.button("Autentificare"):
        if parola == "nutrifit2026":
            st.session_state.login = True
            st.rerun()
        else: 
            st.error("Parolă incorectă!")
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

# REZOLVARE EROARE: Definim opțiunile pentru deficit (0 - 800 kcal)
deficit = st.sidebar.select_slider("Deficit Caloric (Kcal)", options=list(range(0, 801, 50)))

# 5. LOGICA MATEMATICĂ (Pag. 11-17)
# Formula RMB
if varsta >= 65:
    rmb_f = 0.9 if sex == "Masculin" else 0.8
else:
    rmb_f = 1.0 if sex == "Masculin" else 0.8
rmb = rmb_f * greutate * 24

# Target Caloric (Greutate * IC - Deficit)
tnc_mentinere = greutate * ic
target = tnc_mentinere - deficit

# Protecție Metabolică: Nu sub RMB! (Pag. 13, 150)
if target < rmb: 
    target = rmb
    st.sidebar.warning(f"⚠️ Atenție: Targetul a fost limitat la RMB ({rmb:.0f} kcal) pentru a preveni încetinirea metabolismului.")

# Calcul Nutrienți (Pag. 15-17)
p_gr = greutate * (1.7 if ic >= 35 else 1.2)
l_gr = greutate * (1.0 if ic >= 35 else 0.8)
c_gr = (target - (p_gr * 4) - (l_gr * 9)) / 4

# 6. INTERFAȚĂ ȘI AGENT GENERATOR
st.title(f"⚖️ Plan Nutrițional Matematic: {nume}")

# Afișare KPI
col1, col2, col3, col4 = st.columns(4)
col1.metric("Țintă Zilnică", f"{target:.0f} Kcal")
col2.metric("Proteine", f"{p_gr:.0f} g")
col3.metric("Lipide", f"{l_gr:.0f} g")
col4.metric("Carbohidrați", f"{c_gr:.0f} g")

st.markdown("---")

if st.button("🤖 Agent AI: Generează Plan 7 Zile (5 Mese)"):
    zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
    # Distribuție calorică: MD(25%), G1(10%), PZ(35%), G2(10%), CN(20%)
    dist = {"Mic Dejun": 0.25, "Gustare 1": 0.10, "Prânz": 0.35, "Gustare 2": 0.10, "Cină": 0.20}
    
    plan_saptamanal = []
    
    for zi in zile:
        for masa, proc in dist.items():
            # Selectăm categoria corectă din baza de date
            cat = "Gustări" if "Gustare" in masa else masa
            
            # Alegem un aliment aleatoriu din categoria respectivă
            aliment = random.choice(list(db_alimente[cat].keys()))
            kcal_100 = db_alimente[cat][aliment]
            
            # Calculăm necesarul caloric pentru acea masă și gramajul aferent
            kcal_masa = target * proc
            gramaj = (kcal_masa / kcal_100) * 100
            
            plan_saptamanal.append({
                "Zi": zi, 
                "Masă": masa, 
                "Aliment": aliment, 
                "Cantitate": f"{gramaj:.0f}g", 
                "Kcal": int(kcal_masa)
            })

    # Creăm DataFrame-ul și îl afișăm pe zile
    df = pd.DataFrame(plan_saptamanal)
    
    for zi in zile:
        with st.expander(f"📅 Meniu DETALIAT - {zi}"):
            df_zi = df[df["Zi"] == zi][["Masă", "Aliment", "Cantitate", "Kcal"]]
            st.table(df_zi)
            st.info(f"Total Calorii {zi}: {df_zi['Kcal'].sum()} kcal")

else:
    st.info("Apasă pe butonul de mai sus pentru a genera planul alimentar personalizat.")
