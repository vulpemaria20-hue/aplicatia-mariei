import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="centered", page_icon="👩‍💻")

# --- INITIALIZARE STRICTA ---
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False
if "pas_curent" not in st.session_state:
    st.session_state["pas_curent"] = "login"

# --- LOGICA DE LOGARE (ECRAN IZOLAT) ---
if not st.session_state["autentificat"]:
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.subheader("🔐 Introducere Parolă")
    
    parola_introdusa = st.text_input("Introdu parola de acces:", type="password", key="login_pass")
    
    if st.button("Verifică Parola", key="btn_login"):
        if parola_introdusa == "nutrifit2026":
            st.session_state["autentificat"] = True
            st.session_state["pas_curent"] = "selectie"
            st.rerun()
        else:
            st.error("❌ Parolă incorectă!")
    st.stop() # GARANTEAZA că nimic de mai jos nu apare pe ecran

# --- DACĂ EȘTI AICI, EȘTI AUTENTIFICAT ---

# Meniu de Logout în Sidebar
if st.sidebar.button("Ieșire (Logout)"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

# --- PASUL 1: SELECȚIE (ECRAN IZOLAT) ---
if st.session_state["pas_curent"] == "selectie":
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.info("👋 Bine ai venit! Te rugăm să parcurgi etapele de mai jos.")
    st.markdown("### 📝 Pasul 1: Selecție Opțiuni")
    
    optiuni_200 = [f"Serviciu NutriFit #{i}" for i in range(1, 201)]
    selectie = st.multiselect("Alege serviciile dorite:", options=optiuni_200, key="multi_select")

    if selectie:
        st.session_state["date_alese"] = selectie
        st.divider()
        st.markdown("### 🤖 Pasul 2: Activare Agent AI")
        if st.button("Procesează cu Agentul AI", key="btn_ai"):
            st.session_state["pas_curent"] = "tabel"
            st.rerun()
    else:
        st.warning("Te rugăm să selectezi cel puțin o opțiune.")

# --- PASUL 2: TABEL ȘI EXPORT (ECRAN IZOLAT) ---
elif st.session_state["pas_curent"] == "tabel":
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.success(f"✅ Agentul AI a finalizat procesarea pentru {len(st.session_state['date_alese'])} elemente!")
    
    st.subheader("📊 Previzualizare Tabel Final")
    
    # Construim tabelul cerut în imaginea ta
    date_tabel = []
    for idx, item in enumerate(st.session_state["date_alese"]):
        p = 150.0
        date_tabel.append({
            "ID": idx + 1,
            "Descriere": item,
            "Cantitate": 1,
            "Pret Unitar (RON)": p,
            "Total Fara TVA": p,
            "TVA (19%)": p * 0.19,
            "Total de Plata": p * 1.19
        })
    
    df = pd.DataFrame(date_tabel)
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.subheader("💾 Export")
    
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Descarcă Raportul Excel",
        data=csv,
        file_name="Raport_Maria.csv",
        mime="text/csv",
        key="btn_download"
    )

    if st.button("🔄 Începe o selecție nouă"):
        st.session_state["pas_curent"] = "selectie"
        st.rerun()
