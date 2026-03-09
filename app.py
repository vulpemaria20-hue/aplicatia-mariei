import streamlit as st
import pandas as pd

# Configurare pagină
st.set_page_config(
    page_title="Aplicația Mariei",
    layout="centered",
    page_icon="👩‍💻"
)

# --- SESSION STATE ---
if "autentificat" not in st.session_state:
    st.session_state.autentificat = False

if "pas_meniu" not in st.session_state:
    st.session_state.pas_meniu = "selectie"

# --- PASUL 0: LOGIN ---
if not st.session_state.autentificat:

    st.title("👩‍💻 Aplicația Mariei")

    parola = st.text_input(
        "Introdu parola de acces:",
        type="password"
    )

    if st.button("Conectare"):

        if parola == "nutrifit2026":
            st.session_state.autentificat = True
            st.rerun()

        else:
            st.error("❌ Parolă incorectă!")

    st.stop()


# --- SIDEBAR ---
st.sidebar.title("Cont")

if st.sidebar.button("Logout"):
    st.session_state.autentificat = False
    st.session_state.pas_meniu = "selectie"
    st.rerun()


# --- PASUL 1: SELECTIE ---
if st.session_state.pas_meniu == "selectie":

    st.title("👩‍💻 Aplicația Mariei")

    st.info("👋 Bine ai venit! Te rugăm să parcurgi etapele de mai jos.")

    st.subheader("Pasul 1: Selecție Opțiuni")

    # 200 alimente
    optiuni_200 = [f"Aliment / Preparat #{i}" for i in range(1, 201)]

    alegeri = st.multiselect(
        "Alege din cele 200 de configurații:",
        options=optiuni_200
    )

    if alegeri:
        st.success(f"Ai selectat {len(alegeri)} alimente")

        st.divider()

        st.subheader("Pasul 2: Agent AI")

        if st.button("🤖 Generează Planul pe 7 Zile"):

            st.session_state.selectie_finala = alegeri
            st.session_state.pas_meniu = "raport"
            st.rerun()

    else:
        st.warning("Selectează cel puțin un aliment pentru a continua.")


# --- PASUL 2: RAPORT ---
elif st.session_state.pas_meniu == "raport":

    st.title("👩‍💻 Aplicația Mariei")

    st.success("✅ Agentul AI a generat meniul tău săptămânal!")

    zile = [
        "Luni",
        "Marți",
        "Miercuri",
        "Joi",
        "Vineri",
        "Sâmbătă",
        "Duminică"
    ]

    selectie = st.session_state.selectie_finala

    plan_final = []

    for i, zi in enumerate(zile):

        articol = selectie[i % len(selectie)]

        plan_final.append({
            "Ziua": zi,
            "Aliment Recomandat": articol,
            "Observații": "Consum conform planului"
        })

    df = pd.DataFrame(plan_final)

    st.table(df)

    st.divider()

    # Export CSV
    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "📥 Descarcă meniul (CSV)",
        data=csv,
        file_name="meniu_7_zile.csv",
        mime="text/csv"
    )

    if st.button("🔄 Creează un meniu nou"):

        st.session_state.pas_meniu = "selectie"
        st.session_state.selectie_finala = []
        st.rerun()
