import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Aplicația Mariei", layout="centered", page_icon="👩‍💻")

# --- LOGICA DE AUTENTIFICARE ---
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False

def ecran_login():
    st.markdown("# 🔐 Bun venit la Aplicația Mariei")
    st.write("Introdu parola pentru a accesa Agentul AI și instrumentele de export.")
    
    parola = st.text_input("Parola de acces:", type="password")
    if st.button("Autentificare"):
        if parola == "nutrifit2026":
            st.session_state["autentificat"] = True
            st.rerun()
        else:
            st.error("❌ Parolă incorectă! Te rugăm să verifici parola.")

# --- APLICAȚIA PROPRIU-ZISĂ ---
if not st.session_state["autentificat"]:
    ecran_login()
else:
    # Header Personalizat
    st.markdown("# 👩‍💻 Aplicația Mariei")
    st.sidebar.title("Setări Profil")
    if st.sidebar.button("Ieșire (Logout)"):
        st.session_state["autentificat"] = False
        st.rerun()

    st.divider()

    # 2. AGENTUL AI ȘI CELE 200 DE OPȚIUNI
    st.subheader("🤖 Agent AI NutriFit")
    st.write("Selectează din lista de 200 de configurații pentru a genera raportul final.")

    # Generăm lista extinsă de 200 de opțiuni
    lista_optiuni = [f"Serviciu NutriFit #{i}: Analiză detaliată și plan personalizat" for i in range(1, 201)]
    
    selectie = st.multiselect(
        "Alege opțiunile dorite:",
        options=lista_optiuni,
        placeholder="Apasă aici pentru a vedea cele 200 de opțiuni..."
    )

    if st.button("Procesează selecția cu Agentul AI"):
        if not selectie:
            st.warning("⚠️ Te rugăm să selectezi cel puțin o opțiune din listă.")
        else:
            st.success(f"✅ Agentul AI a procesat cu succes {len(selectie)} elemente!")
            
            # 3. CONSTRUCȚIE TABEL DATE
            date_raport = []
            for item in selectie:
                # Simulăm niște calcule pentru fiecare opțiune
                pret_baza = 125.0
                tva = pret_baza * 0.19
                date_raport.append({
                    "Element Procesat": item,
                    "Unități": 1,
                    "Preț Unitar (RON)": pret_baza,
                    "TVA (19%)": tva,
                    "Total Final": pret_baza + tva
                })
            
            df = pd.DataFrame(date_raport)

            # Afișare tabel
            st.write("### 📋 Previzualizare Tabel Final")
            st.dataframe(df, use_container_width=True)

            # 4. EXPORT
            st.divider()
            st.subheader("💾 Finalizare și Export")
            
            nume_fis = st.text_input("Nume fișier:", value="Export_Maria_NutriFit")
            
            # Export CSV (cel mai sigur, fără erori de bibliotecă)
            csv_data = df.to_csv(index=False).encode('utf-8-sig')

            st.download_button(
                label="📥 Descarcă Raportul pentru Excel",
                data=csv_data,
                file_name=f"{nume_fis}.csv",
                mime="text/csv"
            )

# Adăugăm un mic footer
st.markdown("---")
st.caption("Aplicația Mariei v2.0 - Securizată și optimizată")
