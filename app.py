import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="centered", page_icon="👩‍💻")

# --- SISTEM DE SECURITATE ---
# Verificăm dacă utilizatorul este autentificat. Dacă nu, oprim restul codului.
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False

if not st.session_state["autentificat"]:
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.subheader("🔐 Introducere Parolă")
    
    parola = st.text_input("Introdu parola de acces pentru a continua:", type="password")
    
    if st.button("Verifică Parola"):
        if parola == "nutrifit2026":
            st.session_state["autentificat"] = True
            st.rerun() # Reîncărcăm pagina pentru a afișa conținutul
        else:
            st.error("❌ Parolă incorectă! Te rugăm să încerci din nou.")
    
    # st.stop() este ESENȚIAL: nu lasă nimic de mai jos să se încarce până la login
    st.stop()

# --- DACĂ AM AJUNS AICI, PAROLA ESTE CORECTĂ ---

# Inițializăm starea pentru Agentul AI
if "ai_procesat" not in st.session_state:
    st.session_state["ai_procesat"] = False

# Buton de logout în sidebar
if st.sidebar.button("Ieșire (Logout)"):
    st.session_state["autentificat"] = False
    st.session_state["ai_procesat"] = False
    st.rerun()

st.markdown("# 👩‍💻 Aplicația Mariei")

# LOGICA FLUXULUI: SELECȚIE -> AGENT AI -> EXPORT
if not st.session_state["ai_procesat"]:
    st.info("👋 Bine ai venit! Te rugăm să parcurgi etapele de mai jos.")
    
    st.markdown("### 📝 Pasul 1: Selecție Opțiuni")
    st.write("Alege serviciile dorite din lista de 200 de configurații disponibile:")

    # Generăm lista de 200 opțiuni
    optiuni_200 = [f"Opțiunea {i}: Configurație NutriFit" for i in range(1, 201)]
    selectie = st.multiselect("Selectează opțiunile:", options=optiuni_200)

    if selectie:
        st.divider()
        st.markdown("### 🤖 Pasul 2: Activare Agent AI")
        st.write("Acum poți procesa selecția ta cu ajutorul Agentului AI.")
        
        if st.button("Procesează datele cu Agentul AI"):
            st.session_state["selectie_finala"] = selectie
            st.session_state["ai_procesat"] = True
            st.rerun()
    else:
        st.warning("Te rugăm să selectezi cel puțin o opțiune pentru a continua.")

else:
    # --- AFIȘARE REZULTATE FINALE ---
    st.success(f"✅ Agentul AI a finalizat procesarea pentru cele {len(st.session_state['selectie_finala'])} elemente!")
    
    st.subheader("📊 Previzualizare Tabel Final")
    
    # Creăm tabelul conform datelor tale
    date_tabel = []
    for item in st.session_state["selectie_finala"]:
        pret_baza = 150.0
        date_tabel.append({
            "Descriere": item,
            "Cantitate": 1,
            "Pret Unitar (RON)": pret_baza,
            "Total Fara TVA": pret_baza,
            "TVA (19%)": pret_baza * 0.19,
            "Total de Plata": pret_baza * 1.19
        })
    
    df = pd.DataFrame(date_tabel)
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.subheader("💾 Exportă Rezultatele")
    
    nume_fisier = st.text_input("Numele fișierului:", value="Raport_Final_Maria")
    
    # Export CSV (cel mai sigur format pentru Excel fără erori de motor)
    csv = df.to_csv(index=False).encode('utf-8-sig')

    st.download_button(
        label="📥 Descarcă Raportul Excel",
        data=csv,
        file_name=f"{nume_fisier}.csv",
        mime="text/csv"
    )

    if st.button("🔄 Începe o selecție nouă"):
        st.session_state["ai_procesat"] = False
        st.rerun()
