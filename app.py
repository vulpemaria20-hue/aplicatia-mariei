import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="centered", page_icon="👩‍💻")

# --- CONTROLUL ACCESULUI (STRICT) ---
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False

# FUNCȚIE DE LOGIN
def ecran_logare():
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.subheader("🔐 Introducere Parolă")
    parola_introdusa = st.text_input("Introdu parola de acces:", type="password")
    
    if st.button("Verifică și Intră"):
        if parola_introdusa == "nutrifit2026":
            st.session_state["autentificat"] = True
            st.rerun()
        else:
            st.error("❌ Parolă incorectă!")

# DACĂ NU ESTE LOGAT, AFIȘĂM DOAR LOGIN ȘI OPRIM TOTUL AICI
if not st.session_state["autentificat"]:
    ecran_logare()
    st.stop()  # <--- Această comandă blochează orice execuție ulterioară

# --- DACĂ AM AJUNS AICI, UTILIZATORUL ESTE AUTENTIFICAT ---

# Gestionare etape după logare
if "etapa_procesare" not in st.session_state:
    st.session_state["etapa_procesare"] = "selectie"

# Buton Logout în meniul lateral
if st.sidebar.button("Ieșire (Logout)"):
    st.session_state["autentificat"] = False
    st.session_state["etapa_procesare"] = "selectie"
    st.rerun()

st.markdown("# 👩‍💻 Aplicația Mariei")

# ETAPA DE SELECȚIE (Pasul 1)
if st.session_state["etapa_procesare"] == "selectie":
    st.info("👋 Bine ai venit! Te rugăm să parcurgi etapele de mai jos.")
    st.markdown("### 📝 Pasul 1: Selecție Opțiuni")
    st.write("Alege serviciile dorite din lista de 200 de configurații:")

    # Lista celor 200 de opțiuni
    optiuni_200 = [f"Serviciu NutriFit #{i}: Configurație Premium" for i in range(1, 201)]
    selectie = st.multiselect("Selectează opțiunile:", options=optiuni_200)

    if selectie:
        st.divider()
        st.markdown("### 🤖 Pasul 2: Activare Agent AI")
        if st.button("Procesează selecția cu Agentul AI"):
            st.session_state["rezultate_finale"] = selectie
            st.session_state["etapa_procesare"] = "tabel"
            st.rerun()
    else:
        st.warning("Te rugăm să selectezi cel puțin o opțiune pentru a continua.")

# ETAPA DE TABEL ȘI EXPORT (Pasul 2)
elif st.session_state["etapa_procesare"] == "tabel":
    st.success("✅ Agentul AI a finalizat procesarea!")
    
    st.subheader("📊 Previzualizare Tabel Final")
    
    # Construim tabelul exact ca în imaginea ta
    date_tabel = []
    for idx, item in enumerate(st.session_state["rezultate_finale"]):
        pret = 150.0 # Valoare exemplu
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
    
    # ZONA DE EXPORT
    st.subheader("💾 Exportă Rezultatele")
    nume_fisier = st.text_input("Nume fișier export:", value="Raport_Final_Maria")
    
    # Export CSV sigur (pentru a evita erori de librării Excel pe server)
    csv = df.to_csv(index=False).encode('utf-8-sig')

    st.download_button(
        label="📥 Descarcă Raportul pentru Excel",
        data=csv,
        file_name=f"{nume_fisier}.csv",
        mime="text/csv"
    )

    if st.button("🔄 Începe o selecție nouă"):
        st.session_state["etapa_procesare"] = "selectie"
        st.rerun()
