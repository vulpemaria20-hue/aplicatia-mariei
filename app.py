import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="centered", page_icon="👩‍💻")

# --- INITIALIZARE VARIABILE DE SESIUNE ---
# Acestea controlează ce etapă vede utilizatorul
if "etapa" not in st.session_state:
    st.session_state["etapa"] = "login"

# --- ETAPA 1: LOGARE ---
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
    st.stop() # Oprește execuția aici până la logare

# --- ETAPA 2: SELECȚIE OPȚIUNI (Imaginea 3 din mesajul tău) ---
if st.session_state["etapa"] == "selectie":
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.info("👋 Bine ai venit! Te rugăm să parcurgi etapele de mai jos.")
    
    st.markdown("### 📝 Pasul 1: Selecție Opțiuni")
    st.write("Alege serviciile dorite din lista de 200 de configurații:")

    # Generăm lista celor 200 de opțiuni
    optiuni = [f"Opțiunea {i}: Plan NutriFit #{i}" for i in range(1, 201)]
    selectie = st.multiselect("Selectează opțiunile:", options=optiuni)

    if selectie:
        st.session_state["selectie_utilizator"] = selectie
        st.divider()
        st.markdown("### 🤖 Pasul 2: Activare Agent AI")
        if st.button("Procesează selecția cu Agentul AI"):
            st.session_state["etapa"] = "tabel_final"
            st.rerun()
    else:
        st.warning("Te rugăm să selectezi cel puțin o opțiune pentru a continua.")

# --- ETAPA 3: TABEL ȘI EXPORT (Imaginea 1 din mesajul tău) ---
elif st.session_state["etapa"] == "tabel_final":
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.success("✅ Agentul AI a finalizat procesarea!")
    
    st.subheader("📊 Previzualizare Tabel Final")
    
    # Construim tabelul pe baza selecției utilizatorului
    date_tabel = []
    for idx, item in enumerate(st.session_state["selectie_utilizator"]):
        pret = 150.0
        date_tabel.append({
            "ID": idx + 1,
            "Descriere": item,
            "Cantitate": 1,
            "Pret Unitar (RON)": pret,
            "Total Fara TVA": pret,
            "TVA (19%)": pret * 0.19,
            "Total de Plata": pret * 1.19
        })
    
    df = pd.DataFrame(date_tabel)
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.subheader("💾 Exportă Rezultatele")
    
    nume_fisier = st.text_input("Nume fișier export:", value="Raport_Final_Maria")
    csv = df.to_csv(index=False).encode('utf-8-sig')

    st.download_button(
        label="📥 Descarcă Raportul Excel",
        data=csv,
        file_name=f"{nume_fisier}.csv",
        mime="text/csv"
    )

    if st.button("🔄 Începe o selecție nouă"):
        st.session_state["etapa"] = "selectie"
        st.rerun()

# Buton de Logout în Sidebar
if st.sidebar.button("Logout"):
    st.session_state["etapa"] = "login"
    st.rerun()
