import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="centered", page_icon="👩‍💻")

# --- INITIALIZARE STARE ---
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False
if "etapa" not in st.session_state:
    st.session_state["etapa"] = "login"
if "selectie" not in st.session_state:
    st.session_state["selectie"] = []

# --- FUNCTIE RESETARE ---
def logout():
    st.session_state["autentificat"] = False
    st.session_state["etapa"] = "login"
    st.rerun()

# --- LOGICA DE AFISARE ---
placeholder = st.empty()

with placeholder.container():
    # PASUL 0: LOGIN
    if st.session_state["etapa"] == "login":
        st.markdown("# 👩‍💻 Aplicația Mariei")
        st.subheader("🔐 Introducere Parolă")
        parola = st.text_input("Parola de acces:", type="password")
        if st.button("Autentificare"):
            if parola == "nutrifit2026":
                st.session_state["autentificat"] = True
                st.session_state["etapa"] = "selectie"
                st.rerun()
            else:
                st.error("Parolă incorectă!")

    # PASUL 1: SELECȚIE (Imaginea ta cu 'Pasul 1')
    elif st.session_state["etapa"] == "selectie":
        st.markdown("# 👩‍💻 Aplicația Mariei")
        st.info("👋 Bine ai venit! Te rugăm să parcurgi etapele de mai jos.")
        st.markdown("### 📝 Pasul 1: Selecție Opțiuni")
        
        # Lista de 200 opțiuni
        optiuni_200 = [f"Serviciu NutriFit #{i}" for i in range(1, 201)]
        st.session_state["selectie"] = st.multiselect("Alege configurațiile:", options=optiuni_200)

        if st.session_state["selectie"]:
            st.divider()
            st.markdown("### 🤖 Pasul 2: Agent AI")
            if st.button("🚀 Procesează datele cu AI"):
                st.session_state["etapa"] = "raport"
                st.rerun()
        else:
            st.warning("Te rugăm să selectezi cel puțin o opțiune.")

    # PASUL 2: RAPORT FINAL (Imaginea ta cu tabelul)
    elif st.session_state["etapa"] == "raport":
        st.markdown("# 👩‍💻 Aplicația Mariei")
        st.success(f"✅ Agentul AI a procesat {len(st.session_state['selectie'])} elemente!")
        
        st.subheader("📊 Previzualizare Tabel Final")
        
        date = []
        for idx, item in enumerate(st.session_state["selectie"]):
            pret = 150.0
            date.append({
                "ID": idx + 1,
                "Descriere": item,
                "Cantitate": 1,
                "Pret Unitar": pret,
                "TVA (19%)": pret * 0.19,
                "Total": pret * 1.19
            })
        
        df = pd.DataFrame(date)
        st.dataframe(df, use_container_width=True)

        st.divider()
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Descarcă Raportul", data=csv, file_name="Raport_Maria.csv", mime="text/csv")
        
        if st.button("🔄 Start Nou"):
            st.session_state["etapa"] = "selectie"
            st.rerun()

# Sidebar Logout
if st.session_state["autentificat"]:
    st.sidebar.button("Logout", on_click=logout)
