import streamlit as st
import pandas as pd
import random
import io
import json
import os

# CONFIG PAGINA
st.set_page_config(page_title="Sistem Expert Nutriție", page_icon="⚖️", layout="wide")

# LOGIN
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.title("🔐 Acces aplicație")

    parola = st.text_input("Introduceți parola:", type="password")

    if st.button("Autentificare"):

        if parola == "nutrifit2026":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Parolă incorectă!")

    st.stop()


# -------------------------------
# BAZA DE DATE JSON
# -------------------------------

db_file = "alimente.json"

default_db = {

"Mic Dejun": {
"Omletă cu brânză":156,
"Budincă Chia":105.4,
"Brioșe legume":95,
"Humus clasic":230.9,
"Ouă fierte":155,
"Pâine integrală":223.3,
"Cremă urdă mărar":137,
"Zacuscă vinete":92
},

"Gustări":{
"Smoothie Verde":54.2,
"Măr verde":52,
"Banana":89,
"Iaurt grecesc 2%":69,
"Migdale":575,
"Nuci":654,
"Grapefruit":32,
"Căpșuni":32
},

"Prânz":{
"Tocană de legume":29.15,
"Mâncare de linte":188.41,
"Orez integral legume":150.4,
"Piept curcan grătar":107,
"Somon file":208,
"Rasol vită":133,
"Supă pui":24.14,
"Iahnie fasole":154.1,
"Mămăligă":66
},

"Cină":{
"Salată ton avocado":158,
"Cod la grătar":107,
"Supă cremă conopidă":86.8,
"Creveți rucola":85,
"Zucchini grătar":17,
"Paste integrale":340,
"Salată pui crudități":110,
"Piure mazăre":84
}

}

# incarcare baza
if os.path.exists(db_file):
    with open(db_file,"r") as f:
        db_alimente=json.load(f)
else:
    db_alimente=default_db

# salvare functie
def save_db():
    with open(db_file,"w") as f:
        json.dump(db_alimente,f)


# -------------------------------
# CRUD ALIMENTE
# -------------------------------

st.header("🗄️ Administrare Alimente")

tab1,tab2,tab3,tab4=st.tabs(["📖 Vizualizare","➕ Adaugă","✏️ Editează","❌ Șterge"])

# VIEW
with tab1:

    for cat,alim in db_alimente.items():

        st.subheader(cat)

        df=pd.DataFrame(list(alim.items()),columns=["Aliment","Kcal / 100g"])

        st.dataframe(df,use_container_width=True)


# CREATE
with tab2:

    categorie=st.selectbox("Categorie",list(db_alimente.keys()))

    nume=st.text_input("Nume aliment")

    kcal=st.number_input("Kcal / 100g",0.0,1000.0,100.0)

    if st.button("Adaugă"):

        if nume in db_alimente[categorie]:

            st.warning("Alimentul există deja!")

        else:

            db_alimente[categorie][nume]=kcal

            save_db()

            st.success("Aliment adăugat")


# UPDATE
with tab3:

    categorie=st.selectbox("Categorie editare",list(db_alimente.keys()))

    aliment=st.selectbox("Aliment",list(db_alimente[categorie].keys()))

    kcal_nou=st.number_input(
        "Kcal noi",
        0.0,
        1000.0,
        float(db_alimente[categorie][aliment])
    )

    if st.button("Salvează modificare"):

        db_alimente[categorie][aliment]=kcal_nou

        save_db()

        st.success("Actualizat")


# DELETE
with tab4:

    categorie=st.selectbox("Categorie ștergere",list(db_alimente.keys()))

    aliment=st.selectbox("Aliment de șters",list(db_alimente[categorie].keys()))

    if st.button("Șterge"):

        del db_alimente[categorie][aliment]

        save_db()

        st.success("Aliment șters")


st.divider()


# -------------------------------
# COMBINATII
# -------------------------------

db_combinatii = {
    "Mic Dejun":[
        {"Omletă cu brânză":156, "Pâine integrală":223.3},
        {"Budincă Chia":105.4, "Fructe":50},
        {"Brioșe legume":95, "Humus clasic":230.9}
    ],
    "Prânz":[
        {"Piept curcan grătar":107, "Mămăligă":66, "Salată":50},
        {"Somon file":208, "Orez integral legume":150.4, "Zucchini grătar":17},
        {"Rasol vită":133, "Iahnie fasole":154.1}
    ],
    "Cină":[
        {"Salată ton avocado":158, "Pâine integrală":50},
        {"Cod la grătar":107, "Piure mazăre":84, "Salată":30},
        {"Creveți rucola":85, "Zucchini grătar":17}
    ],
    "Gustări":[
        {"Smoothie Verde":54.2},
        {"Măr verde":52, "Migdale":50},
        {"Banana":89, "Nuci":50},
    ]
}


# -------------------------------
# SIDEBAR PROFIL CLIENT
# -------------------------------

st.sidebar.header("👤 Profil Client")

nume=st.sidebar.text_input("Nume","Maria")
greutate=st.sidebar.number_input("Greutate",40,200,70)
inaltime=st.sidebar.number_input("Înălțime",130,220,170)
varsta=st.sidebar.number_input("Vârstă",18,95,35)
sex=st.sidebar.radio("Sex",["Masculin","Feminin"])

ic_map={
"Sedentar":25,
"Ușor":30,
"Mediu":35,
"Mare":40,
"Sportiv":45
}

activitate=st.sidebar.selectbox("Activitate",list(ic_map.keys()))
ic=ic_map[activitate]

deficit=st.sidebar.slider("Deficit caloric",0,800,300)
variante=st.sidebar.slider("Variante meniu",1,4,2)


# -------------------------------
# CALCULURI
# -------------------------------

rmb=(1 if sex=="Masculin" else 0.8)*greutate*24

tnc=greutate*ic
target=tnc-deficit

if target<rmb:
    target=rmb
    st.sidebar.warning("Target limitat la RMB")

p_gr=greutate*(1.7 if ic>=35 else 1.2)
l_gr=greutate*(1.0 if ic>=35 else 0.8)
c_gr=(target-(p_gr*4)-(l_gr*9))/4


# -------------------------------
# KPI
# -------------------------------

st.title(f"⚖️ Plan Nutrițional: {nume}")

col1,col2,col3,col4=st.columns(4)

col1.metric("Calorii",round(target))
col2.metric("Proteine",round(p_gr))
col3.metric("Lipide",round(l_gr))
col4.metric("Carbo",round(c_gr))


chart=pd.DataFrame({
"Macro":["Proteine","Lipide","Carbo"],
"g":[p_gr,l_gr,c_gr]
})

st.bar_chart(chart.set_index("Macro"))

st.divider()


# -------------------------------
# GENERATOR PLAN
# -------------------------------

if st.button("🤖 Generează plan alimentar"):

    zile=["Luni","Marți","Miercuri","Joi","Vineri","Sâmbătă","Duminică"]

    distributie={
        "Mic Dejun":0.25,
        "Gustare 1":0.10,
        "Prânz":0.35,
        "Gustare 2":0.10,
        "Cină":0.20
    }

    plan=[]

    for zi in zile:

        for v in range(1,variante+1):

            for masa,proc in distributie.items():

                cat="Gustări" if "Gustare" in masa else masa

                alegere=random.choice(db_combinatii[cat])

                kcal_masa=target*proc
                total_kcal=sum(alegere.values())

                factor=kcal_masa/total_kcal

                for aliment,kcal100 in alegere.items():

                    gramaj=(kcal100*factor)/(kcal100/100)

                    plan.append({
                    "Zi":zi,
                    "Variantă":v,
                    "Masă":masa,
                    "Aliment":aliment,
                    "Cantitate":round(gramaj),
                    "Kcal":round(kcal100*factor)
                    })

    df=pd.DataFrame(plan)

    for zi in zile:

        with st.expander(zi):

            df_zi=df[df["Zi"]==zi]

            for v in df_zi["Variantă"].unique():

                st.subheader(f"Variantă {v}")

                df_v=df_zi[df_zi["Variantă"]==v]

                st.table(df_v[["Masă","Aliment","Cantitate","Kcal"]])

                st.info(f"Total calorii {df_v['Kcal'].sum()} kcal")


    buffer=io.BytesIO()

    with pd.ExcelWriter(buffer,engine="openpyxl") as writer:

        df.to_excel(writer,index=False)

    buffer.seek(0)

    st.download_button(
    "📥 Descarcă Excel",
    buffer,
    "plan_nutritie.xlsx"
    )

else:

    st.info("Apasă pe buton pentru generare plan")
