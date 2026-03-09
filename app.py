import streamlit as st
import pandas as pd

# ------------------------------------------------
# CONFIGURARE PAGINA
# ------------------------------------------------

st.set_page_config(
    page_title="Nutriția Matematică - Sistem Expert",
    page_icon="🍎",
    layout="wide"
)

# ------------------------------------------------
# LOGIN
# ------------------------------------------------

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.title("🔐 Acces Sistem Expert Nutrițional")

    parola = st.text_input("Introduceți parola", type="password")

    if st.button("Autentificare"):

        if parola == "nutrifit2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Parolă incorectă")

    st.stop()

# ------------------------------------------------
# SIDEBAR CLIENT
# ------------------------------------------------

st.sidebar.title("👤 Client")

nume_client = st.sidebar.text_input(
    "Nume client",
    placeholder="Ex: Ion Popescu"
)

if not nume_client:
    st.info("Introduceți numele clientului în sidebar.")
    st.stop()

# ------------------------------------------------
# BAZA DE DATE ALIMENTE (kcal / 100g)
# ------------------------------------------------

baza_alimente = {

"Omletă":155,
"Iaurt grecesc 2%":69,
"Budincă Chia":105,
"Smoothie Verde":54,
"Smoothie Mango & Cătină":94,
"Brioșe din Legume":95,
"Banana":89,

"Tocană de legume":29,
"Mâncare de linte":188,
"Somon file":208,
"Orez integral cu legume":150,
"Cod la grătar":150,
"Humus":230,

"Salată de ton":158,

"Smoothie Fructe Pădure":114,
"Brioșe Spanac & Banană":247,
"Kinder Felie de Lapte":135

}

# ------------------------------------------------
# LISTE ALIMENTE PE MASĂ
# ------------------------------------------------

mic_dejun = [
"Omletă",
"Iaurt grecesc 2%",
"Budincă Chia",
"Smoothie Verde",
"Smoothie Mango & Cătină",
"Brioșe din Legume",
"Banana"
]

pranz = [
"Tocană de legume",
"Mâncare de linte",
"Somon file",
"Orez integral cu legume",
"Cod la grătar",
"Humus"
]

cina = [
"Salată de ton",
"Cod la grătar",
"Humus",
"Omletă",
"Iaurt grecesc 2%"
]

gustari = [
"Banana",
"Smoothie Fructe Pădure",
"Brioșe Spanac & Banană",
"Iaurt grecesc 2%",
"Kinder Felie de Lapte"
]

# ------------------------------------------------
# FUNCTIE RMB
# ------------------------------------------------

def calcul_rmb(greutate, sex, varsta):

    if sex == "Masculin":
        factor = 24
    else:
        factor = 22

    return greutate * factor

# ------------------------------------------------
# INTERFATA
# ------------------------------------------------

st.title(f"⚖️ Plan Nutrițional Personalizat - {nume_client}")

tab1, tab2, tab3 = st.tabs([
"📊 Calculator caloric",
"📉 Evaluare progres",
"🍱 Plan alimentar 7 zile"
])

# ------------------------------------------------
# TAB 1 CALCULATOR
# ------------------------------------------------

with tab1:

    c1, c2 = st.columns(2)

    with c1:

        greutate = st.number_input("Greutate (kg)",10.0,250.0,70.0)

        inaltime = st.number_input("Înălțime (cm)",80,230,170)

        varsta = st.number_input("Vârstă",2,100,35)

        sex = st.radio("Sex",["Masculin","Feminin"])

    with c2:

        activitate = st.selectbox(
        "Nivel activitate",
        [
        "Sedentar (25 kcal/kg)",
        "Ușor (30 kcal/kg)",
        "Mediu (35 kcal/kg)",
        "Intens (40 kcal/kg)"
        ])

        if "25" in activitate:
            factor = 25
        elif "30" in activitate:
            factor = 30
        elif "35" in activitate:
            factor = 35
        else:
            factor = 40

        tnc = greutate * factor

        obiectiv = st.radio(
        "Obiectiv",
        ["Menținere","Scădere","Creștere"]
        )

        target = tnc

        if obiectiv == "Scădere":
            target -= 500

        if obiectiv == "Creștere":
            target += 500

    if st.button("Generează analiză"):

        rmb = calcul_rmb(greutate, sex, varsta)

        bmi = greutate / ((inaltime/100)**2)

        r1,r2,r3 = st.columns(3)

        r1.metric("Target caloric",f"{target:.0f} kcal")

        r2.metric("RMB",f"{rmb:.0f} kcal")

        r3.metric("IMC",f"{bmi:.1f}")

        if target < rmb:
            st.warning("Targetul este sub metabolismul bazal.")

# ------------------------------------------------
# TAB 2 EVALUARE
# ------------------------------------------------

with tab2:

    st.subheader("Evaluare la 2 săptămâni")

    c1,c2 = st.columns(2)

    with c1:

        st.write("Plicometrie")

        pli_triceps = st.number_input("Pliu triceps",0.0)

        pli_abdomen = st.number_input("Pliu abdomen",0.0)

    with c2:

        st.write("Circumferințe")

        talie = st.number_input("Talie (cm)",40)

    st.info("Scăderea greutății + scăderea taliei indică progres.")

# ------------------------------------------------
# TAB 3 PLAN ALIMENTAR
# ------------------------------------------------

with tab3:

    st.subheader("🍱 Plan alimentar săptămânal")

    zile = [
    "Luni","Marți","Miercuri",
    "Joi","Vineri","Sâmbătă","Duminică"
    ]

    distributie = {
    "MD":0.25,
    "G1":0.10,
    "PZ":0.30,
    "G2":0.10,
    "CN":0.25
    }

    def calc_g(aliment, ratio):

        gramaj = (target * ratio / baza_alimente[aliment]) * 100

        if gramaj < 200:
            gramaj = 200

        return gramaj

    plan = []

    for zi in zile:

        st.markdown(f"### 📅 {zi}")

        col1,col2,col3 = st.columns(3)

        with col1:

            md = st.selectbox(
            "Mic dejun",
            mic_dejun,
            key=f"md{zi}"
            )

            g1 = st.selectbox(
            "Gustare 1",
            gustari,
            key=f"g1{zi}"
            )

        with col2:

            pz = st.selectbox(
            "Prânz",
            pranz,
            key=f"pz{zi}"
            )

            g2 = st.selectbox(
            "Gustare 2",
            gustari,
            key=f"g2{zi}"
            )

        with col3:

            cn = st.selectbox(
            "Cină",
            cina,
            key=f"cn{zi}"
            )

        plan.append({

        "Zi":zi,

        "Mic Dejun":
        f"{md} - {calc_g(md,distributie['MD']):.0f} g",

        "Gustare 1":
        f"{g1} - {calc_g(g1,distributie['G1']):.0f} g",

        "Prânz":
        f"{pz} - {calc_g(pz,distributie['PZ']):.0f} g",

        "Gustare 2":
        f"{g2} - {calc_g(g2,distributie['G2']):.0f} g",

        "Cină":
        f"{cn} - {calc_g(cn,distributie['CN']):.0f} g"

        })

    df = pd.DataFrame(plan)

    st.markdown("## 📋 Meniu final")

    st.dataframe(df, use_container_width=True)
