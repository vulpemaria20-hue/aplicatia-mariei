import streamlit as st
import pandas as pd

# 1. CONFIGURARE PAGINĂ (Profesională și atractivă)
st.set_page_config(page_title="Nutriția Matematică - Sistem Expert", page_icon="⚖️", layout="wide")

# 2. SISTEM DE SECURITATE (Acces limitat)
if "autentificat" not in st.session_state:
    st.session_state.autentificat = False

if not st.session_state.autentificat:
    st.title("🔐 Acces Rezervat - Matematica Nutriției")
    st.markdown("Vă rugăm să introduceți parola de acces pentru a utiliza sistemul expert.")
    parola_introdusa = st.text_input("Parolă", type="password")
    if st.button("Autentificare"):
        if parola_introdusa == "nutrifit2026":
            st.session_state.autentificat = True
            st.rerun()
        else:
            st.error("Parolă incorectă. Vă rugăm să contactați administratorul.")
    st.stop()

# 3. GESTIONARE CLIENȚI (Bara laterală pentru multiplicitate)
st.sidebar.title("👥 Administrare Clienți")
nume_client = st.sidebar.text_input("Nume și Prenume Client", placeholder="Ex: Maria Ionescu")

if not nume_client:
    st.info("Introduceți numele clientului în bara laterală pentru a activa funcțiile de calcul.")
    st.stop()

# 4. BAZA DE DATE ALIMENTE ȘI REȚETE (Kcal/100g extrase din surse) [1-5]
baza_alimente = {
    "Tocană de legume": 29.15, "Mâncare de linte": 52.0, "Orez integral cu legume": 150.4,
    "Humus": 230.9, "Salată de ton": 158.0, "Omletă": 155.0, "Smoothie Verde": 54.2,
    "Kinder Felie de Lapte": 135.88, "Brioșe Spanac & Banană": 247.46, "Budincă Chia": 105.4,
    "Banana": 89.0, "Pâine integrală": 223.3, "Supă de pui": 24.14, "Iaurt grecesc 2%": 69.0,
    "Somon file": 208.0, "Vită slabă": 133.0, "Cod la grătar": 107.0, "Brioșe legume": 95.0
}

# 5. FUNCȚII DE CALCUL CONFORM MANUALULUI
def calcul_rmb(greutate, sex, varsta):
    # RMB diferențiat: Adulți (Pag. 13) vs Seniori (Pag. 20)
    if varsta >= 65:
        factor = 0.9 if sex == "Masculin" else 0.8
    else:
        factor = 1.0 if sex == "Masculin" else 0.8
    return factor * greutate * 24

def interpreteaza_imc(varsta, sex, imc):
    # Tabel Pediatric (Pag. 20) vs Adult (Pag. 20)
    if varsta < 18:
        tabel_copii = {
            "Masculin": {2: 18.8, 8: 19.3, 14: 24.8, 18: 27.9},
            "Feminin": {2: 18.7, 8: 19.8, 14: 26.0, 18: 28.7}
        }
        limita = tabel_copii[sex].get(varsta, 25.0)
        return "Obezitate" if imc >= limita else "Status Normal/Sub"
    else:
        if imc < 18.5: return "Subponderal"
        elif imc < 25: return "Normoponderal"
        elif imc < 30: return "Supraponderal"
        else: return "Obezitate"

# --- INTERFAȚA PRINCIPALĂ ---
st.title(f"🍎 Plan Nutrițional: {nume_client}")
tab1, tab2, tab3 = st.tabs(["📊 Calculator Metabolic", "🔍 Evaluare Evoluție", "🍱 Plan Alimentar"])

# ====================================================
# TAB 1: CALCULATOR METABOLIC (Metoda Bogdan Vasile)
# ====================================================
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        tip_p = st.selectbox("Categorie", ["Adult (18-65)", "Senior (>65)", "Copil/Adolescent"])
        greutate = st.number_input("Greutate (kg)", 10, 200, 70)
        inaltime = st.number_input("Înălțime (cm)", 80, 230, 170)
        varsta = st.number_input("Vârstă (ani)", 2, 100, 35)
        sex = st.radio("Sex", ["Masculin", "Feminin"])

    with col2:
        if tip_p == "Copil/Adolescent":
            st.info("Necesar caloric fix conform grupei de vârstă.") # [6]
            if varsta < 7: tnc = 1400
            elif varsta < 10: tnc = 1800
            elif varsta < 14: tnc = 2500 if sex == "Masculin" else 2250
            else: tnc = 3250 if sex == "Masculin" else 2400
        else:
            activitate = st.selectbox("Activitate (Indice IC)", [
                "Sedentar (25-30 kcal/kg)", "Ușor (30-35 kcal/kg)", 
                "Mediu (35-40 kcal/kg)", "Mare (40-45 kcal/kg)"
            ])
            # Corecție eroare IndexError: extragem prima valoare din interval
            ic = int(activitate.split("(")[7].split("-"))
            tnc = greutate * ic # Formula GA x IC [8]

        obiectiv = st.radio("Obiectivul Clientului", ["Menținere", "Scădere", "Creștere"])
        target = tnc
        if obiectiv == "Scădere": target -= 500
        elif obiectiv == "Creștere": target += 500

    if st.button("Generează Analiza"):
        rmb = calcul_rmb(greutate, sex, varsta)
        bmi = greutate / ((inaltime/100)**2)
        status = interpreteaza_imc(varsta, sex, bmi)
        
        st.subheader("Rezultate Analiză")
        c1, c2, c3 = st.columns(3)
        c1.metric("Țintă Zilnică", f"{target:.0f} kcal")
        c2.metric("RMB (Metabolism Bazal)", f"{rmb:.0f} kcal")
        c3.metric("Indice IMC", f"{bmi:.1f}")
        st.info(f"Interpretare IMC: **{status}**")
        
        if target < rmb:
            st.error(f"⚠️ ATENȚIE: Targetul ({target:.0f} kcal) este sub RMB ({rmb:.0f} kcal). Risc de încetinire metabolică!") # [9]

# ====================================================
# TAB 2: EVALUARE EVOLUȚIE (Circumferințe și Plicometrie)
# ====================================================
with tab2:
    st.subheader(f"Monitorizare Progres: {nume_client}")
    st.write("Evaluarea corectă presupune măsurarea circumferințelor și a pliurilor adipoase la fiecare 2 săptămâni.") # [10]
    
    col_c, col_p = st.columns(2)
    with col_c:
        st.write("**Centimetru (cm)**")
        talie = st.number_input("Circumferință Talie", 40, 160)
        coapsa = st.number_input("Circumferință Coapsă", 20, 100)
    with col_p:
        st.write("**Plicometru (mm)**")
        p_tri = st.number_input("Pliu Triceps", 0.0, 50.0)
        p_abd = st.number_input("Pliu Abdomen", 0.0, 50.0)
        st.info(f"Media pliurilor: {(p_tri + p_abd)/2:.1f} mm")
    st.caption("Pierderea sănătoasă în greutate: Greutatea scade ȘI Talia scade.") # [10]

# ====================================================
# TAB 3: PLAN ALIMENTAR (Gramaje calculate automat)
# ====================================================
with tab3:
    st.subheader(f"Meniu Personalizat ({target:.0f} kcal)")
    dist = {"MD": 0.25, "G1": 0.10, "PZ": 0.35, "G2": 0.10, "CN": 0.20} # Distribuție standard
    
    col_a, col_b = st.columns(2)
    with col_a:
        md = st.selectbox("Mic Dejun (25%)", ["Omletă", "Smoothie Verde", "Budincă Chia", "Brioșe legume"])
        pz = st.selectbox("Prânz (35%)", ["Tocană de legume", "Mâncare de linte", "Somon file", "Vită slabă"])
    with col_b:
        g1 = st.selectbox("Gustare (10%)", ["Banana", "Kinder Felie de Lapte", "Iaurt grecesc 2%"])
        cn = st.selectbox("Cină (20%)", ["Salată de ton", "Cod la grătar", "Supă de pui"])

    # Metoda de calcul a gramajului (Formula Pag. 117 din context / logică sursă)
    def calc_g(food, ratio):
        return (target * ratio / baza_alimente[food]) * 100

    plan_df = pd.DataFrame({
        "Masă": ["Mic Dejun", "Gustare", "Prânz", "Cină"],
        "Preparat": [md, g1, pz, cn],
        "Gramaj Recomandat": [
            f"{calc_g(md, dist['MD']):.0f} g", 
            f"{calc_g(g1, dist['G1']):.0f} g", 
            f"{calc_g(pz, dist['PZ']):.0f} g", 
            f"{calc_g(cn, dist['CN']):.0f} g"
        ]
    })
    st.table(plan_df)
    st.success("Plan generat profesional conform Metodologiei Vasile Bogdan.")
