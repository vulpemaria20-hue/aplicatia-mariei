import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="centered", page_icon="👩‍💻")

# --- LOGICA DE SESIUNE (PENTRU FLUX) ---
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False
if "procesat" not in st.session_state:
    st.session_state["procesat"] = False

# --- 1. ECRAN LOGIN ---
if not st.session_state["autentificat"]:
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.subheader("🔐 Autentificare Necesară")
    parola = st.text_input("Introdu parola de acces:", type="password")
    
    if st.button("Conectare"):
        if parola == "nutrifit2026":
            st.session_state["autentificat"] = True
            st.rerun()
        else:
            st.error("❌ Parolă incorectă!")

# --- 2. ECRAN INTRODUCERE ȘI SELECȚIE ---
elif st.session_state["autentificat"] and not st.session_state["procesat"]:
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.info("👋 Bine ai venit! Te rugăm să parcurgi etapele de mai jos.")
    
    st.markdown("### 📝 Pasul 1: Selecție Opțiuni")
    st.write("Alege serviciile dorite din lista de 200 de configurații disponibile:")

    # Lista celor 200 de opțiuni
    optiuni = [f"Opțiunea {i}: Configurație NutriFit Premium" for i in range(1, 201)]
    selectie_utilizator = st.multiselect("Selectează opțiunile:", options=optiuni)

    if selectie_utilizator:
        st.divider()
        st.markdown("### 🤖 Pasul 2: Activare Agent AI")
        st.write("Acum poți trimite selecția către Agentul AI pentru procesare.")
        
        if st.button("Procesează datele cu Agentul AI"):
            st.session_state["selectie"] = selectie_utilizator
            st.session_state["procesat"] = True
            st.rerun()
    else:
        st.warning("Te rugăm să selectezi cel puțin o opțiune pentru a continua.")

# --- 3. ECRAN FINAL (RAPORT ȘI EXPORT) ---
else:
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.success(f"✅ Agentul AI a finalizat procesarea celor {len(st.session_state['selectie'])} elemente!")
    
    st.subheader("📋 Previzualizare Tabel Final")
    
    # Construim tabelul pe baza selecției
    date_raport = []
    for item in st.session_state["selectie"]:
        pret = 150.0
        date_raport.append({
            "Denumire": item,
            "Cantitate": 1,
            "Pret (RON)": pret,
            "TVA (19%)": pret * 0.19,
            "Total": pret * 1.19
        })
    
    df = pd.DataFrame(date_raport)
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.subheader("💾 Pasul Final: Export")
    nume_f = st.text_input("Nume fișier:", value="Raport_Final_Maria")
    
    # Export CSV (cel mai sigur pentru Excel)
    csv_data = df.to_csv(index=False).encode('utf-8-sig')

    st.download_button(
        label="📥 Descarcă Raportul pentru Excel",
        data=csv_data,
        file_name=f"{nume_f}.csv",
        mime="text/csv"
    )

    if st.button("🔄 Începe o sesiune nouă"):
        st.session_state["procesat"] = False
        st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state["autentificat"] = False
        st.session_state["procesat"] = False
        st.rerun()
