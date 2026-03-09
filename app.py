import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="centered", page_icon="👩‍💻")

# --- GESTIONARE SESIUNE ---
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False
if "ai_gata" not in st.session_state:
    st.session_state["ai_gata"] = False

# --- BLOCARE ACCES (LOGIN) ---
if not st.session_state["autentificat"]:
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.subheader("🔐 Introducere Parolă")
    parola = st.text_input("Parola de acces:", type="password")
    if st.button("Verifică"):
        if parola == "nutrifit2026":
            st.session_state["autentificat"] = True
            st.rerun()
        else:
            st.error("Parolă incorectă!")
    st.stop() # Nu lasă restul codului să ruleze

# --- DACĂ EȘTI AICI, EȘTI LOGAT ---

# Buton Logout în lateral
if st.sidebar.button("Ieșire (Logout)"):
    st.session_state["autentificat"] = False
    st.session_state["ai_gata"] = False
    st.rerun()

st.markdown("# 👩‍💻 Aplicația Mariei")

# LOGICA PE ETAPE
if not st.session_state["ai_gata"]:
    # PASUL 1: SELECȚIE
    st.info("👋 Bine ai venit! Te rugăm să parcurgi etapele de mai jos.")
    st.markdown("### 📝 Pasul 1: Selecție Opțiuni")
    st.write("Alege serviciile dorite din lista de 200 de configurații:")

    optiuni_200 = [f"Serviciu NutriFit #{i}" for i in range(1, 201)]
    selectie = st.multiselect("Selectează opțiunile:", options=optiuni_200)

    if selectie:
        st.divider()
        st.markdown("### 🤖 Pasul 2: Activare Agent AI")
        if st.button("Procesează selecția cu Agentul AI"):
            st.session_state["rezultate"] = selectie
            st.session_state["ai_gata"] = True
            st.rerun()
    else:
        st.warning("Te rugăm să selectezi cel puțin o opțiune pentru a continua.")

else:
    # PASUL FINAL: RAPORTUL DIN PRIMA IMAGINE
    st.success("✅ Agentul AI a finalizat procesarea!")
    
    st.subheader("📊 Previzualizare Tabel")
    
    # Construim tabelul exact ca în imaginea ta
    rows = []
    for idx, item in enumerate(st.session_state["rezultate"]):
        pret = 150.0  # Exemplu
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
    
    # EXPORTUL
    st.subheader("💾 Exportă Rezultatele")
    nume_fisier = st.text_input("Numele fișierului:", value="Raport_Maria")
    
    # Export CSV sigur (fără biblioteci care crapă)
    csv = df.to_csv(index=False).encode('utf-8-sig')

    st.download_button(
        label="📥 Descarcă Raportul Excel",
        data=csv,
        file_name=f"{nume_fisier}.csv",
        mime="text/csv"
    )

    if st.button("🔄 Începe o selecție nouă"):
        st.session_state["ai_gata"] = False
        st.rerun()
