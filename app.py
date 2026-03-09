import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="centered", page_icon="👩‍💻")

# --- INITIALIZARE VARIABILE DE SESIUNE ---
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False
if "ai_executat" not in st.session_state:
    st.session_state["ai_executat"] = False

# --- PASUL 0: LOGARE ---
if not st.session_state["autentificat"]:
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.subheader("🔐 Acces Securizat")
    parola = st.text_input("Introdu parola de acces:", type="password")
    
    if st.button("Verifică și Intră"):
        if parola == "nutrifit2026":
            st.session_state["autentificat"] = True
            st.rerun()
        else:
            st.error("❌ Parolă incorectă!")
    st.stop()

# --- DIN ACEST PUNCT ESTI LOGAT ---

# Meniu Logout
if st.sidebar.button("Ieșire (Logout)"):
    st.session_state["autentificat"] = False
    st.session_state["ai_executat"] = False
    st.rerun()

st.markdown("# 👩‍💻 Aplicația Mariei")

# --- PASUL 1: SELECȚIE (Vizibil doar dacă AI nu a fost executat) ---
if not st.session_state["ai_executat"]:
    st.info("👋 Bine ai venit! Urmează pașii de mai jos.")
    st.markdown("### 📝 Pasul 1: Selecție Opțiuni")
    
    optiuni_200 = [f"Serviciu NutriFit #{i}" for i in range(1, 201)]
    selectie = st.multiselect("Alege din cele 200 de configurații:", options=optiuni_200)

    if selectie:
        st.divider()
        st.markdown("### 🤖 Pasul 2: Activare Agent AI")
        st.write("Apasă butonul de mai jos pentru a genera raportul final.")
        if st.button("Procesează cu Agentul AI"):
            st.session_state["date_selectate"] = selectie
            st.session_state["ai_executat"] = True
            st.rerun()
    else:
        st.warning("Te rugăm să selectezi cel puțin o opțiune pentru a continua.")

# --- PASUL 2: REZULTAT FINAL (Vizibil DOAR după ce ai apăsat butonul AI) ---
else:
    st.success("✅ Agentul AI a finalizat procesarea!")
    
    st.subheader("📊 Previzualizare Tabel Final")
    
    # Construim tabelul exact cum ai cerut
    rows = []
    for idx, item in enumerate(st.session_state["date_selectate"]):
        pret = 150.0
        rows.append({
            "ID": idx + 1,
            "Descriere": item,
            "Cantitate": 1,
            "Pret Unitar (RON)": pret,
            "Total Fara TVA": pret,
            "TVA (19%)": pret * 0.19,
            "Total de Plata": pret * 1.19
        })
    
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.subheader("💾 Exportă Rezultatele")
    
    # Export CSV sigur
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Descarcă Raportul Excel (CSV)",
        data=csv,
        file_name="Raport_Final_Maria.csv",
        mime="text/csv"
    )

    if st.button("🔄 Începe o selecție nouă"):
        st.session_state["ai_executat"] = False
        st.rerun()
