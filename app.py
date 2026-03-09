import streamlit as st
import pandas as pd
import random

# 1. CONFIGURARE PAGINĂ
st.set_page_config(page_title="Matematica Nutriției - Sistem Expert", page_icon="⚖️", layout="wide")

# 2. BAZA DE DATE EXTINSĂ (Extrase din Pag. 32-107)
# Structură: "Nume": [kcal, P, L, G] per 100g
db = {
    "Mic Dejun": {
        "Omletă simplă": [155, 12.6, 10.6, 1.1], "Budincă Chia Zmeură": [105.4, 4.22, 6.69, 10.52],
        "Brioșe legume": [95, 10.2, 3.4, 5.5], "Cremă urdă mărar": [7-10],
        "Humus clasic": [230.9, 8.07, 15.16, 19.09], "Ou fiert": [155, 13, 11, 1.1],
        "Fulgi de secară": [11-13], "Pâine integrală": [223.3, 13, 1.7, 39]
    },
    "Gustări": {
        "Smoothie Verde": [54.2, 1.6, 0.08, 10.08], "Kinder Felie Lapte": [135.88, 13, 6.25, 6.5],
        "Măr verde": [52, 0.3, 0.2, 13.8], "Banana": [89, 1.1, 0.3, 22.8],
        "Migdale crude": [14, 15], "Iaurt grecesc 2%": [9, 11, 16, 17],
        "Brioșe Spanac": [247.46, 3.82, 15.3, 23.4], "Nuci pecan": [9, 11, 18]
    },
    "Prânz": {
        "Tocană de legume": [29.15, 0.81, 0.85, 4.41], "Mâncare de linte": [188.41, 11.28, 2.71, 31.99],
        "Orez integral legume": [150.4, 3.7, 2.5, 28.2], "Salată ton avocado": [2, 10, 19, 20],
        "Somon file": [21, 22], "Piept de pui grătar": [165, 31, 3.6, 0],
        "Rasol vită": [133, 22.6, 4.6, 0], "Mămăligă": [66, 1.4, 0.4, 14.3]
    },
    "Cină": {
        "Cod la grătar": [12, 23, 24], "Supă de pui": [24.14, 2.15, 0.7, 0.28],
        "Zucchini la grătar": [17, 1.2, 0.2, 3.1], "Creveți rucola": [12, 17, 25, 26],
        "Salată pui crudități": [110, 15, 4, 3.5], "Piure conopidă": [57, 1, 4.3, 3.7]
    }
}

# 3. SECURITATE (Parola conform pag. 156)
if "login" not in st.session_state: st.session_state.login = False
if not st.session_state.login:
    st.title("🔐 Acces Protejat - Sistem Expert")
    parola = st.text_input("Introduceți parola:", type="password")
    if st.button("Autentificare"):
        if parola == "nutrifit2026":
            st.session_state.login = True
            st.rerun()
        else: st.error("Parolă incorectă!")
    st.stop()

# 4. GESTIONARE CLIENȚI
st.sidebar.title("👥 Administrare")
nume_client = st.sidebar.text_input("Nume Client:", "Maria")

# 5. CALCULATOR METABOLIC (Metodologia Vasile Bogdan)
st.title(f"⚖️ Plan Nutrițional Matematic: {nume_client}")
t1, t2 = st.tabs(["📊 Calculator", "📅 Plan 7 Zile"])

with t1:
    c1, c2 = st.columns(2)
    with c1:
        g = st.number_input("Greutate actuală (GA) - kg", 40, 200, 70)
        v = st.number_input("Vârstă", 18, 95, 35)
        s = st.radio("Sex", ["Masculin", "Feminin"])
    with c2:
        # Indici corespunzători (IC) conform Pag. 11
        ic_map = {"Sedentar": 25, "Ușor": 30, "Mediu": 35, "Mare": 40, "Foarte Mare": 45}
        act = st.selectbox("Nivel Activitate (IC)", list(ic_map.keys()))
        # CORECȚIA ERORII TALE: Definim opțiunile corect [1, 3]
        def_cal = st.select_slider("Deficit Caloric (Kcal)", options=)

    # Calcule [1, 5, 26, 27]
    rmb_f = (0.9 if s == "Masculin" else 0.8) if v >= 65 else (1.0 if s == "Masculin" else 0.8)
    rmb = rmb_f * g * 24
    target = (g * ic_map[act]) - def_cal
    if target < rmb: target = rmb # Protecție metabolică [2]

    # Nutrienți [4, 5]
    p_g = g * (1.7 if ic_map[act] >= 35 else 1.2)
    l_g = g * (1.0 if ic_map[act] >= 35 else 0.8)
    c_g = (target - (p_g * 4) - (l_g * 9)) / 4

    st.success(f"Țintă Zilnică: {target:.0f} Kcal (RMB: {rmb:.0f})")
    st.info(f"Necesar Nutrienți: P: {p_g:.0f}g | L: {l_g:.0f}g | G: {c_g:.0f}g")

with t2:
    if st.button("🤖 Agent AI: Generează Plan 7 Zile (5 Mese)"):
        zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
        # Distribuția pe mese conform standardului profesional
        dist = {"Mic Dejun": 0.25, "Gustare 1": 0.10, "Prânz": 0.35, "Gustare 2": 0.10, "Cină": 0.20}
        
        full_plan = []
        for zi in zile:
            for masa, proc in dist.items():
                cat = "Gustări" if "Gustare" in masa else masa
                aliment = random.choice(list(db[cat].keys()))
                vals = db[cat][aliment]
                
                kcal_m = target * proc
                gramaj = (kcal_m / vals) * 100
                p_m = (gramaj * vals[12]) / 100
                l_m = (gramaj * vals[17]) / 100
                g_m = (gramaj * vals[28]) / 100
                
                full_plan.append({"Zi": zi, "Masă": masa, "Preparat": aliment, "Gramaj": f"{gramaj:.0f}g", 
                                  "P": round(p_m,1), "L": round(l_m,1), "G": round(g_m,1)})
        
        df = pd.DataFrame(full_plan)
        for zi in zile:
            with st.expander(f"📅 Meniu {zi}"):
                st.table(df[df["Zi"] == zi][["Masă", "Preparat", "Gramaj", "P", "L", "G"]])
