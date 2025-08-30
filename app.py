import streamlit as st
import requests
import json
import datetime

# --- Page Configuration and Styling ---
st.set_page_config(
    page_title="AI Medical Prescription Verifier",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- NEW: Custom CSS for a Modern "Glassmorphism" Theme ---
st.markdown("""
<style>
    /* --- General Styling & Background --- */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: #FFFFFF;
    }

    /* --- Sidebar Styling --- */
    [data-testid="stSidebar"] {
        background-color: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* --- Main Header (Reusing Card Style) --- */
      .header {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px); /* For Safari */
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 0.8rem 1.5rem; /* Reduced padding */
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 1.5rem; /* Reduced margin */
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .header-left {
        display: flex;
        align-items: center;
    }
    .header h1 {
        margin: 0;
        font-size: 1.8rem; /* Further Reduced font size */
        color: #FFFFFF;
        font-weight: 700;
        margin-left: 15px;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.6);
    }
    .header-icon {
        font-size: 2.2rem; /* Further Reduced icon size */
        color: #00D4FF;
    }
    .header-date {
        color: #FFFFFF;
        font-weight: bold;
        font-size: 0.9rem; /* Further Reduced font size */
    }
    
    .page-title {
        text-align: center;
        margin-bottom: 0.5rem; /* Further reduced margin */
    }
    .page-title h2 {
        font-size: 2rem; /* Further Reduced font size */
        font-weight: 700;
        text-shadow: 0 0 15px rgba(0, 212, 255, 0.7);
        margin-bottom: 0.3rem; /* Reduced margin */
    }
    .page-title p {
        font-size: 0.9rem; /* Further Reduced font size */
        color: #e0e0e0;
        margin-top: 0;
    }


    
    .card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px); /* For Safari */
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }

    /* --- Typography --- */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF;
    }
    h2, h3 {
        color: #FFFFFF;
        text-shadow: 0 0 8px rgba(0, 212, 255, 0.5);
        border-bottom: 1px solid #00D4FF;
        padding-bottom: 10px;
    }
    
    /* --- Input Widget Styling --- */
    label {
        color: #FFFFFF !important;
        font-weight: bold;
    }
    
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div, .stTextArea textarea, .stMultiSelect div[data-baseweb="select"] > div {
        background-color: rgba(0, 0, 0, 0.3);
        color: #FFFFFF;
        border: 1px solid #00D4FF;
        border-radius: 8px;
    }
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox div[data-baseweb="select"] > div:focus-within, .stTextArea textarea:focus, .stMultiSelect div[data-baseweb="select"] > div:focus-within {
        border-color: #FFFFFF;
        box-shadow: 0 0 8px rgba(0, 212, 255, 0.5);
    }

    /* --- Radio Button Styling --- */
    .stRadio [role="radiogroup"] {
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        gap: 10px;
    }
    .stRadio label {
        flex: 1;
        text-align: center;
        padding: 8px 15px;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid #00D4FF;
        border-radius: 8px; /* Changed from 20px for a more official look */
        cursor: pointer;
        transition: all 0.2s ease-in-out;
    }
    .stRadio label:hover {
        background: rgba(0, 212, 255, 0.3);
    }

    /* --- Button Styling --- */
    div.stButton > button:first-child {
        background: linear-gradient(to right, #00c6ff, #0072ff);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 25px;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4);
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 114, 255, 0.6);
    }
    
    /* --- Patient Header & Expanders --- */
    .patient-detail-box {
        background: rgba(0, 212, 255, 0.1);
        border-left: 5px solid #00D4FF;
        padding: 12px;
        border-radius: 8px;
        font-size: 15px;
        height: 100%;
    }

    .streamlit-expanderHeader {
        background-color: rgba(0, 212, 255, 0.2);
        color: #FFFFFF;
        border-radius: 8px !important;
    }
    .streamlit-expanderContent {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }

    /* --- NEW: Footer Styling --- */
    .footer {
        text-align: center;
        padding-top: 2rem;
        padding-bottom: 1rem;
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# --- Header & Tools ---
def display_header():
    time_str = datetime.datetime.now().strftime('%A, %b %d, %Y')
    st.markdown(f"""
    <div class="header">
        <div class="header-left">
            <span class="header-icon">⚕️</span>
            <h1>MediGuard AI Verifier</h1>
        </div>
        <div class="header-date">
            <span>🗓️ {time_str}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

display_header()


# --- Backend API URL ---
BACKEND_URL = "http://127.0.0.1:8000"

# --- Initialize Session State ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# --- NEW: Backend Status Check ---
@st.cache_data(ttl=30) # Cache the status for 30 seconds
def check_backend_status():
    """Pings the backend to check for connectivity."""
    try:
        # A simple GET request to the root or a dedicated health-check endpoint
        response = requests.get(f"{BACKEND_URL}/", timeout=3)
        if response.status_code == 200:
            return "🟢 Connected"
        else:
            return f"🟡 Status: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "🔴 Disconnected"
    except requests.exceptions.Timeout:
        return "🔴 Timeout"

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("Main Menu")
    backend_status = check_backend_status()
    st.markdown(f"Backend Status: **{backend_status}**")
    if "🔴" in backend_status:
        st.warning("The backend is not reachable. Please start the FastAPI server.")
    st.markdown("---")

    if st.button("🏠 Home / New Analysis", use_container_width=True):
        keys_to_clear = ['patient_details', 'drugs', 'analysis_result']
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.page = 'home'
        st.rerun()

    if st.button("📜 Analysis History", use_container_width=True):
        st.session_state.page = 'history'
        st.rerun()
        
    if st.button("💊 Drug Database", use_container_width=True):
        st.session_state.page = 'database'
        st.rerun()
        
    if st.button("🩺 Symptom Checker", use_container_width=True):
        st.session_state.page = 'symptoms'
        st.rerun()

    st.markdown("---")
    st.info("This is a demonstration tool for medical professionals. Always verify results.")

# --- Page 1: Home / Patient Details ---
def patient_details_page():
    st.markdown("""
    <div class='page-title'>
        <h2>Begin a New Prescription Analysis</h2>
        <p>Enter patient details to start the AI-powered verification process.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; border-bottom: none; padding-bottom: 10px; margin-top: 0;'>👤 Patient Information</h3>", unsafe_allow_html=True)

    name = st.text_input("Full Name", placeholder="e.g., Jane Doe")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=30, step=1)
    with col2:
        gender = st.selectbox("Gender", ('Male', 'Female', 'Other'))
    with col3:
        blood_group = st.selectbox("Blood Group", ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'))
    
    st.markdown("<br>", unsafe_allow_html=True)

    submit_col_1, submit_col_2, submit_col_3 = st.columns([2, 3, 2])
    with submit_col_2:
        if st.button("Proceed to Prescription Input", use_container_width=True, type="primary"):
            if name:
                st.session_state['patient_details'] = {
                    "name": name, "age": age, "gender": gender, "blood_group": blood_group
                }
                st.session_state['page'] = 'analyzer'
                st.rerun()
            else:
                st.error("Patient name is required.")


# --- Page 2: Prescription Analyzer ---
def prescription_analyzer_page():
    if 'patient_details' not in st.session_state:
        st.warning("No patient data found. Please start from the Home page.")
        st.stop()
    
    patient = st.session_state['patient_details']
    
    
    st.markdown("<h2 style='text-align: center; border-bottom: none; padding-bottom: 10px;'>Prescription Analyzer 🔬</h2>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; border-bottom: none;'>👤 Patient on File</h3>", unsafe_allow_html=True)
    cols = st.columns(4)
    cols[0].markdown(f"<div class='patient-detail-box'><b>Name:</b><br>{patient['name']}</div>", unsafe_allow_html=True)
    cols[1].markdown(f"<div class='patient-detail-box'><b>Age:</b><br>{patient['age']}</div>", unsafe_allow_html=True)
    cols[2].markdown(f"<div class='patient-detail-box'><b>Gender:</b><br>{patient['gender']}</div>", unsafe_allow_html=True)
    cols[3].markdown(f"<div class='patient-detail-box'><b>Blood Group:</b><br>{patient.get('blood_group', 'N/A')}</div>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center;  border-bottom: none;'>💊 Prescription Details</h3>", unsafe_allow_html=True)
    input_method = st.selectbox("Input Method", ('Enter Drugs Manually', 'Paste Raw Prescription Text'))

    drugs_payload = []
    if 'drugs' not in st.session_state: st.session_state.drugs = [{"name": "", "dosage": ""}]

    if input_method == 'Enter Drugs Manually':
        for i, drug in enumerate(st.session_state.drugs):
            row = st.columns([4, 2, 1])
            st.session_state.drugs[i]['name'] = row[0].text_input(f"Drug Name {i+1}", drug['name'], key=f"name_{i}", label_visibility="collapsed", placeholder="Drug Name")
            st.session_state.drugs[i]['dosage'] = row[1].text_input(f"Dosage {i+1}", drug['dosage'], key=f"dosage_{i}", label_visibility="collapsed", placeholder="Dosage (e.g., 10mg)")
            if row[2].button("➖", key=f"del_{i}", help="Remove drug"):
                st.session_state.drugs.pop(i)
                st.rerun()
        if st.button("➕ Add another drug", key="add_drug"):
            st.session_state.drugs.append({"name": "", "dosage": ""})
            st.rerun()
        drugs_payload = [d for d in st.session_state.drugs if d['name'] and d['dosage']]
    else:
        prescription_text = st.text_area("Paste prescription text", height=150, placeholder="e.g., Take Lisinopril 10mg once daily...")
        if prescription_text:
            try:
                nlp_response = requests.post(f"{BACKEND_URL}/extract-from-text", json={"prescription_text": prescription_text})
                if nlp_response.status_code == 200:
                    extracted_data = nlp_response.json()
                    st.success("Successfully extracted drug information:")
                    st.json(extracted_data)
                    drugs_payload = extracted_data.get("drugs", [])
                else: st.error(f"Failed to extract info: {nlp_response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Connection Error: Could not connect to the FastAPI backend. Please ensure the backend server is running.")
            except Exception as e: st.error(f"An error occurred: {e}")

    btn_col1, btn_col2, btn_col3 = st.columns([2, 3, 2])
    if btn_col2.button("Analyze Prescription", type="primary", use_container_width=True):
        if not drugs_payload:
            st.warning("Please enter at least one drug to analyze.")
        else:
            with st.spinner("🤖 AI is analyzing the prescription..."):
                payload = {"patient": patient, "drugs": drugs_payload}
                try:
                    response = requests.post(f"{BACKEND_URL}/verify-prescription", json=payload)
                    if response.status_code == 200:
                        st.session_state.analysis_result = response.json()
                        history_entry = {
                            "patient": patient,
                            "drugs": drugs_payload,
                            "result": st.session_state.analysis_result,
                            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.session_state.analysis_history.insert(0, history_entry)
                        # We will not rerun here; the script will continue and show the dialog
                    else: st.error(f"Error from API: {response.status_code} - {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Connection Error: Could not connect to the FastAPI backend. Please ensure the backend server is running and accessible.")
                except Exception as e: st.error(f"An unexpected error occurred: {e}")

    # --- NEW: Display the analysis result in a pop-up dialog ---
    if 'analysis_result' in st.session_state:
        @st.dialog("🔬 Analysis Report")
        def display_report_dialog():
            result = st.session_state.analysis_result
            st.subheader("AI Verification Complete")
            st.markdown("---")
            
            with st.expander("⚠️ **Drug-Drug Interactions**", expanded=True):
                st.markdown(result.get("interaction_analysis", "No interaction analysis available."))
            
            with st.expander("🩺 **Dosage Recommendations**", expanded=True):
                st.markdown(result.get("dosage_recommendations", "No dosage recommendations available."))
            
            with st.expander("💡 **Alternative Suggestions**", expanded=True):
                st.markdown(result.get("alternative_suggestions", "No alternative suggestions available."))

            st.markdown("---")
            if st.button("Close Report", use_container_width=True, type="primary"):
                # Clean up the state and rerun to close the dialog
                del st.session_state['analysis_result']
                st.rerun()

        # Call the function to render the dialog
        display_report_dialog()


# --- Page 3: Analysis History ---
def analysis_history_page():
    # --- NEW: Confirmation Dialog Logic ---
    if 'show_clear_confirm' not in st.session_state:
        st.session_state.show_clear_confirm = False

    @st.dialog("⚠️ Confirm Deletion")
    def confirm_clear_dialog():
        st.error("Are you sure you want to permanently delete the entire analysis history? This action cannot be undone.")
        btn_cols = st.columns([1, 1])
        if btn_cols[0].button("Yes, Delete Everything", use_container_width=True, type="primary"):
            st.session_state.analysis_history = []
            st.session_state.show_clear_confirm = False
            st.rerun()
        if btn_cols[1].button("Cancel", use_container_width=True):
            st.session_state.show_clear_confirm = False
            st.rerun()

    if st.session_state.show_clear_confirm:
        confirm_clear_dialog()

    # --- MODIFIED: Header with Clear Button ---
    header_cols = st.columns([5, 1])
    with header_cols[0]:
        st.header("📜 Analysis History")
    with header_cols[1]:
        # Only show the clear button if there's history to clear
        if st.session_state.analysis_history:
            if st.button("🗑️ Clear", help="Delete all history entries", use_container_width=True):
                st.session_state.show_clear_confirm = True
                st.rerun()

    if not st.session_state.analysis_history:
        st.info("No analyses have been performed yet.")
        return

    # --- MODIFIED: Loop with more compact display ---
    for i, entry in enumerate(st.session_state.analysis_history):
        # Use a more compact title for the expander
        expander_title = f"{entry['patient']['name']} - {entry['timestamp']}"
        with st.expander(expander_title):
            # Using st.caption for smaller, less emphasized text for patient details
            st.caption(f"**Patient:** {entry['patient']['name']} | **Age:** {entry['patient']['age']} | **Gender:** {entry['patient']['gender']}")
            
            st.caption("**Prescribed Drugs:**")
            for drug in entry['drugs']:
                st.caption(f"- {drug['name']} ({drug['dosage']})")
            
            st.markdown("---")
            st.markdown("##### Full AI Report")
            st.info(f"**Interaction Analysis:**\n{entry['result'].get('interaction_analysis', 'N/A')}")
            st.success(f"**Dosage Recommendations:**\n{entry['result'].get('dosage_recommendations', 'N/A')}")
            st.warning(f"**Alternative Suggestions:**\n{entry['result'].get('alternative_suggestions', 'N/A')}")


# --- Page 4: Drug Database (Live API) ---
def drug_database_page():
    st.header("💊 Drug Database Search")
    drug_name = st.text_input("Enter Drug Name to Search", placeholder="e.g., Lipitor")
    
    if st.button("Search Drug", use_container_width=True):
        if drug_name:
            with st.spinner(f"Searching for {drug_name}..."):
                try:
                    # Using the OpenFDA API to search for the drug by brand name
                    api_url = f'https://api.fda.gov/drug/label.json?search=openfda.brand_name:"{drug_name}"&limit=1'
                    response = requests.get(api_url)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if 'results' in data and len(data['results']) > 0:
                            drug_info = data['results'][0]
                            
                            # Safely get brand and generic names
                            brand_name = drug_info.get('openfda', {}).get('brand_name', ['N/A'])[0]
                            generic_name = drug_info.get('openfda', {}).get('generic_name', ['N/A'])[0]
                            st.subheader(f"Displaying Information for: {brand_name} ({generic_name})")

                            # Display key information from the API response
                            with st.expander("📋 Indications & Usage", expanded=True):
                                indications = drug_info.get('indications_and_usage', ['Not available.'])[0]
                                st.markdown(indications)

                            with st.expander("Dosage & Administration", expanded=False):
                                dosage = drug_info.get('dosage_and_administration', ['Not available.'])[0]
                                st.markdown(dosage)
                            
                            with st.expander("⚠️ Warnings and Precautions", expanded=False):
                                warnings = drug_info.get('warnings_and_cautions', ['Not available.'])[0]
                                st.warning(warnings)

                            with st.expander("❗ Adverse Reactions (Side Effects)", expanded=False):
                                reactions = drug_info.get('adverse_reactions', ['Not available.'])[0]
                                st.info(reactions)

                            with st.expander("❌ Contraindications", expanded=False):
                                contra = drug_info.get('contraindications', ['Not available.'])[0]
                                st.error(contra)

                        else:
                            st.warning(f"No drug found with the name '{drug_name}'. Please check the spelling.")
                    else:
                        st.error(f"API Error: Failed to fetch data (Status code: {response.status_code}).")

                except requests.exceptions.RequestException as e:
                    st.error(f"Network Error: Could not connect to the drug database. Please check your connection. Details: {e}")
        else:
            st.warning("Please enter a drug name to search.")
            

# --- Page 5: Symptom Checker (Live AI Analysis) ---
def symptom_checker_page():
    st.header("🩺 AI-Powered Symptom Checker")
    st.info("This tool provides an AI-generated analysis of symptoms for informational purposes. It is not a substitute for a professional medical diagnosis.")
    
    symptoms = st.multiselect(
        "Select your symptoms from the list below",
        ["Fever", "Cough", "Headache", "Sore Throat", "Fatigue", "Nausea", "Dizziness", "Shortness of breath", "Body aches", "Chills"]
    )
    
    if st.button("Analyze Symptoms", use_container_width=True):
        if symptoms:
            with st.spinner("🧑‍⚕️ AI is analyzing your symptoms..."):
                try:
                    # New endpoint in the backend for symptom analysis
                    response = requests.post(f"{BACKEND_URL}/analyze-symptoms", json={"symptoms": symptoms})

                    if response.status_code == 200:
                        analysis = response.json()
                        st.subheader("AI-Powered Symptom Analysis")
                        st.markdown(analysis.get("report", "No analysis available from the AI."))
                        
                    else:
                        st.error(f"Error from API: {response.status_code} - {response.text}")

                except requests.exceptions.RequestException as e:
                    st.error(f"Network Error: Could not connect to the backend. Please ensure it's running. Details: {e}")
        else:
            st.warning("Please select at least one symptom to analyze.")


# --- Main App Router ---
page_router = {
    'home': patient_details_page,
    'analyzer': prescription_analyzer_page,
    'history': analysis_history_page,
    'database': drug_database_page,
    'symptoms': symptom_checker_page,
}

page_to_render = page_router.get(st.session_state.page, patient_details_page)
page_to_render()
