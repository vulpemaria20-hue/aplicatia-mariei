import streamlit as st
import pandas as pd

# CONFIGURARE PAGINĂ PROFESIONALĂ
st.set_page_config(page_title="Sistem Expert - Matematica Nutriției", page_icon="⚖️", layout="wide")

# --- BAZA DE DATE ALIMENTE & REȚETE (Kcal per 100g) ---
# Date extrase din Metode de calcul rețete și diete calculate (pag. 23-107)
baza_alimente = {
    "Omletă simplă": 155.0, "Omletă cu legume": 110.0, "Ou fiert": 155.0,
    "Smoothie Verde (spanac, măr, afine)": 54.2, "Smoothie Fructe Pădure": 114.6,
    "Smoothie Mango & Cătină": 94.2, "Budincă Chia & Zmeură": 105.4,
    "Pâine integrală graham": 223.3, "Iaurt grecesc 2%": 97.0, "Chefir 3.3%": 60.0,
    "Tocană de legume": 29.15, "Mâncare de linte": 188.41, "Humus clasic": 230.9,
    "Orez integral cu legume": 150.4, "Iahnie de fasole": 154.1, "Supă de pui": 24.14,
    "Piept de pui grătar": 165.0, "Piept de curcan grill": 140.0, "Somon file": 208.0,
    "Cod la grătar": 107.0, "Dorada la cuptor": 89.0, "Mușchi de porc": 145.0,
    "Cartofi dulci copți": 116.0, "Mămăligă": 66.0, "Quinoa fiartă": 120.0,
    "Kinder Felie de Lapte (Proteic)": 135.88, "Brioșe Spanac & Banană": 247.46,
    "Brioșe din Legume": 95.0, "Banana": 89.0, "Măr": 52.0, "Nuci/Migdale": 575.0
}

# --- FUNCȚII DE CALCUL CONFORM METODOLOGIEI VASILE BOGDAN ---

def calcul_rmb(greutate, sex, varsta):
    """Calculează Rata Metabolismului Bazal (RMB) conform pag. 12 și 50."""
    if varsta >= 65:  # RMB Seniori
        return (0.9 if sex == "Masculin" else 0.8) * greutate * 24
    else:  # RMB Adulți
        return (1.0 if sex == "Masculin" else 0.8) * greutate * 24

def interpreteaza_imc_copii(varsta, sex, imc):
    """Interpretare IMC pediatric conform Tabelului de BMI (pag. 54)."""
    tabel = {
        "Masculin": {
            2: [14.9, 17.8, 18.8], 8: [14.0, 17.4, 19.3], 
            14: [16.3, 21.9, 24.8], 18: [18.6, 24.9, 27.9]
        },
        "Feminin": {
            2: [14.6, 17.8, 18.7], 8: [13.8, 17.6, 19.8], 
            14: [16.2, 22.4, 26.0], 18: [17.9, 24.8, 28.7]
        }
    }
    # Căutăm vârsta cea mai apropiată în tabel
    varste_disponibile = sorted(tabel[sex].keys())
    v_cheie = min(varste_disponibile, key=lambda x: abs(x - varsta))
    limite = tabel[sex][v_cheie]
    
    if imc < limite: return "Subponderal"
    elif imc <= limite[1]: return "Normoponderal"
    elif imc <= limite[2]: return "Peste greutate"
    else: return "Obezitate"

# --- INTERFAȚA UTILIZATOR ---

if "autentificat" not in st.session_state:
    st.session_state.autentificat = False

if not st.session_state.autentificat:
    st.title("🔐 Acces Sistem Expert Nutriție")
    parola = st.text_input("Cod de acces", type="password")
    if st.button("Autentificare"):
        if parola == "nutrifit2026":
            st.session_state.autentificat = True
            st.rerun()
        else: st.error("Cod incorect!")
    st.stop()

st.title("⚖️ Nutriția Matematică - Sistem de Planificare")
tab1, tab2, tab3, tab4 = st.tabs(["📊 Calculator Caloric", "🔍 Evaluare Fizică", "🍱 Plan Alimentar", "🛒 Listă Cumpărături"])

# --- TAB 1: CALCULATOR METABOLIC ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Date Client")
        tip_p = st.selectbox("Categorie", ["Adult", "Senior (>65 ani)", "Copil/Adolescent"])
        ga = st.number_input("Greutate Actuală (kg)", 10.0, 250.0, 75.0)
        inaltime = st.number_input("Înălțime (cm)", 80, 230, 170)
        varsta = st.number_input("Vârstă (ani)", 2, 100, 35)
        sex = st.radio("Sex", ["Masculin", "Feminin"])
    
    with col2:
        st.subheader("Obiective")
        if tip_p == "Copil/Adolescent":
            st.info("Se utilizează necesarul caloric fix pe grupe de vârstă (pag. 26).")
            if varsta < 7: tnc_baza = 1400
            elif varsta < 10: tnc_baza = 1800
            elif varsta < 14: tnc_baza = 2500 if sex == "Masculin" else 2250
            else: tnc_baza = 3250 if sex == "Masculin" else 2400
            ic_ales = 0
        else:
            activitate = st.selectbox("Nivel Activitate (IC)", [
                ("Sedentar (25-30)", 27), ("Ușor (30-35)", 32), 
                ("Mediu (35-40)", 37), ("Mare (40-45)", 42), ("Foarte Mare (45-50)", 47)
            ])
            ic_ales = activitate[1]
            tnc_baza = ga * ic_ales

        obiectiv = st.selectbox("Scopul propus", ["Menținere", "Scădere în greutate", "Creștere în greutate", "Remodelare Somatotip"])
        
        target = tnc_baza
        if obiectiv == "Scădere în greutate":
            deficit = st.slider("Deficit (Kcal)", 500, 1000, 500)
            target = tnc_baza - deficit
        elif obiectiv == "Creștere în greutate":
            surplus = st.slider("Surplus (Kcal)", 500, 1000, 500)
            target = tnc_baza + surplus

    if st.button("Calculează"):
        rmb = calcul_rmb(ga, sex, varsta)
        bmi = ga / ((inaltime/100)**2)
        st.session_state.target_final = target
        
        if target < rmb:
            st.error(f"⚠️ Atenție: Targetul ({target:.0f} Kcal) este sub RMB ({rmb:.0f} Kcal). Pericol de încetinire metabolică!")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Necesar (TNC)", f"{tnc_baza:.0f} Kcal")
        c2.metric("Target Obiectiv", f"{target:.0f} Kcal")
        c3.metric("Baza (RMB)", f"{rmb:.0f} Kcal")
        
        if varsta < 18:
            status = interpreteaza_imc_copii(varsta, sex, bmi)
        else:
            status = "Normal" if 18.5 <= bmi < 25 else "Supraponderal" if bmi < 30 else "Obezitate"
        st.info(f"**Indice de Masă Corporală:** {
