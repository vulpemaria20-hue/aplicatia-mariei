import streamlit as st
import pandas as pd
import random
import io

st.set_page_config(page_title="Sistem Expert Nutriție", page_icon="⚖️", layout="wide")

# BAZĂ DATE ALIMENTE
db_alimente = {

"Mic Dejun": {
"Omletă cu brânză":156,
"Budincă Chia":105.4,
"Brioșe legume":95,
"Humus clasic":230.9,
"Ouă fierte":155,
"Pâine integrală":223.3
},

"Gustări":{
"Smoothie Verde":54.2,
"Măr verde":52,
"Banana":89,
"Iaurt grecesc":69,
"Migdale":575,
"Nuci":654
},

"Prânz":{
"Tocană de legume":29.15,
"Mâncare de linte":188.41,
"Orez integral legume":150.4,
"Piept curcan":107,
"Somon":208,
"Supă pui":24.14
},

"Cină":{
"Salată ton":158,
"Cod la grătar":107,
"Supă cremă conopidă":86.8,
"Creveți":85,
"Zucchini":17,
"Paste integrale":340
}

}

# LOGIN
if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.title("🔐 Acces aplicație")

    parola=st.text_input("Parolă",type="password")

    if st.button("Autentificare"):

        if parola=="nutrifit2026":
            st.session_state.login=True
            st.rerun()
        else:
            st.error("Parolă incorectă")

    st.stop()


# PROFIL CLIENT

st.sidebar.header("Profil Client")

nume=st.sidebar.text_input("Nume","Maria")
greutate=st.sidebar.number_input("Greutate",40,200,70)
inaltime=st.sidebar.number_input("Înălțime",130,220,170)
varsta=st.sidebar.number_input("Vârstă",18,95,35)
sex=st.sidebar.radio("Sex",["Masculin","Feminin"])

ic_map={"Sedentar":25,"Ușor":30,"Mediu":35,"Mare":40,"Sportiv":45}

activitate=st.sidebar.selectbox("Activitate",list(ic_map.keys()))

ic=ic_map[activitate]

deficit=st.sidebar.slider("Deficit caloric",0,800,300,50)

variante=st.sidebar.slider("Variante meniu/zi",1,4,2)

# CALCULURI (FORMULELE TALE)

if varsta>=65:
    rmb_f=0.9 if sex=="Masculin" else 0.8
else:
    rmb_f=1.0 if sex=="Masculin" else 0.8

rmb=rmb_f*greutate*24

tnc=greutate*ic

target=tnc-deficit

if target<rmb:
    target=rmb
    st.sidebar.warning("Target limitat la RMB")

# MACRONUTRIENȚI

p_gr=greutate*(1.7 if ic>=35 else 1.2)
l_gr=greutate*(1.0 if ic>=35 else 0.8)

c_gr=(target-(p_gr*4)-(l_gr*9))/4


# KPI

st.title(f"Plan Nutrițional: {nume}")

c1,c2,c3,c4=st.columns(4)

c1.metric("Target kcal",round(target))
c2.metric("Proteine g",round(p_gr))
c3.metric("Lipide g",round(l_gr))
c4.metric("Carbo g",round(c_gr))


# GRAFIC MACRO

chart=pd.DataFrame({
"Macro":["Proteine","Lipide","Carbo"],
"g":[p_gr,l_gr,c_gr]
})

st.bar_chart(chart.set_index("Macro"))

st.divider()


# GENERATOR PLAN

if st.button("Generează plan 7 zile"):

    zile=["Luni","Marți","Miercuri","Joi","Vineri","Sâmbătă","Duminică"]

    dist={
    "Mic Dejun":0.25,
    "Gustare 1":0.10,
    "Prânz":0.35,
    "Gustare 2":0.10,
    "Cină":0.20
    }

    plan=[]
    istoric=set()

    for zi in zile:

        for v in range(1,variante+1):

            for masa,proc in dist.items():

                cat="Gustări" if "Gustare" in masa else masa

                alimente=list(db_alimente[cat].keys())

                alimente_posibile=[a for a in alimente if a not in istoric]

                if not alimente_posibile:
                    alimente_posibile=alimente

                aliment=random.choice(alimente_posibile)

                istoric.add(aliment)

                kcal100=db_alimente[cat][aliment]

                kcal_masa=target*proc

                gramaj=(kcal_masa/kcal100)*100

                plan.append({

                "Zi":zi,
                "Variantă":v,
                "Masă":masa,
                "Aliment":aliment,
                "Cantitate g":round(gramaj),
                "Kcal":round(kcal_masa)

                })


    df=pd.DataFrame(plan)

    for zi in zile:

        with st.expander(zi):

            df_zi=df[df["Zi"]==zi]

            for v in df_zi["Variantă"].unique():

                st.subheader(f"Variantă {v}")

                df_v=df_zi[df_zi["Variantă"]==v]

                st.table(df_v[["Masă","Aliment","Cantitate g","Kcal"]])

                st.info(f"Total kcal: {df_v['Kcal'].sum()}")


# RAPORT EXCEL

    buffer=io.BytesIO()

    with pd.ExcelWriter(buffer,engine="xlsxwriter") as writer:

        df.to_excel(writer,sheet_name="Plan Saptamanal",index=False)

        profil=pd.DataFrame({

        "Parametru":[
        "Client",
        "Greutate",
        "Inaltime",
        "Varsta",
        "Sex",
        "Activitate",
        "Target kcal"
        ],

        "Valoare":[
        nume,
        greutate,
        inaltime,
        varsta,
        sex,
        activitate,
        round(target)
        ]

        })

        profil.to_excel(writer,sheet_name="Profil",index=False)

    buffer.seek(0)

    st.download_button(
    "Descarcă raport Excel",
    buffer,
    file_name=f"plan_nutritie_{nume}.xlsx",
    mime="application/vnd.ms-excel"
    )
