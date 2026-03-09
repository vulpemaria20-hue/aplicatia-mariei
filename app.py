import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="centered", page_icon="👩‍💻")

# --- INITIALIZARE VARIABILE DE SESIUNE ---
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False
if "etapa" not in st.session_state:
    st.session_state["etapa"] = "selectie"

# --- LOGICA DE LOGIN (BLOCARE TOTALĂ) ---
if not st.session_state["autentificat"]:
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.subheader("🔐 Introducere Parolă")
    
    parola = st.text_input("Introdu parola de acces:", type="password")
    
    if st.button("Accesează Aplicația"):
        if parola == "nutrifit2026":
            st.session_state["autentificat"] = True
            st.rerun()
        else:
            st.error("❌ Parolă incorectă!")
    
    # ACESTA ESTE SECRETUL: st.stop() nu lasă codul de mai jos să se execute DELOC
    st.stop()

# --- DIN ACEST PUNCT CODUL SE EXECUTĂ DOAR DUPĂ LOGIN ---

# Meniu de Ieșire
if st.sidebar.button("Ieșire (Logout)"):
    st.session_state["autentificat"] = False
    st.session_state["etapa"] = "selectie"
    st.rerun()

st.markdown("# 👩‍💻 Aplicația Mariei")

# ETAPA 1: SELECȚIE (Pasul de introducere)
if st.session_state["etapa"] == "selectie":
    st.info("👋 Bine ai venit! Te rugăm să parcurgi etapele de mai jos.")
    
    st.markdown("### 📝 Pasul 1: Selecție Opțiuni")
    st.write("Alege serviciile dorite din lista de 200 de configurații:")

    # Lista celor 200 de opțiuni
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

# ETAPA 2: TABEL ȘI EXPORT (Apare doar după ce apeși butonul AI)
elif st.session_state["etapa"] == "tabel_final":
    st.success(f"✅ Agentul AI a finalizat procesarea celor {len(st.session_state['selectie_utilizator'])} elemente!")
    
    st.subheader("📊 Previzualizare Tabel Final")
    
    # Generăm tabelul exact ca în imaginea ta
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
