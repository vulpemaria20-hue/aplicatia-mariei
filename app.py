import streamlit as st
import pandas as pd

# 1. Configurare Pagină (Păstrăm titlul tău original)
st.set_page_config(page_title="Aplicația Mariei", layout="centered", page_icon="👩‍💻")

# --- CONTROLUL ETAPELOR ---
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False
if "pas_meniu" not in st.session_state:
    st.session_state["pas_meniu"] = "selectie"

# --- PASUL 0: LOGARE ---
if not st.session_state["autentificat"]:
    st.title("👩‍💻 Aplicația Mariei")
    parola = st.text_input("Introdu parola de acces:", type="password")
    if st.button("Conectare"):
        if parola == "nutrifit2026":
            st.session_state["autentificat"] = True
            st.rerun()
        else:
            st.error("Parolă incorectă!")
    st.stop()

# --- PASUL 1: SELECȚIE ALIMENTE ---
if st.session_state["pas_meniu"] == "selectie":
    st.title("👩‍💻 Aplicația Mariei")
    st.info("👋 Bine ai venit! Te rugăm să parcurgi etapele de mai jos.")
    st.subheader("Pasul 1: Selecție Opțiuni")
    
    # Generăm lista de 200 de opțiuni de alimente
    optiuni_200 = [f"Aliment/Preparat #{i}" for i in range(1, 201)]
    alegeri = st.multiselect("Alege din cele 200 de configurații:", options=optiuni_200)

    if alegeri:
        st.divider()
        st.subheader("Pasul 2: Agent AI")
        if st.button("🤖 Generează Planul pe 7 Zile"):
            st.session_state["selectie_finala"] = alegeri
            st.session_state["pas_meniu"] = "raport"
            st.rerun()
    else:
        st.warning("Te rugăm să selectezi cel puțin o opțiune pentru a continua.")

# --- PASUL 2: AFIȘARE MENIU 7 ZILE ---
elif st.session_state["pas_meniu"] == "raport":
    st.title("👩‍💻 Aplicația Mariei")
    st.success("✅ Agentul AI a generat meniul tău săptămânal!")

    zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
    selectie = st.session_state["selectie_finala"]
    
    plan_final = []
    for i, zi in enumerate(zile):
        # Alocăm alimentele alese pe rând pentru fiecare zi
        articol = selectie[i % len(selectie)]
        plan_final.append({
            "Ziua": zi,
            "Aliment Recomandat": articol,
            "Observații": "Consum conform planului"
        })

    df = pd.DataFrame(plan_final)
    st.table(df) # Afișăm tabelul clar, fără prețuri sau TVA

    st.divider()
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Descarcă Meniul (Excel)", data=csv, file_name="Meniu_7_Zile.csv")
    
    if st.button("🔄 Crează un meniu nou"):
        st.session_state["pas_meniu"] = "selectie"
        st.rerun()

# Buton Logout (Sidebar)
if st.sidebar.button("Logout"):
    st.session_state["autentificat"] = False
    st.rerun()
