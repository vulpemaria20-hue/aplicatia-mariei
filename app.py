import streamlit as st
import pandas as pd

# 1. Configurare Pagină (Singurul lucru care poate sta înainte de login)
st.set_page_config(page_title="Aplicația Mariei", layout="centered", page_icon="👩‍💻")

# --- SISTEMUL DE SECURITATE (BLOCARE TOTALĂ) ---
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False

if not st.session_state["autentificat"]:
    # Ecranul de Login apare SINGUR
    st.markdown("# 🔐 Acces Restricționat")
    parola = st.text_input("Introdu parola pentru a deschide Aplicația Mariei:", type="password")
    
    if st.button("Verifică Parola"):
        if parola == "nutrifit2026":
            st.session_state["autentificat"] = True
            st.rerun()
        else:
            st.error("❌ Parolă incorectă!")
    st.stop() # Oprește execuția restului de cod până la autentificare

# --- DIN ACEST PUNCT CODUL RULEAZĂ DOAR DACĂ EȘTI AUTENTIFICAT ---

# Inițializăm starea procesului AI
if "etapa_ai" not in st.session_state:
    st.session_state["etapa_ai"] = False

# Meniu lateral pentru Logout
if st.sidebar.button("Ieșire (Logout)"):
    st.session_state["autentificat"] = False
    st.session_state["etapa_ai"] = False
    st.rerun()

# TITLUL APLICAȚIEI
st.markdown("# 👩‍💻 Aplicația Mariei")

# LOGICA PE ETAPE (Pasul 1 -> Pasul 2 -> Export)
if not st.session_state["etapa_ai"]:
    st.info("👋 Bine ai venit! Te rugăm să parcurgi etapele de mai jos.")
    
    st.markdown("### 📝 Pasul 1: Selecție Opțiuni")
    st.write("Alege serviciile dorite din lista de 200 de configurații disponibile:")

    # Generăm lista de 200 opțiuni
    optiuni_200 = [f"Opțiunea {i}: Configurație NutriFit" for i in range(1, 201)]
    selectie = st.multiselect("Selectează opțiunile:", options=optiuni_200)

    if selectie:
        st.divider()
        st.markdown("### 🤖 Pasul 2: Activare Agent AI")
        if st.button("Procesează datele cu Agentul AI"):
            st.session_state["date_selectate"] = selectie
            st.session_state["etapa_ai"] = True
            st.rerun()
    else:
        st.warning("Te rugăm să selectezi cel puțin o opțiune pentru a continua.")

else:
    # ECRANUL FINAL DUPĂ PROCESAREA AI
    st.success(f"✅ Agentul AI a finalizat procesarea pentru cele {len(st.session_state['date_selectate'])} elemente!")
    
    st.subheader("📋 Previzualizare Tabel Final")
    
    # Construim tabelul
    date_tabel = []
    for item in st.session_state["date_selectate"]:
        pret = 150.0
        date_tabel.append({
            "Denumire": item,
            "Cantitate": 1,
            "Pret (RON)": pret,
            "TVA (19%)": pret * 0.19,
            "Total": pret * 1.19
        })
    
    df = pd.DataFrame(date_tabel)
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.subheader("💾 Pasul Final: Export")
    nume_fisier = st.text_input("Nume fișier export:", value="Raport_Final_Maria")
    
    # Export CSV (universal pentru Excel)
    csv = df.to_csv(index=False).encode('utf-8-sig')

    st.download_button(
        label="📥 Descarcă Raportul Excel",
        data=csv,
        file_name=f"{nume_fisier}.csv",
        mime="text/csv"
    )

    if st.button("🔄 Începe o sesiune nouă"):
        st.session_state["etapa_ai"] = False
        st.rerun()
