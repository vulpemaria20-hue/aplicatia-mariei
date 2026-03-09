import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="NutriFit Maria", layout="centered", page_icon="🥗")

# --- INITIALIZARE ---
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False
if "pas" not in st.session_state:
    st.session_state["pas"] = "selectie"

# --- LOGARE ---
if not st.session_state["autentificat"]:
    st.title("🥗 NutriFit Maria")
    parola = st.text_input("Parola:", type="password")
    if st.button("Intră"):
        if parola == "nutrifit2026":
            st.session_state["autentificat"] = True
            st.rerun()
    st.stop()

# --- INTERFAȚA ---
st.title("👩‍💻 Aplicația Mariei")

if st.session_state["pas"] == "selectie":
    st.subheader("Pasul 1: Selectează alimentele (200 opțiuni)")
    
    # Lista de 200 de variante
    optiuni = [f"Aliment NutriFit #{i}" for i in range(1, 201)]
    alegeri = st.multiselect("Alege produsele:", options=optiuni)

    if alegeri:
        st.divider()
        if st.button("🤖 Agent AI: Generează Meniul"):
            st.session_state["alimente_alese"] = alegeri
            st.session_state["pas"] = "final"
            st.rerun()
    else:
        st.info("Selectează minim un aliment.")

elif st.session_state["pas"] == "final":
    st.success("✅ Meniul pe 7 zile a fost generat!")
    
    zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
    data = []
    for i, zi in enumerate(zile):
        # Repartizăm alimentele pe zile
        aliment = st.session_state["alimente_alese"][i % len(st.session_state["alimente_alese"])]
        data.append({"Ziua": zi, "Meniu Recomandat": aliment})
    
    df = pd.DataFrame(data)
    st.table(df) # Afișare curată, fără prețuri

    if st.button("🔄 Crează alt meniu"):
        st.session_state["pas"] = "selectie"
        st.rerun()

if st.sidebar.button("Logout"):
    st.session_state["autentificat"] = False
    st.rerun()
