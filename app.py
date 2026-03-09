import streamlit as st
import pandas as pd

# CONFIGURARE PAGINA
st.set_page_config(page_title="Aplicația Mariei", page_icon="🍎", layout="wide")

# DESIGN
st.markdown("""
<style>
.stButton>button {
    background-color:#2ecc71;
    color:white;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# AUTENTIFICARE
if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.title("🔐 Acces Aplicația Mariei")

    parola = st.text_input("Parolă",type="password")

    if st.button("Login"):
        if parola=="nutrifit2026":
            st.session_state.login=True
            st.rerun()
        else:
            st.error("Parolă greșită")

    st.stop()

# INITIALIZARE
if "kcal" not in st.session_state:
    st.session_state.kcal=1800

if "lista" not in st.session_state:
    st.session_state.lista=[]

# TITLU PRINCIPAL
st.title("🍎 Aplicația Mariei – Planner Nutrițional")

tab1,tab2,tab3 = st.tabs([
"📊 Calculator caloric",
"🍱 Plan alimentar",
"🛒 Lista cumpărături"
])

# ====================================================
# CALCULATOR CALORIC
# ====================================================

with tab1:

    st.subheader("Calculator metabolic")

    col1,col2 = st.columns(2)

    with col1:

        greutate = st.number_input("Greutate kg",40,200,70)

        inaltime = st.number_input("Înălțime cm",140,220,170)

        varsta = st.number_input("Vârstă",18,90,35)

        sex = st.radio("Sex",["Masculin","Feminin"])

    with col2:

        activitate = st.selectbox("Nivel activitate",
        [
        ("Sedentar",1.2),
        ("Ușor activ",1.375),
        ("Moderat activ",1.55),
        ("Foarte activ",1.725)
        ])

        deficit = st.slider("Deficit caloric",300,900,500)

        proteine = st.slider("Proteine g/kg",1.2,2.5,1.8)

    if st.button("Calculează necesarul"):

        if sex=="Masculin":
            rmb = 10*greutate + 6.25*inaltime - 5*varsta + 5
        else:
            rmb = 10*greutate + 6.25*inaltime - 5*varsta - 161

        tdee = rmb*activitate[1]

        target = tdee-deficit

        bmi = greutate/((inaltime/100)**2)

        proteine_total = greutate*proteine
        kcal_prot = proteine_total*4

        grasimi = target*0.25/9
        kcal_grasimi = grasimi*9

        carbo = (target - kcal_prot - kcal_grasimi)/4

        st.session_state.kcal=target

        st.success(f"Calorii zilnice: {target:.0f} kcal")

        st.write(f"BMI: {bmi:.1f}")

        st.write("Macronutrienți zilnici")

        st.write(f"Proteine: {proteine_total:.0f} g")
        st.write(f"Grăsimi: {grasimi:.0f} g")
        st.write(f"Carbohidrați: {carbo:.0f} g")

# ====================================================
# BAZA DE DATE ALIMENTE
# ====================================================

alimente = {

"Omletă":155,
"Ovăz":389,
"Iaurt grecesc":97,
"Budincă chia":180,
"Smoothie proteic":120,

"Măr":52,
"Banana":89,
"Portocală":47,
"Migdale":575,
"Nuci":654,

"Pui grătar":165,
"Curcan":140,
"Somon":208,
"Ton":132,
"Vită slabă":250,

"Orez":130,
"Cartofi":77,
"Quinoa":120,

"Salată pui":120,
"Salată ton":110,

"Supă cremă":50,
"Pește alb":90
}

# ====================================================
# PLAN ALIMENTAR
# ====================================================

with tab2:

    st.subheader(f"Plan alimentar – țintă {st.session_state.kcal:.0f} kcal")

    distributie={
    "MD":0.25,
    "G1":0.10,
    "PZ":0.35,
    "G2":0.10,
    "CN":0.20
    }

    st.session_state.lista=[]

    zile=["Luni","Marți","Miercuri","Joi","Vineri","Sâmbătă","Duminică"]

    tabel=[]

    for zi in zile:

        with st.expander(zi):

            cols=st.columns(5)

            md = cols[0].selectbox("Mic dejun",
            ["Ovăz","Omletă","Iaurt grecesc","Budincă chia"],
            key=f"md{zi}")

            g1 = cols[1].selectbox("Gustare",
            ["Măr","Banana","Migdale","Nuci"],
            key=f"g1{zi}")

            pz = cols[2].selectbox("Prânz",
            ["Pui grătar","Curcan","Somon","Ton","Vită slabă"],
            key=f"pz{zi}")

            g2 = cols[3].selectbox("Gustare 2",
            ["Iaurt grecesc","Migdale","Nuci"],
            key=f"g2{zi}")

            cn = cols[4].selectbox("Cină",
            ["Supă cremă","Pește alb","Salată pui","Salată ton"],
            key=f"cn{zi}")

            def calc(food,ratio):

                kcal = st.session_state.kcal*ratio

                gr = kcal/alimente[food]*100

                return gr

            gr_md=calc(md,distributie["MD"])
            gr_g1=calc(g1,distributie["G1"])
            gr_pz=calc(pz,distributie["PZ"])
            gr_g2=calc(g2,distributie["G2"])
            gr_cn=calc(cn,distributie["CN"])

            tabel.append({
            "Zi":zi,
            "Mic dejun":f"{md} {gr_md:.0f} g",
            "Gustare":f"{g1} {gr_g1:.0f} g",
            "Prânz":f"{pz} {gr_pz:.0f} g",
            "Gustare 2":f"{g2} {gr_g2:.0f} g",
            "Cină":f"{cn} {gr_cn:.0f} g"
            })

            st.session_state.lista.extend([
            (md,gr_md),
            (g1,gr_g1),
            (pz,gr_pz),
            (g2,gr_g2),
            (cn,gr_cn)
            ])

    df=pd.DataFrame(tabel)

    st.table(df)

    csv=df.to_csv(index=False).encode("utf-8-sig")

    st.download_button("📥 Descarcă plan alimentar",
                       csv,
                       "plan_aplicatia_mariei.csv")

# ====================================================
# LISTA CUMPARATURI
# ====================================================

with tab3:

    st.subheader("🛒 Lista cumpărături")

    if len(st.session_state.lista)>0:

        df_lista=pd.DataFrame(st.session_state.lista,
        columns=["aliment","cantitate"])

        total=df_lista.groupby("aliment").sum().reset_index()

        for i,row in total.iterrows():

            st.write(f"✅ {row['aliment']} — {row['cantitate']:.0f} g")

        csv=total.to_csv(index=False).encode("utf-8-sig")

        st.download_button("📥 Descarcă lista cumpărături",
                           csv,
                           "lista_cumparaturi_aplicatia_mariei.csv")

    else:

        st.info("Configurează planul alimentar pentru a genera lista.")