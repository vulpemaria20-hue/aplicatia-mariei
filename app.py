import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="centered", page_icon="👩‍💻")

# --- INITIALIZARE VARIABILE DE SESIUNE ---
# Acestea controlează ce vede utilizatorul la fiecare moment
if "etapa" not in st.session_state:
    st.session_state["etapa"] = "login"

# --- FUNCȚIE REPORNIRE ---
def resetare_sesiune():
    st.session_state["etapa"] = "login"
    st.rerun()

# --- LOGICA DE AFIȘARE PE ETAPE ---

# ETAPA 1: LOGIN
if st.session_state["etapa"] == "login":
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.subheader("🔐 Introducere Parolă")
    
    parola = st.text_input("Introdu parola de acces:", type="password")
    
    if st.button("Accesează Aplicația"):
        if parola == "nutrifit2026":
            st.session_state["etapa"] = "selectie"
            st.rerun()
        else:
            st.error("❌ Parolă incorectă!")

# ETAPA 2: SELECȚIE OPȚIUNI (Clientul alege din 200 de variante)
elif st.session_state["etapa"] == "selectie":
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.info("👋 Bine ai venit! Te rugăm să parcurgi etapele de mai jos.")
    
    st.markdown("### 📝 Pasul 1: Selecție Opțiuni")
    st.write("Alege serviciile dorite din lista de 200 de configurații disponibile:")

    # Lista celor 200 de opțiuni
    optiuni = [f"Opțiunea {i}: Configurație NutriFit Premium" for i in range(1, 201)]
    selectie_utilizator = st.multiselect("Selectează opțiunile:", options=optiuni)

    if selectie_utilizator:
        st.session_state["selectie_finala"] = selectie_utilizator
        if st.button("Confirmă Selecția și Treci la Agentul AI"):
            st.session_state["etapa"] = "agent_ai"
            st.rerun()
    else:
        st.warning("Te rugăm să selectezi cel puțin o opțiune pentru a continua.")

# ETAPA 3: ACTIVARE AGENT AI
elif st.session_state["etapa"] == "agent_ai":
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.subheader("🤖 Pasul 2: Activare Agent AI")
    st.write(f"Ai selectat {len(st.session_state['selectie_finala'])} elemente.")
    
    if st.button("🚀 Procesează datele cu Agentul AI"):
        with st.spinner('Agentul AI calculează datele...'):
            # Aici poți adăuga logică AI reală sau procesare
            st.session_state["etapa"] = "export"
            st.rerun()

# ETAPA 4: TABEL FINAL ȘI EXPORT EXCEL
elif st.session_state["etapa"] == "export":
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.success("✅ Agentul AI a finalizat procesarea!")
    
    st.subheader("📋 Previzualizare Tabel Final")
    
    # Construim tabelul pe baza selecției
    date_raport = []
    for item in st.session_state["selectie_finala"]:
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
        resetare_sesiune()

# Meniu de Ieșire în lateral (disponibil oricând după login)
if st.session_state["etapa"] != "login":
    if st.sidebar.button("Logout"):
        resetare_sesiune()
