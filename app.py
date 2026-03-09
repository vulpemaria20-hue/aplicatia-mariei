import streamlit as st
import pandas as pd

# CONFIGURARE PROFESIONALĂ
st.set_page_config(page_title="Matematica Nutriției - Sistem Expert", layout="wide")

# ====================================================
# 1. BAZA DE DATE EXTINSĂ (Date extrase din Pag. 32-107)
# ====================================================
# Valorile sunt per 100g de produs finit/ingredient
db_alimente = {
    "Tocană de legume": {"kcal": 29.15, "P": 0.81, "L": 0.85, "G": 4.41},
    "Mâncare de linte": {"kcal": 188.41, "P": 11.28, "L": 2.71, "G": 31.99},
    "Supă de pui": {"kcal": 24.14, "P": 2.15, "L": 0.7, "G": 0.28},
    "Orez integral legume": {"kcal": 150.4, "P": 3.7, "L": 2.5, "G": 28.2},
    "Salată ton avocado": {"kcal": 158.0, "P": 6.0, "L": 12.0, "G": 5.0},
    "Kinder Felie Lapte": {"kcal": 135.88, "P": 13.0, "L": 6.25, "G": 6.5},
    "Budincă Chia Zmeură": {"kcal": 105.4, "P": 4.22, "L": 6.69, "G": 10.52},
    "Smoothie Verde": {"kcal": 54.2, "P": 1.6, "L": 0.08, "G": 10.08},
    "Piept de pui grătar": {"kcal": 165.0, "P": 31.0, "L": 3.6, "G": 0.0},
    "Somon file": {"kcal": 208.0, "P": 20.0, "L": 13.0, "G": 0.0},
    "Omletă simplă": {"kcal": 155.0, "P": 12.6, "L": 10.6, "G": 1.1},
    "Iaurt grecesc 2%": {"kcal": 69.0, "P": 9.0, "L": 2.0, "G": 4.0},
    "Banana": {"kcal": 89.0, "P": 1.1, "L": 0.3, "G": 22.8},
    "Migdale crude": {"kcal": 575.0, "P": 21.0, "L": 49.0, "G": 21.0},
    "Pâine integrală": {"kcal": 223.3, "P": 13.0, "L": 1.7, "G": 39.0},
    "Cartof dulce copt": {"kcal": 116.0, "P": 1.6, "L": 0.1, "G": 20.1},
    "Brioșe legume": {"kcal": 95.0, "P": 10.2, "L": 3.4, "G": 5.5},
    "Humus clasic": {"kcal": 230.9, "P": 8.0, "L": 14.0, "G": 18.0}
}
# Notă: Pentru a ajunge la 200+, se pot adăuga restul ingredientelor din tabelele de la pag. 32-107.

# ====================================================
# 2. LOGICA DE CALCUL (Matematica Nutriției)
# ====================================================
def calcul_metabolic(greutate, sex, varsta, ic_tip, obiectiv):
    # RMB (Pag. 10 & 29)
    if varsta >= 65:
        factor_rmb = 0.9 if sex == "Masculin" else 0.8
    else:
        factor_rmb = 1.0 if sex == "Masculin" else 0.8
    rmb = factor_rmb * greutate * 24
    
    # TNC - Mentinere (GA x IC - Pag. 11)
    tnc_mentinere = greutate * ic_tip
    
    # Target Obiectiv (Pag. 11, 28)
    target = tnc_mentinere
    if obiectiv == "Scădere": target -= 500
    elif obiectiv == "Creștere": target += 500
    
    # Siguranță: Nu sub RMB! (Pag. 8)
    if target < rmb: target = rmb
    
    return rmb, target

# ====================================================
# 3. INTERFAȚA UTILIZATOR
# ====================================================
st.title("⚖️ Matematica Nutriției - Sistem Expert")
st.sidebar.header("🔐 Autentificare & Client")
nume = st.sidebar.text_input("Nume Client", "Maria")
parola = st.sidebar.text_input("Cod Acces", type="password")

if parola == "nutrifit2026":
    tab1, tab2, tab3 = st.tabs(["📊 Calcule", "🍱 Plan Alimentar (5 Mese)", "🔍 Nutrienți"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            greutate = st.number_input("Greutate (kg)", 40, 200, 70)
            sex = st.radio("Sex", ["Masculin", "Feminin"])
            varsta = st.number_input("Vârstă", 18, 95, 35)
        with col2:
            ic_map = {"Sedentar": 25, "Ușor": 30, "Mediu": 35, "Mare": 40, "Sportiv": 45}
            act = st.selectbox("Activitate", list(ic_map.keys()))
            obj = st.selectbox("Obiectiv", ["Menținere", "Scădere", "Creștere"])
        
        rmb, target = calcul_metabolic(greutate, sex, varsta, ic_map[act], obj)
        st.metric("Target Zilnic", f"{target:.0f} kcal")
        
        # Calcul Macro (Pag. 14-15)
        p_gr = greutate * (1.7 if act != "Sedentar" else 1.2)
        l_gr = greutate * (1.0 if act != "Sedentar" else 0.8)
        g_kcal = target - (p_gr * 4) - (l_gr * 9)
        g_gr = g_kcal / 4 if g_kcal > 0 else 0

    with tab2:
        st.subheader(f"Meniu pentru {nume} - {target:.0f} kcal")
        dist = {"Mic Dejun": 0.25, "Gustare 1": 0.10, "Prânz": 0.35, "Gustare 2": 0.10, "Cină": 0.20}
        
        plan_zile = []
        for masa, procent in dist.items():
            kcal_masa = target * procent
            # Selecție aliment bazată pe masa respectivă
            options = list(db_alimente.keys())
            sel = st.selectbox(f"Alege {masa}", options, key=masa)
            
            gramaj = (kcal_masa / db_alimente[sel]["kcal"]) * 100
            p_masa = (gramaj * db_alimente[sel]["P"]) / 100
            l_masa = (gramaj * db_alimente[sel]["L"]) / 100
            g_masa = (gramaj * db_alimente[sel]["G"]) / 100
            
            plan_zile.append({"Masă": masa, "Aliment": sel, "Cantitate (g)": f"{gramaj:.0f} g", 
                              "Kcal": f"{kcal_masa:.0f}", "P (g)": f"{p_masa:.1f}", 
                              "L (g)": f"{l_masa:.1f}", "G (g)": f"{g_masa:.1f}"})
        
        st.table(pd.DataFrame(plan_zile))

    with tab3:
        st.subheader("Verificare Echilibru Macronutrienți")
        c1, c2, c3 = st.columns(3)
        c1.metric("Proteine Necesar", f"{p_gr:.0f} g")
        c2.metric("Lipide Necesar", f"{l_gr:.0f} g")
        c3.metric("Glucide (Restul)", f"{g_gr:.0f} g")
        st.info("Sistemul ajustează automat glucidele în funcție de targetul caloric ales [8].")
