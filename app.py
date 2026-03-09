import streamlit as st
import pandas as pd
import random

# CONFIGURARE PAGINĂ
st.set_page_config(page_title="Sistem Expert - Matematica Nutriției", layout="wide")

# ====================================================
# 1. BAZA DE DATE EXTINSĂ (Extrase din Pag. 32-107)
# ====================================================
# Am inclus categorii de alimente pentru a permite Agentului AI să aleagă variat
db_alimente = {
    "Mic Dejun": {
        "Omletă simplă": 155, "Ovăz cu lapte": 110, "Budincă Chia Zmeură": 105.4, 
        "Brioșe legume": 95, "Cremă urdă mărar": 137, "Humus clasic": 230.9,
        "Ouă fierte cu avocado": 160, "Zacuscă vinete casă": 92, "Pancakes proteice": 180
    },
    "Gustări": {
        "Măr verde": 52, "Banana": 89, "Migdale crude": 575, "Nuci pecan": 690,
        "Iaurt grecesc 2%": 69, "Smoothie Verde": 54.2, "Kinder Felie Lapte": 135.88,
        "Brioșe Spanac": 247.46, "Căpșuni ciocolată": 136, "Grapefruit": 32
    },
    "Prânz": {
        "Tocană de legume": 29.15, "Mâncare de linte": 188.41, "Orez integral legume": 150.4,
        "Piept curcan grătar": 107, "Somon file": 208, "Rasol vită": 133,
        "Paste integrale": 340, "Supă pui": 24.14, "Iahnie fasole": 154.1,
        "Dorada cu legume": 89, "Burger vită casă": 250
    },
    "Cină": {
        "Salată ton avocado": 158, "Cod la grătar": 107, "Supă cremă ciuperci": 50,
        "Creveți rucola": 85, "Zucchini la grătar": 75, "Păstrăv cu mămăligă": 140,
        "Salată pui și crudități": 120, "Vită cu broccoli": 110
    }
}

# ====================================================
# 2. LOGICA MATEMATICĂ (Formule Vasile Bogdan)
# ====================================================
def calculeaza_plan(greutate, sex, varsta, ic_val, deficit, p_kg, l_kg):
    # RMB (Pag. 12 & 50)
    rmb_factor = (0.9 if sex == "Masculin" else 0.8) if varsta >= 65 else (1.0 if sex == "Masculin" else 0.8)
    rmb = rmb_factor * greutate * 24
    
    # TNC Mentinere (GA x IC - Pag. 8)
    tnc_mentinere = greutate * ic_val
    
    # Target (Deficit 500-1000 - Pag. 12, 156)
    target = tnc_mentinere - deficit
    if target < rmb: target = rmb # Limita de siguranță: Nu sub RMB! [3]
    
    # Macronutrienți (Pag. 15-17)
    prot_g = greutate * p_kg
    lip_g = greutate * l_kg
    carb_kcal = target - (prot_g * 4) - (lip_g * 9)
    carb_g = carb_kcal / 4 if carb_kcal > 0 else 0
    
    return rmb, target, prot_g, lip_g, carb_g

# ====================================================
# 3. INTERFAȚĂ & AGENT AI
# ====================================================
st.title("⚖️ Matematica Nutriției - Agent Expert 7 Zile")
parola = st.sidebar.text_input("Parolă", type="password")

if parola == "nutrifit2026":
    t1, t2 = st.tabs(["📊 Parametri Client", "🍱 Plan 7 Zile"])
    
    with t1:
        c1, c2 = st.columns(2)
        with c1:
            g = st.number_input("Greutate (kg)", 40, 200, 80)
            v = st.number_input("Vârstă", 18, 95, 40)
            s = st.radio("Sex", ["Masculin", "Feminin"])
        with c2:
            ic = st.select_slider("Nivel Activitate (IC)", options=[4-9])
            def_cal = st.select_slider("Deficit Caloric (Kcal)", options=)
        
        # Setări nutrienți conform activității (Pag. 15-16)
        p_val = 1.7 if ic >= 35 else 1.2
        l_val = 1.0 if ic >= 35 else 0.8
        
        rmb, target, p, l, c = calculeaza_plan(g, s, v, ic, def_cal, p_val, l_val)
        
        st.metric("Target Zilnic", f"{target:.0f} kcal")
        if target == rmb: st.warning("Targetul a fost limitat la RMB pentru siguranță metabolică.")

    with t2:
        if st.button("🤖 Agent AI: Generează Plan Diversificat (7 Zile)"):
            zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
            distributie = {"Mic Dejun": 0.25, "Gustare 1": 0.10, "Prânz": 0.35, "Gustare 2": 0.10, "Cină": 0.20}
            
            plan_complet = []
            for zi in zile:
                for masa, procent in distributie.items():
                    # Alegere inteligentă a alimentelor bazată pe categorie
                    cat = "Mic Dejun" if masa == "Mic Dejun" else "Prânz" if masa == "Prânz" else "Cină" if masa == "Cină" else "Gustări"
                    aliment = random.choice(list(db_alimente[cat].keys()))
                    kcal_100g = db_alimente[cat][aliment]
                    
                    kcal_masa = target * procent
                    gramaj = (kcal_masa / kcal_100g) * 100
                    
                    plan_complet.append({"Zi": zi, "Masă": masa, "Aliment": aliment, "Gramaj": f"{gramaj:.0f} g", "Kcal": f"{kcal_masa:.0f}"})
            
            df = pd.DataFrame(plan_complet)
            for zi in zile:
                with st.expander(f"📅 Plan pentru {zi}"):
                    st.table(df[df["Zi"] == zi][["Masă", "Aliment", "Gramaj", "Kcal"]])
            
            st.download_button("📥 Descarcă Planul 7 Zile", df.to_csv().encode('utf-8'), "plan_7_zile.csv")

else:
    st.info("Introduceți parola pentru a accesa sistemul.")
