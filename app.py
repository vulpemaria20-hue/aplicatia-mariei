import streamlit as st
import pandas as pd
import random
import io

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


# BAZA DE DATE ALIMENTE
db_alimente = {

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

# COMBINAȚII LOGICE PENTRU MÂNCARE
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

# SIDEBAR PROFIL CLIENT
st.sidebar.header("👤 Profil Client")

nume = st.sidebar.text_input("Nume Client","Maria")

greutate = st.sidebar.number_input("Greutate (kg)",40,200,70)

inaltime = st.sidebar.number_input("Înălțime (cm)",130,220,170)

varsta = st.sidebar.number_input("Vârstă",18,95,35)

sex = st.sidebar.radio("Sex",["Masculin","Feminin"])

# INDICE ACTIVITATE
ic_map={
"Sedentar":25,
"Ușor":30,
"Mediu":35,
"Mare":40,
"Sportiv":45
}

activitate=st.sidebar.selectbox("Activitate (IC)",list(ic_map.keys()))
ic=ic_map[activitate]

# DEFICIT
deficit = st.sidebar.slider("Deficit caloric",0,800,300,50)

# VARIANTE MENIU
variante = st.sidebar.slider("Variante meniu / zi",1,4,2)

# CALCULURI METABOLICE
if varsta >= 65:
    rmb_f = 0.9 if sex == "Masculin" else 0.8
else:
    rmb_f = 1.0 if sex == "Masculin" else 0.8

rmb = rmb_f * greutate * 24
tnc_mentinere = greutate * ic
target = tnc_mentinere - deficit

# PROTECTIE METABOLICA
if target < rmb:
    target = rmb
    st.sidebar.warning(f"⚠️ Target limitat la RMB ({rmb:.0f} kcal)")

# MACRONUTRIENTI
p_gr = greutate * (1.7 if ic >= 35 else 1.2)
l_gr = greutate * (1.0 if ic >= 35 else 0.8)
c_gr = (target - (p_gr * 4) - (l_gr * 9)) / 4

# TITLU
st.title(f"⚖️ Plan Nutrițional Matematic: {nume}")

# KPI
col1,col2,col3,col4 = st.columns(4)
col1.metric("Țintă calorică",f"{target:.0f} kcal")
col2.metric("Proteine",f"{p_gr:.0f} g")
col3.metric("Lipide",f"{l_gr:.0f} g")
col4.metric("Carbohidrați",f"{c_gr:.0f} g")

st.divider()

# GRAFIC MACRO
chart = pd.DataFrame({
"Macro":["Proteine","Lipide","Carbohidrați"],
"Grame":[p_gr,l_gr,c_gr]
})
st.bar_chart(chart.set_index("Macro"))

st.divider()

# GENERATOR PLAN
if st.button("🤖 Generează plan alimentar 7 zile"):

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
                combinatii = db_combinatii[cat]
                alegere = random.choice(combinatii)

                kcal_masa = target*proc
                total_kcal_comb = sum(alegere.values())
                factor = kcal_masa / total_kcal_comb

                for aliment, kcal_100 in alegere.items():
                    gramaj = (kcal_100 * factor) / (kcal_100/100)
                    plan.append({
                        "Zi": zi,
                        "Variantă": v,
                        "Masă": masa,
                        "Aliment": aliment,
                        "Cantitate g": round(gramaj),
                        "Kcal": round(kcal_100*factor)
                    })

    df=pd.DataFrame(plan)

    # AFISARE MENIU
    for zi in zile:
        with st.expander(f"📅 {zi}"):
            df_zi=df[df["Zi"]==zi]
            for v in df_zi["Variantă"].unique():
                st.subheader(f"Variantă {v}")
                df_v=df_zi[df_zi["Variantă"]==v]
                st.table(df_v[["Masă","Aliment","Cantitate g","Kcal"]])
                st.info(f"Total calorii: {df_v['Kcal'].sum()} kcal")

    # GENERARE RAPORT EXCEL
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Plan Saptamanal", index=False)
        profil = pd.DataFrame({
        "Parametru":["Client","Greutate","Inaltime","Varsta","Sex","Activitate","Target kcal"],
        "Valoare":[nume,greutate,inaltime,varsta,sex,activitate,round(target)]
        })
        profil.to_excel(writer, sheet_name="Profil Client", index=False)
    buffer.seek(0)

    st.download_button(
    label="📥 Descarcă raport nutrițional Excel",
    data=buffer,
    file_name=f"plan_nutritie_{nume}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("Apasă pe buton pentru a genera planul alimentar.")  
