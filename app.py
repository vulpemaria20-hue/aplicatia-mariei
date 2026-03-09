import streamlit as st
import pandas as pd

# CONFIG PAGINA
st.set_page_config(page_title="Nutriția Matematică - Sistem Expert", page_icon="🍎", layout="wide")

# -----------------------------
# SISTEM LOGIN
# -----------------------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.title("🔐 Acces Protejat - Sistem Expert")

    parola = st.text_input("Introduceți parola:", type="password")

    if st.button("Autentificare"):

        if parola == "nutrifit2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Parolă incorectă!")

    st.stop()

# -----------------------------
# SIDEBAR CLIENT
# -----------------------------
st.sidebar.title("👥 Gestiune Client")

nume_client = st.sidebar.text_input("Nume client:", placeholder="Ex: Ion Popescu")

if not nume_client:
    st.info("Introduceți numele clientului pentru a continua.")
    st.stop()

# -----------------------------
# BAZA ALIMENTE
# kcal / 100g
# -----------------------------
baza_alimente = {

"Tocană de legume":29.15,
"Mâncare de linte":188.41,
"Humus":230.9,
"Orez integral cu legume":150.4,
"Salată de ton":158.0,
"Omletă":155.0,
"Smoothie Verde":54.2,
"Smoothie Fructe Pădure":114.6,
"Smoothie Mango & Cătină":94.2,
"Kinder Felie de Lapte":135.88,
"Brioșe Spanac & Banană":247.46,
"Budincă Chia":105.4,
"Brioșe din Legume":95.0,
"Somon file":208.0,
"Iaurt grecesc 2%":69.0,
"Banana":89.0,
"Cod la grătar":150.0

}

# -----------------------------
# FUNCTIE RMB
# -----------------------------
def calcul_rmb(greutate, sex, varsta):

    if varsta >= 65:
        factor = 0.9 if sex == "Masculin" else 0.8
    else:
        factor = 1.0 if sex == "Masculin" else 0.8

    return factor * greutate * 24

# -----------------------------
# INTERFATA
# -----------------------------
st.title(f"⚖️ Plan Nutrițional Personalizat - {nume_client}")

tab1, tab2, tab3 = st.tabs(["📊 Calculator", "🔍 Evaluare", "🍱 Plan 7 Zile"])

# ==================================================
# TAB 1 CALCULATOR
# ==================================================
with tab1:

    col1, col2 = st.columns(2)

    with col1:

        tip = st.selectbox("Categorie", ["Adult (18-65)", "Senior (>65)", "Copil/Adolescent"])

        greutate = st.number_input("Greutate (kg)",10.0,250.0,70.0)

        inaltime = st.number_input("Înălțime (cm)",80,230,170)

        varsta = st.number_input("Vârstă",2,100,35)

        sex = st.radio("Sex",["Masculin","Feminin"])

    with col2:

        if tip == "Copil/Adolescent":

            if varsta < 7:
                tnc = 1400
            elif varsta < 10:
                tnc = 1800
            elif varsta < 14:
                tnc = 2500 if sex == "Masculin" else 2250
            else:
                tnc = 3250 if sex == "Masculin" else 2400

        else:

            activitate = st.selectbox("Nivel activitate",[
            "Sedentar (25-30 kcal/kg)",
            "Ușor (30-35 kcal/kg)",
            "Mediu (35-40 kcal/kg)",
            "Mare (40-45 kcal/kg)"
            ])

            ic_text = activitate.split("(")[1].split(" ")[0]

            ic_min, ic_max = map(int, ic_text.split("-"))

            ic = (ic_min + ic_max) / 2

            tnc = greutate * ic

        obiectiv = st.radio("Obiectiv",["Menținere","Scădere","Creștere"])

        target = tnc

        if obiectiv == "Scădere":
            target -= 500

        if obiectiv == "Creștere":
            target += 500

    if st.button("Generează Analiză"):

        rmb = calcul_rmb(greutate,sex,varsta)

        bmi = greutate / ((inaltime/100)**2)

        st.subheader("Rezultate")

        c1,c2,c3 = st.columns(3)

        c1.metric("Target kcal",f"{target:.0f}")

        c2.metric("RMB",f"{rmb:.0f}")

        c3.metric("IMC",f"{bmi:.1f}")

        if target < rmb:
            st.error("⚠️ Target sub RMB!")

# ==================================================
# TAB 2 EVALUARE
# ==================================================
with tab2:

    st.subheader("Evaluare la 2 săptămâni")

    c1,c2 = st.columns(2)

    with c1:

        st.write("Plicometrie")

        p1 = st.number_input("Pliu triceps",0.0)

        p2 = st.number_input("Pliu abdomen",0.0)

    with c2:

        st.write("Circumferințe")

        talie = st.number_input("Talie",40)

    st.info("Scăderea taliei + greutate = progres corect.")

# ==================================================
# TAB 3 PLAN 7 ZILE
# ==================================================
with tab3:

    st.subheader("🍱 Plan Alimentar 7 Zile")

    zile = ["Luni","Marți","Miercuri","Joi","Vineri","Sâmbătă","Duminică"]

    dist = {
    "MD":0.25,
    "G1":0.10,
    "PZ":0.30,
    "G2":0.10,
    "CN":0.25
    }

    def calc_g(food, ratio):

        gramaj = (target * ratio / baza_alimente[food]) * 100

        return max(200, gramaj)

    plan = []

    for zi in zile:

        st.markdown(f"### {zi}")

        c1,c2,c3 = st.columns(3)

        with c1:

            md = st.selectbox(
            f"Mic dejun {zi}",
            list(baza_alimente.keys()),
            key=f"md_{zi}"
            )

            g1 = st.selectbox(
            f"Gustare 1 {zi}",
            list(baza_alimente.keys()),
            key=f"g1_{zi}"
            )

        with c2:

            pz = st.selectbox(
            f"Prânz {zi}",
            list(baza_alimente.keys()),
            key=f"pz_{zi}"
            )

            g2 = st.selectbox(
            f"Gustare 2 {zi}",
            list(baza_alimente.keys()),
            key=f"g2_{zi}"
            )

        with c3:

            cn = st.selectbox(
            f"Cină {zi}",
            list(baza_alimente.keys()),
            key=f"cn_{zi}"
            )

        plan.append({

        "Zi":zi,
        "Mic Dejun":f"{md} - {calc_g(md,dist['MD']):.0f} g",
        "Gustare1":f"{g1} - {calc_g(g1,dist['G1']):.0f} g",
        "Prânz":f"{pz} - {calc_g(pz,dist['PZ']):.0f} g",
        "Gustare2":f"{g2} - {calc_g(g2,dist['G2']):.0f} g",
        "Cină":f"{cn} - {calc_g(cn,dist['CN']):.0f} g"

        })

    df = pd.DataFrame(plan)

    st.markdown("## 📋 Meniu final")

    st.dataframe(df, use_container_width=True)