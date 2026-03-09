import streamlit as st
import pandas as pd
import random

# 1. CONFIGURARE PAGINĂ
st.set_page_config(page_title="Sistem Expert - Matematica Nutriției", page_icon="⚖️", layout="wide")

# 2. BAZĂ DE DATE EXTINSĂ (Extrase din Pag. 32-145)
# Structură: "Aliment": [Kcal/100g, Proteine, Lipide, Glucide]
db_alimente = {
    "Tocană de legume": [29.15, 0.81, 0.85, 4.41],
    "Mâncare de linte verde": [188.41, 11.28, 2.71, 31.99],
    "Orez integral cu legume": [150.4, 3.7, 2.5, 28.2],
    "Humus clasic": [230.9, 8.07, 15.16, 19.09],
    "Salată de ton cu avocado": [158.0, 6.0, 12.0, 5.0],
    "Kinder Felie de Lapte (Proteic)": [135.88, 13.0, 6.25, 6.5],
    "Smoothie Verde": [54.2, 1.6, 0.08, 10.08],
    "Budincă de chia cu zmeură": [105.4, 4.22, 6.69, 10.52],
    "Omletă simplă": [155.0, 12.6, 10.6, 1.1],
    "Piept de pui grătar": [165.0, 31.0, 3.6, 0.0],
    "Somon file": [208.0, 20.0, 13.0, 0.0],
    "Iaurt grecesc 2%": [69.0, 9.0, 2.0, 4.0],
    "Brioșe legume": [95.0, 10.2, 3.4, 5.5],
    "Pâine integrală": [223.3, 13.0, 1.7, 39.0],
    "Mâncare de mazăre": [50.0, 3.2, 1.6, 6.0],
    "Cod la grătar": [107.0, 24.0, 1.0, 0.0],
    "Banana": [89.0, 1.1, 0.3, 22.8],
    "Migdale crude": [575.0, 21.0, 49.0, 21.0],
    "Brânză de vaci slabă": [125.0, 18.0, 4.4, 3.5],
    "Cartof dulce copt": [116.0, 1.6, 0.1, 20.1]
}

# 3. SECURITATE
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
greutate = st.sidebar.number_input("Greutate Actuală (GA) kg", 40, 200, 70)
inaltime = st.sidebar.number_input("Înălțime cm", 130, 220, 170)
varsta = st.sidebar.number_input("Vârstă", 18, 95, 35)
sex = st.sidebar.radio("Sex", ["Masculin", "Feminin"])

# Indici Corespunzători (IC) - Pag. 12
ic_valuri = {"Sedentar": 25, "Ușor": 30, "Mediu": 35, "Mare": 40, "Foarte Mare": 45}
activitate = st.sidebar.selectbox("Nivel Activitate", list(ic_valuri.keys()))
ic = ic_valuri[activitate]

# Deficit Caloric (Fixarea erorii tale) - Pag. 148
deficit = st.sidebar.select_slider("Deficit Caloric (Kcal)", options=)

# 5. LOGICA MATEMATICĂ
# Formula RMB (Pag. 13, 25, 29)
if varsta >= 65:
    factor_rmb = 0.9 if sex == "Masculin" else 0.8
else:
    factor_rmb = 1.0 if sex == "Masculin" else 0.8
rmb = factor_rmb * greutate * 24

# Formula TNC Mentinere (GA x IC) - Pag. 11
tnc_mentinere = greutate * ic
target_final = tnc_mentinere - deficit

# Protecție Metabolică: Nu sub RMB! - Pag. 13, 148
if target_final < rmb:
    target_final = rmb

# Calcul Macronutrienți (Pag. 15-17)
# Proteine și Lipide fixe per kg, Glucidele preiau restul
prot_g = greutate * (1.7 if ic >= 35 else 1.2)
lip_g = greutate * (1.0 if ic >= 35 else 0.8)
gluc_kcal = target_final - (prot_g * 4) - (lip_g * 9)
gluc_g = gluc_kcal / 4

# 6. INTERFAȚĂ REZULTATE
st.title(f"🍎 Plan Nutrițional Matematic: {nume}")
c1, c2, c3 = st.columns(3)
c1.metric("Țintă Zilnică", f"{target_final:.0f} Kcal")
c2.metric("RMB (Minim)", f"{rmb:.0f} Kcal")
c3.metric("Deficit Aplicat", f"{deficit} Kcal")

st.info(f"**Necesar Macronutrienți:** P: {prot_g:.1f}g | L: {lip_g:.1f}g | G: {gluc_g:.1f}g")

# 7. GENERATOR AUTOMAT 7 ZILE (Agent AI)
if st.button("🤖 Agent AI: Generează Plan 7 Zile (3 Mese + 2 Gustări)"):
    zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
    # Distribuție calorică pe mese - Pag. 157
    distributie = {"Mic Dejun": 0.25, "Gustare 1": 0.10, "Prânz": 0.35, "Gustare 2": 0.10, "Cină": 0.20}
    
    plan_complet = []
    for zi in zile:
        for masa, procent in distributie.items():
            preparat = random.choice(list(db_alimente.keys()))
            kcal_100g = db_alimente[preparat]
            
            kcal_alocate = target_final * procent
            # Formula Gramaj: (Kcal masă / Kcal aliment 100g) * 100
            gramaj = (kcal_alocate / kcal_100g) * 100
            
            p_m = (gramaj * db_alimente[preparat][3]) / 100
            l_m = (gramaj * db_alimente[preparat][4]) / 100
            g_m = (gramaj * db_alimente[preparat][5]) / 100
            
            plan_complet.append({
                "Zi": zi, "Masă": masa, "Preparat": preparat, 
                "Gramaj": f"{gramaj:.0f}g", "Kcal": int(kcal_alocate),
                "P": round(p_m,1), "L": round(l_m,1), "G": round(g_m,1)
            })

    df = pd.DataFrame(plan_complet)
    for zi in zile:
        with st.expander(f"📅 Meniu {zi}"):
            st.table(df[df["Zi"] == zi][["Masă", "Preparat", "Gramaj", "Kcal", "P", "L", "G"]])
