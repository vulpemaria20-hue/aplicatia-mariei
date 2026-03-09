import streamlit as st
import pandas as pd

# 1. Configurare Pagină
st.set_page_config(page_title="Sistem Maria AI", layout="wide", page_icon="🤖")

# --- LOGICA DE AUTENTIFICARE ---
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False

def ecran_login():
    st.title("🔐 Acces Sistem NutriFit 2026")
    parola = st.text_input("Introdu parola de acces:", type="password")
    if st.button("Conectare"):
        if parola == "nutrifit2026":
            st.session_state["autentificat"] = True
            st.rerun()
        else:
            st.error("Parolă incorectă!")

# --- APLICAȚIA PROPRIU-ZISĂ ---
if not st.session_state["autentificat"]:
    ecran_login()
else:
    # Meniu lateral
    st.sidebar.title("Meniu Agent AI")
    if st.sidebar.button("Ieșire (Logout)"):
        st.session_state["autentificat"] = False
        st.rerun()

    # 2. AGENTUL AI ȘI SELECȚIA CELOR 200 DE OPȚIUNI
    st.title("🤖 Agent AI NutriFit")
    st.write("Salut! Sunt asistentul tău. Selectează opțiunile pentru raportul final.")

    # Generăm o listă de 200 de opțiuni pentru Agentul AI
    optiuni_ai = [f"Opțiunea {i}: Plan Nutrițional {i*5} calorii" for i in range(1, 201)]
    
    selected_options = st.multiselect(
        "Alege din cele 200 de configurații disponibile:",
        optiuni_ai,
        default=optiuni_ai[:3] # Pre-selectăm primele 3 pentru exemplu
    )

    if st.button("Procesează datele cu AI"):
        st.success("Agentul AI a finalizat procesarea!")
        
        # 3. GENERARE RAPORT PE BAZA SELECȚIEI
        st.divider()
        st.subheader("📊 Tabel Rezultate Final")
        
        # Creăm tabelul bazat pe ce s-a ales din lista de 200
        raport_data = []
        for item in selected_options:
            pret_baza = 150 # Exemplu pret
            raport_data.append({
                "Denumire Serviciu": item,
                "Cantitate": 1,
                "Pret Unitar (RON)": pret_baza,
                "TVA (19%)": pret_baza * 0.19,
                "Total de Plata": pret_baza * 1.19
            })
        
        df_final = pd.DataFrame(raport_data)
        st.dataframe(df_final, use_container_width=True)

        # 4. EXPORT (Format sigur CSV)
        st.divider()
        st.subheader("💾 Finalizare și Export")
        
        nume_fisier = st.text_input("Nume fișier export:", value="Raport_Final_Maria")
        
        # Conversie CSV sigură pentru Excel (cu utf-8-sig pentru caractere speciale)
        csv_data = df_final.to_csv(index=False).encode('utf-8-sig')

        st.download_button(
            label="📥 Descarcă Raportul (CSV/Excel)",
            data=csv_data,
            file_name=f"{nume_fisier}.csv",
            mime="text/csv"
        )

# --- NOTĂ FINALĂ ---
# Acest cod acoperă tot fluxul: Login -> AI Selection (200 optiuni) -> Tabel -> Export.
