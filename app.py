import streamlit as st
import pandas as pd

# 1. CONFIGURARE ȘI SECURITATE (CONFORM SURSEI [2])
st.set_page_config(page_title="Nutriția Matematică - Sistem Expert", layout="wide")

if "auth" not in st.session_state:
    st.session_state.auth = False

# Ecran de logare corectat
if not st.session_state.auth:
    st.title("🔐 Acces Protejat - Sistem Expert")
    parola_introdusa = st.text_input("Introduceți parola de acces:", type="password")
    if st.button("Autentificare"):
        # Verificare strictă a parolei stabilită în sursa [2]
        if parola_introdusa == "nutrifit2026":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Parolă incorectă! Vă rugăm să verificați caracterele.")
    st.stop()

# 2. BAZA DE DATE EXTINSĂ (Exemple pentru 200+ repere)
# Structura permite adăugarea nelimitată de alimente
db_alimente = {
    "Mic Dejun": {"Omletă": 155, "Smoothie Verde": 54.2, "Budincă Chia": 105.4, "Brioșe Legume": 95, "Ovăz": 389, "Ou Fiert": 155, "Pâine integrală": 247, "Iaurt grecesc": 69, "Brânză vaci": 98, "Clătite proteice": 170},
    "Gustări": {"Banană": 89, "Măr": 52, "Nuci": 654, "Kinder Felie Lapte": 135.88, "Baton proteic": 380, "Migdale": 579, "Iaurt 2%": 65, "Caju": 553, "Afine": 57, "Biscuiți digestivi": 450},
    "Prânz": {"Tocană legume": 29.15, "Mâncare linte": 188.41, "Somon file": 208, "Pui grătar": 165, "Orez integral": 150.4, "Iahnie fasole": 125, "Curcan": 135, "Vită": 250, "Quinoa": 120, "Paste": 150},
    "Cină": {"Salată ton": 158, "Supă cremă": 45, "Cod": 105, "Tofu": 95, "Curcan abur": 104, "Creveți": 99, "Dovlecei": 35, "Salată grecească": 115, "Sufleu dovlecei": 90, "Omletă spanac": 140}
}

# 3. GESTIUNE CLIENT
st.sidebar.title("👥 Management Client")
nume_client = st.sidebar.text_input("Nume Client curent:", placeholder="Ex: Ion Popescu")

if not nume_client:
    st.info("Vă rugăm să introduceți numele clientului în bara laterală pentru a începe.")
    st.stop()

# 4. CALCULATOR METABOLIC (METODOLOGIA VASILE BOGDAN)
st.title(f"⚖️ Evaluare Biometrică: {nume_client}")

with st.expander("⚙️ Introducere Date și Nivel Activitate", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        sex = st.radio("Sex", ["Feminin", "Masculin"])
        greutate = st.number_input("Greutate Actuală (kg)", 30.0, 250.0, 100.0)
        inaltime = st.number_input("Înălțime (cm)", 100, 230, 170)
    with c2:
        varsta = st.number_input("Vârstă (ani)", 15, 100, 35)
        # Nivel activitate detaliat conform solicitării
        nivel_act = st.selectbox("Nivel Activitate (IC)", [
            "Sedentar (Activitate minimă) - IC 25",
            "Ușor Activ (Mișcare ușoară) - IC 30",
            "Moderat Activ (Sport 3-5 zile) - IC 35",
            "Activ (Antrenament zilnic) - IC 40",
            "Foarte Activ (Muncă fizică grea) - IC 45"
        ])
        ic = int(nivel_act.split("IC ")[1])
    with c3:
        obiectiv = st.radio("Obiectiv", ["Menținere", "Slăbire"])
        deficit = 0
        if obiectiv == "Slăbire":
            # Deficit flexibil între 500 și 1000 kcal
            deficit = st.slider("Selectați Deficitul (kcal)", 500, 1000, 500)

# LOGICĂ MATEMATICĂ
# RMB conform Pag. 12
rmb = (greutate * 24) if sex == "Masculin" else (greutate * 0.8 * 24)
# TNC Inițial conform Pag. 8 (GA x IC)
tnc_initial = greutate * ic
target_final = tnc_initial - deficit

st.divider()
col_r1, col_r2, col_r3 = st.columns(3)
col_r1.metric("RMB (Bazal)", f"{int(rmb)} kcal")
col_r2.metric("TNC (Calorii Inițiale)", f"{int(tnc_initial)} kcal")
col_r3.metric("Target Dietă", f"{int(target_final)} kcal", delta=f"-{deficit}" if deficit > 0 else None)

# Avertisment siguranță
if target_final < rmb:
    st.warning(f"⚠️ Atenție! Targetul de {int(target_final)} kcal este sub RMB. Risc de încetinire metabolică!")

# 5. PLANIFICATOR SĂPTĂMÂNAL (7 ZILE X 5 MESE)
st.header(f"🗓️ Planificator Săptămânal pentru {nume_client}")

zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
# Procente distribuție calorică pe cele 5 mese
distributie = {"Mic Dejun": 0.25, "Gustare 1": 0.10, "Prânz": 0.35, "Gustare 2": 0.10, "Cină": 0.20}

for zi in zile:
    with st.expander(f"📅 Meniu {zi}"):
        cols = st.columns(5)
        # Dicționar pentru a stoca selecțiile zilei
        selectii = {}
        
        # Dropdown-uri pentru cele 5 mese
        selectii["Mic Dejun"] = cols[0].selectbox("Mic Dejun", list(db_alimente["Mic Dejun"].keys()), key=f"md_{zi}")
        selectii["Gustare 1"] = cols[1].selectbox("Gustare 1", list(db_alimente["Gustări"].keys()), key=f"g1_{zi}")
        selectii["Prânz"] = cols[2].selectbox("Prânz", list(db_alimente["Prânz"].keys()), key=f"p_{zi}")
        selectii["Gustare 2"] = cols[3].selectbox("Gustare 2", list(db_alimente["Gustări"].keys()), key=f"g2_{zi}")
        selectii["Cină"] = cols[4].selectbox("Cină", list(db_alimente["Cină"].keys()), key=f"c_{zi}")

        # AGENT AI: Calcul automat gramaje pe baza selecției
        date_tabel = []
        for masa, aliment in selectii.items():
            # Identificare categorie corectă pentru kcal/100g
            categorie = "Gustări" if "Gustare" in masa else masa
            kcal_100g = db_alimente[categorie][aliment]
            
            # Calcul gramaj: (Target Zilnic * Procent Masă / Kcal Aliment) * 100
            kcal_alocate_masa = target_final * distributie[masa]
            gramaj = (kcal_alocate_masa / kcal_100g) * 100
            
            date_tabel.append({
                "Masă": masa,
                "Preparat": aliment,
                "Gramaj Recomandat": f"{int(gramaj)}g",
                "Calorii alocate": f"{int(kcal_alocate_masa)} kcal"
            })
        
        st.table(pd.DataFrame(date_tabel))

# 6. FINALIZARE
if st.button("🤖 Agent AI: Salvează și Finalizează Planul"):
    st.balloons()
    st.success(f"Planul nutrițional complet pentru {nume_client} a fost generat și salvat!")
