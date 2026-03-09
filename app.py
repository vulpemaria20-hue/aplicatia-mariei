import streamlit as st
import pandas as pd

# 1. CONFIGURARE ȘI SECURITATE
st.set_page_config(page_title="Nutriția Matematică - Sistem Expert", layout="wide")

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Acces Protejat")
    pwd = st.text_input("Parolă de acces:", type="password")
    if st.button("Autentificare"):
        if pwd == "nutrifit2026":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Acces respins!")
    st.stop()

# 2. BAZA DE DATE EXTINSĂ (Exemplu structură pentru 200+ repere)
# Puteți adăuga alimente noi în aceste liste
db_alimente = {
    "Mic Dejun": {"Omletă": 155, "Smoothie Verde": 54.2, "Budincă Chia": 105.4, "Brioșe Legume": 95, "Ovăz": 389, "Ou Fiert": 155, "Pâine integrală": 247, "Iaurt grecesc": 69, "Brânză vaci": 98, "Clătite proteice": 170},
    "Gustări": {"Banană": 89, "Măr": 52, "Nuci": 654, "Kinder Felie Lapte": 135.88, "Baton proteic": 380, "Migdale": 579, "Iaurt 2%": 65, "Caju": 553, "Afine": 57, "Biscuiți digestivi": 450},
    "Prânz": {"Tocană legume": 29.15, "Mâncare linte": 188.41, "Somon file": 208, "Pui grătar": 165, "Orez integral": 150.4, "Iahnie fasole": 125, "Curcan": 135, "Vită": 250, "Quinoa": 120, "Paste": 150},
    "Cină": {"Salată ton": 158, "Supă cremă": 45, "Cod": 105, "Tofu": 95, "Curcan abur": 104, "Creveți": 99, "Dovlecei": 35, "Salată grecească": 115, "Sufleu dovlecei": 90, "Omletă spanac": 140}
}

# 3. IDENTIFICARE CLIENT ȘI CALCULATOR
st.sidebar.title("👥 Management Client")
nume = st.sidebar.text_input("Nume Client:", placeholder="Ex: Maria Popescu")

if not nume:
    st.info("Introduceți numele clientului în sidebar.")
    st.stop()

st.header(f"📊 Evaluare Matematică: {nume}")

with st.expander("⚙️ Date Biometrice și Activitate", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        sex = st.selectbox("Sex", ["Feminin", "Masculin"])
        varsta = st.number_input("Vârstă (ani)", 15, 95, 35)
        greutate = st.number_input("Greutate (kg)", 40.0, 250.0, 100.0)
    with c2:
        inaltime = st.number_input("Înălțime (cm)", 120, 220, 170)
        # Cerința: Activitate detaliată
        nivel = st.selectbox("Nivel Activitate (IC)", [
            "Sedentar (Birou/Fără sport) - 25 kcal/kg",
            "Ușor Activ (Mișcare ușoară) - 30 kcal/kg",
            "Moderat Activ (Sport 3-5 zile) - 35 kcal/kg",
            "Activ (Sport zilnic) - 40 kcal/kg",
            "Foarte Activ (Muncă fizică/Performanță) - 45 kcal/kg"
        ])
        ic = int(nivel.split("- ")[1].split(" ")[0])
    with c3:
        obiectiv = st.radio("Obiectiv", ["Menținere", "Slăbire"])
        deficit = 0
        if obiectiv == "Slăbire":
            deficit = st.slider("Deficit dorit (kcal)", 500, 1000, 500)

# LOGICĂ MATEMATICĂ VASILE BOGDAN
rmb = (greutate * 24) if sex == "Masculin" else (greutate * 0.8 * 24)
tnc_initial = greutate * ic
tinta_finala = tnc_initial - deficit

# Afișare rezultate
st.divider()
r1, r2, r3 = st.columns(3)
r1.metric("RMB (Bazal)", f"{int(rmb)} kcal")
r2.metric("TNC (Inițial)", f"{int(tnc_initial)} kcal")
r3.metric("Țintă Dietă", f"{int(tinta_finala)} kcal", delta=f"-{deficit}" if deficit > 0 else None)

if tinta_finala < rmb:
    st.warning(f"⚠️ Atenție: Targetul este sub RMB ({int(rmb)} kcal). Risc de încetinire metabolică!")

# 4. PLANIFICATOR SĂPTĂMÂNAL (7 ZILE X 5 MESE)
st.header("🗓️ Planificator Săptămânal")

zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
distributie = {"Mic Dejun": 0.25, "Gustare 1": 0.10, "Prânz": 0.35, "Gustare 2": 0.10, "Cină": 0.20}

for zi in zile:
    with st.expander(f"📅 Meniu {zi}"):
        cols = st.columns(5)
        mese_alese = {}
        
        # Interfață selecție
        mese_alese["Mic Dejun"] = cols[0].selectbox("Mic Dejun", list(db_alimente["Mic Dejun"].keys()), key=f"md_{zi}")
        mese_alese["Gustare 1"] = cols[1].selectbox("Gustare 1", list(db_alimente["Gustări"].keys()), key=f"g1_{zi}")
        mese_alese["Prânz"] = cols[2].selectbox("Prânz", list(db_alimente["Prânz"].keys()), key=f"p_{zi}")
        mese_alese["Gustare 2"] = cols[3].selectbox("Gustare 2", list(db_alimente["Gustări"].keys()), key=f"g2_{zi}")
        mese_alese["Cină"] = cols[4].selectbox("Cină", list(db_alimente["Cină"].keys()), key=f"c_{zi}")

        # AGENT AI: Calcul Gramaje
        plan_zi = []
        for masa, aliment in mese_alese.items():
            # Identificăm categoria corectă pentru baza de date
            cat = "Gustări" if "Gustare" in masa else masa
            kcal_100g = db_alimente[cat][aliment]
            kcal_masa = tinta_finala * distributie[masa]
            gramaj = (kcal_masa / kcal_100g) * 100
            
            plan_zi.append({"Masă": masa, "Aliment": aliment, "Gramaj AI": f"{int(gramaj)}g", "Kcal": int(kcal_masa)})
        
        st.table(pd.DataFrame(plan_zi))

if st.button("🤖 Agent AI: Salvează Raport Client"):
    st.balloons()
    st.success(f"Planul pentru {nume} a fost salvat cu succes!")
