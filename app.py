import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="centered", page_icon="👩‍💻")

# --- SISTEM DE CONTROL ---
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"

# --- ECRAN 0: LOGIN ---
if not st.session_state["autentificat"]:
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.subheader("🔐 Introducere Parolă")
    parola = st.text_input("Parola de acces:", type="password", key="pwd")
    if st.button("Autentificare", key="login_btn"):
        if parola == "nutrifit2026":
            st.session_state["autentificat"] = True
            st.session_state["pagina"] = "selectie"
            st.rerun()
        else:
            st.error("❌ Parolă incorectă!")
    st.stop()

# --- ECRAN 1: SELECȚIE ---
if st.session_state["pagina"] == "selectie":
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.info("👋 Bine ai venit! Te rugăm să parcurgi etapele de mai jos.")
    st.markdown("### 📝 Pasul 1: Selecție Opțiuni")
    
    # Generăm lista de 200 opțiuni solicitată
    optiuni = [f"Serviciu NutriFit #{i}" for i in range(1, 201)]
    alegeri = st.multiselect("Alege configurațiile:", options=optiuni, key="main_select")

    if alegeri:
        st.divider()
        st.markdown("### 🤖 Pasul 2: Agent AI")
        if st.button("🚀 Procesează datele cu AI", key="process_btn"):
            st.session_state["final_data"] = alegeri
            st.session_state["pagina"] = "raport"
            st.rerun()
    else:
        st.warning("Te rugăm să selectezi cel puțin o opțiune pentru a continua.")

# --- ECRAN 2: RAPORT FINAL ---
elif st.session_state["pagina"] == "raport":
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.success(f"✅ Agentul AI a procesat {len(st.session_state['final_data'])} elemente!")
    
    st.subheader("📊 Previzualizare Tabel Final")
    
    # Recreăm tabelul exact ca în imaginea ta originală
    tabel_list = []
    for idx, item in enumerate(st.session_state["final_data"]):
        pret = 150.0
        tabel_list.append({
            "ID": idx + 1,
            "Descriere": item,
            "Cantitate": 1,
            "Pret Unitar": pret,
            "TVA (19%)": pret * 0.19,
            "Total": pret * 1.19
        })
    
    df = pd.DataFrame(tabel_list)
    st.dataframe(df, use_container_width=True)

    st.divider()
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Descarcă Raportul", data=csv, file_name="Raport_Maria.csv", mime="text/csv")
    
    if st.button("🔄 Începe o selecție nouă"):
        st.session_state["pagina"] = "selectie"
        st.rerun()

# Logout în Sidebar
if st.sidebar.button("Logout"):
    st.session_state["autentificat"] = False
    st.session_state["pagina"] = "login"
    st.rerun()
