import streamlit as st

from analysis import analyze_patient
from cdss import show_cdss_dashboard


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Biomedical Information System",
    page_icon="🩺",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "patient_data" not in st.session_state:
    st.session_state.patient_data = None


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🩺 Biomedical System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Patient Information",
        "CDSS Results"
    ]
)


# =========================================================
# PATIENT INFORMATION PAGE
# =========================================================

if page == "Patient Information":

    st.title("🩺 Biomedical Information System")

    st.write(
        "Enter patient biomedical information "
        "for analysis and decision support."
    )

    st.divider()

    # -----------------------------------------------------
    # Patient Information
    # -----------------------------------------------------

    st.header("👤 Patient Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        patient_id = st.text_input(
            "Patient ID"
        )

    with col2:

        age = st.number_input(
            "Age (years)",
            min_value=0,
            max_value=120,
            value=25
        )

    with col3:

        sex = st.selectbox(
            "Sex",
            [
                "Male",
                "Female",
                "Other"
            ]
        )

    # -----------------------------------------------------
    # Vital Signs
    # -----------------------------------------------------

    st.header("❤️ Vital Signs")

    col1, col2, col3 = st.columns(3)

    with col1:

        systolic_bp = st.number_input(
            "Systolic BP (mmHg)",
            min_value=50,
            max_value=250,
            value=120
        )

        diastolic_bp = st.number_input(
            "Diastolic BP (mmHg)",
            min_value=30,
            max_value=150,
            value=80
        )

    with col2:

        heart_rate = st.number_input(
            "Heart Rate (bpm)",
            min_value=30,
            max_value=220,
            value=72
        )

        temperature = st.number_input(
            "Temperature (°C)",
            min_value=30.0,
            max_value=45.0,
            value=36.7,
            step=0.1
        )

    with col3:

        spo2 = st.number_input(
            "SpO₂ (%)",
            min_value=50,
            max_value=100,
            value=98
        )

        respiratory_rate = st.number_input(
            "Respiratory Rate",
            min_value=5,
            max_value=60,
            value=16
        )

    # -----------------------------------------------------
    # Laboratory Measurements
    # -----------------------------------------------------

    st.header("🧪 Laboratory Measurements")

    col1, col2 = st.columns(2)

    with col1:

        glucose = st.number_input(
            "Blood Glucose (mg/dL)",
            min_value=20.0,
            max_value=600.0,
            value=100.0,
            step=1.0
        )

    with col2:

        hemoglobin = st.number_input(
            "Hemoglobin (g/dL)",
            min_value=3.0,
            max_value=25.0,
            value=14.0,
            step=0.1
        )

    # -----------------------------------------------------
    # Body Measurements
    # -----------------------------------------------------

    st.header("⚖️ Body Measurements")

    col1, col2, col3 = st.columns(3)

    with col1:

        height = st.number_input(
            "Height (cm)",
            min_value=50.0,
            max_value=250.0,
            value=170.0,
            step=0.1
        )

    with col2:

        weight = st.number_input(
            "Weight (kg)",
            min_value=2.0,
            max_value=300.0,
            value=70.0,
            step=0.1
        )

    with col3:

        bmi = weight / ((height / 100) ** 2)

        st.metric(
            "Calculated BMI",
            f"{bmi:.2f}"
        )

    # -----------------------------------------------------
    # Analyze Button
    # -----------------------------------------------------

    st.divider()

    if st.button(
        "🔍 Analyze Patient Data",
        type="primary",
        use_container_width=True
    ):

        patient_data = {

            "Patient_ID": patient_id,

            "Age": age,

            "Sex": sex,

            "Systolic_BP": systolic_bp,

            "Diastolic_BP": diastolic_bp,

            "Heart_Rate": heart_rate,

            "Temperature": temperature,

            "SpO2": spo2,

            "Respiratory_Rate": respiratory_rate,

            "Glucose": glucose,

            "Hemoglobin": hemoglobin,

            "Height": height,

            "Weight": weight,

            "BMI": bmi
        }

        # Send data to analysis.py
        analyzed_data = analyze_patient(
            patient_data
        )

        # Store original patient data
        # for the CDSS dashboard
        st.session_state.patient_data = (
            patient_data
        )

        st.success(
            "Patient data analyzed successfully!"
        )

        st.info(
            "Open 'CDSS Results' from the sidebar "
            "to view the analysis."
        )


# =========================================================
# CDSS RESULTS PAGE
# =========================================================

elif page == "CDSS Results":

    if st.session_state.patient_data is None:

        st.warning(
            "No patient data is available yet."
        )

        st.info(
            "Please enter patient information "
            "first."
        )

    else:

        show_cdss_dashboard(
            st.session_state.patient_data
        )