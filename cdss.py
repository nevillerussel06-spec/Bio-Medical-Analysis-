import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from analysis import (
    generate_alerts,
    generate_recommendations,
    identify_risk_indicators
)


def show_cdss_dashboard(patient_data):

    st.title("🩺 CDSS Results Dashboard")
    st.write(
        "Clinical Decision Support System — "
        "Biomedical Data Analysis"
    )

    # =========================================================
    # MEDICAL DISCLAIMER
    # =========================================================

    st.warning(
        "⚕️ MEDICAL DISCLAIMER: The information and reports "
        "shown by this system are generated for educational "
        "and decision-support purposes only. The system may "
        "make errors or produce inaccurate results. These "
        "results must not be considered a medical diagnosis "
        "or a substitute for professional medical advice. "
        "Please consult a qualified healthcare professional "
        "or relevant field expert for further evaluation "
        "and more information."
    )

    st.divider()

    # =========================================================
    # PATIENT INFORMATION
    # =========================================================

    st.header("👤 Patient Information")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Patient ID",
            patient_data["Patient_ID"]
        )

    with col2:
        st.metric(
            "Age",
            f'{patient_data["Age"]} years'
        )

    with col3:
        st.metric(
            "Sex",
            patient_data["Sex"]
        )

    with col4:
        st.metric(
            "BMI",
            f'{patient_data["BMI"]:.2f}'
        )

    st.divider()

    # =========================================================
    # VITAL SIGNS
    # =========================================================

    st.header("❤️ Vital Signs")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Blood Pressure",
            f'{patient_data["Systolic_BP"]}/{patient_data["Diastolic_BP"]} mmHg'
        )

    with col2:
        st.metric(
            "Heart Rate",
            f'{patient_data["Heart_Rate"]} bpm'
        )

    with col3:
        st.metric(
            "SpO₂",
            f'{patient_data["SpO2"]}%'
        )

    with col4:
        st.metric(
            "Temperature",
            f'{patient_data["Temperature"]:.1f} °C'
        )

    with col5:
        st.metric(
            "Respiratory Rate",
            f'{patient_data["Respiratory_Rate"]}/min'
        )

    # =========================================================
    # LABORATORY RESULTS
    # =========================================================

    st.header("🧪 Laboratory Results")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Blood Glucose",
            f'{patient_data["Glucose"]:.1f} mg/dL'
        )

    with col2:
        st.metric(
            "Hemoglobin",
            f'{patient_data["Hemoglobin"]:.1f} g/dL'
        )

    st.divider()

    # =========================================================
    # RISK INDICATORS
    # =========================================================

    st.header("⚠️ Identified Risk Indicators")

    risk_indicators = identify_risk_indicators(patient_data)

    if risk_indicators:

        st.warning(
            f"{len(risk_indicators)} potential risk indicator(s) detected."
        )

        for risk in risk_indicators:
            st.write(f"🔸 {risk}")

    else:

        st.success(
            "No project-defined risk indicators detected."
        )

    # =========================================================
    # ALERTS
    # =========================================================

    st.header("🚨 Alerts")

    alerts = generate_alerts(patient_data)

    if alerts:

        for alert in alerts:
            st.error(f"⚠️ {alert}")

    else:

        st.success(
            "No alerts generated from the selected thresholds."
        )

    st.divider()

    # =========================================================
    # ANALYTICAL RESULTS
    # =========================================================

    st.header("📊 Analytical Results")

    analytical_data = pd.DataFrame({
        "Parameter": [
            "Systolic Blood Pressure",
            "Diastolic Blood Pressure",
            "Heart Rate",
            "Blood Glucose",
            "SpO₂",
            "Temperature",
            "Respiratory Rate",
            "Hemoglobin",
            "BMI"
        ],

        "Value": [
            patient_data["Systolic_BP"],
            patient_data["Diastolic_BP"],
            patient_data["Heart_Rate"],
            patient_data["Glucose"],
            patient_data["SpO2"],
            patient_data["Temperature"],
            patient_data["Respiratory_Rate"],
            patient_data["Hemoglobin"],
            patient_data["BMI"]
        ],

        "Unit": [
            "mmHg",
            "mmHg",
            "bpm",
            "mg/dL",
            "%",
            "°C",
            "breaths/min",
            "g/dL",
            "kg/m²"
        ]
    })

    st.dataframe(
        analytical_data,
        use_container_width=True,
        hide_index=True
    )

    # =========================================================
    # GRAPH 1 - BLOOD PRESSURE BAR CHART
    # =========================================================

    st.header("🩸 Blood Pressure Analysis")

    bp_data = pd.DataFrame({
        "Measurement": [
            "Systolic BP",
            "Diastolic BP"
        ],

        "Value": [
            patient_data["Systolic_BP"],
            patient_data["Diastolic_BP"]
        ]
    })

    st.bar_chart(
        bp_data.set_index("Measurement")
    )

    st.caption(
        "Comparison of systolic and diastolic blood pressure measurements."
    )

    # =========================================================
    # GRAPH 2 - VITAL SIGNS PIE CHART
    # =========================================================

    st.header("❤️ Vital Signs Pie Chart")

    vital_labels = [
        "Heart Rate",
        "SpO₂",
        "Respiratory Rate"
    ]

    vital_values = [
        patient_data["Heart_Rate"],
        patient_data["SpO2"],
        patient_data["Respiratory_Rate"]
    ]

    vital_fig = go.Figure(
        data=[
            go.Pie(
                labels=vital_labels,
                values=vital_values,
                hole=0
            )
        ]
    )

    vital_fig.update_layout(
        title="Vital Signs Distribution",
        height=450
    )

    st.plotly_chart(
        vital_fig,
        use_container_width=True
    )

    st.caption(
        "Pie chart showing the relative values of selected vital-sign measurements."
    )

    # =========================================================
    # GRAPH 3 - LABORATORY DONUT CHART
    # =========================================================

    st.header("🧪 Laboratory Measurement Distribution")

    laboratory_labels = [
        "Glucose",
        "Hemoglobin"
    ]

    laboratory_values = [
        patient_data["Glucose"],
        patient_data["Hemoglobin"]
    ]

    laboratory_fig = go.Figure(
        data=[
            go.Pie(
                labels=laboratory_labels,
                values=laboratory_values,
                hole=0.5
            )
        ]
    )

    laboratory_fig.update_layout(
        title="Laboratory Measurements",
        height=450
    )

    st.plotly_chart(
        laboratory_fig,
        use_container_width=True
    )

    st.caption(
        "Donut chart showing the relative values of selected laboratory measurements."
    )

    # =========================================================
    # GRAPH 4 - TEMPERATURE VS RESPIRATORY RATE
    # =========================================================

    st.header("🌡️ Temperature & Respiratory Analysis")

    temperature_respiratory_fig = go.Figure()

    temperature_respiratory_fig.add_trace(
        go.Scatter(
            x=[patient_data["Temperature"]],
            y=[patient_data["Respiratory_Rate"]],
            mode="markers",
            marker=dict(size=15),
            name="Patient"
        )
    )

    temperature_respiratory_fig.update_layout(
        title="Temperature vs Respiratory Rate",
        xaxis_title="Temperature (°C)",
        yaxis_title="Respiratory Rate (/min)",
        height=450
    )

    st.plotly_chart(
        temperature_respiratory_fig,
        use_container_width=True
    )

    st.caption(
        "Scatter plot showing the patient's temperature and respiratory rate."
    )

    # =========================================================
    # GRAPH 5 - RISK INDICATOR LINE CHART
    # =========================================================

    st.header("📈 Risk Indicator Analysis")

    risk_categories = [
        "High BP",
        "Heart Rate",
        "Glucose",
        "Low SpO₂",
        "Temperature",
        "Respiratory Rate",
        "BMI"
    ]

    risk_values = [
        int(
            patient_data["Systolic_BP"] >= 140
            or patient_data["Diastolic_BP"] >= 90
        ),

        int(
            patient_data["Heart_Rate"] > 100
            or patient_data["Heart_Rate"] < 60
        ),

        int(
            patient_data["Glucose"] >= 126
        ),

        int(
            patient_data["SpO2"] < 95
        ),

        int(
            patient_data["Temperature"] >= 38
        ),

        int(
            patient_data["Respiratory_Rate"] > 20
        ),

        int(
            patient_data["BMI"] >= 30
        )
    ]

    risk_fig = go.Figure()

    risk_fig.add_trace(
        go.Scatter(
            x=risk_categories,
            y=risk_values,
            mode="lines+markers",
            marker=dict(size=10),
            line=dict(width=3),
            name="Risk Status"
        )
    )

    risk_fig.update_layout(
        title="Project-Defined Risk Indicator Status",
        xaxis_title="Risk Indicator",
        yaxis_title="Detected (1) / Not Detected (0)",
        yaxis=dict(
            tickmode="array",
            tickvals=[0, 1],
            ticktext=["Not Detected", "Detected"],
            range=[-0.1, 1.1]
        ),
        height=500
    )

    st.plotly_chart(
        risk_fig,
        use_container_width=True
    )

    st.caption(
        "A value of 1 indicates that the corresponding project-defined "
        "threshold was flagged; 0 indicates that it was not flagged."
    )

    # =========================================================
    # DECISION SUPPORT
    # =========================================================

    st.header("💡 Decision-Support Information")

    recommendations = generate_recommendations(
        patient_data
    )

    for recommendation in recommendations:

        st.info(
            f"💡 {recommendation}"
        )

    # =========================================================
    # CDSS SUMMARY
    # =========================================================

    st.header("📋 CDSS Summary")

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:

        st.metric(
            "Risk Indicators",
            len(risk_indicators)
        )

    with summary_col2:

        st.metric(
            "Alerts",
            len(alerts)
        )

    with summary_col3:

        if len(risk_indicators) == 0:

            status = "No Flags"

        elif len(risk_indicators) <= 2:

            status = "Monitor"

        else:

            status = "Multiple Flags"

        st.metric(
            "Analysis Status",
            status
        )

    # =========================================================
    # FINAL MEDICAL DISCLAIMER
    # =========================================================

    st.divider()

    st.error(
        "⚕️ Medical Disclaimer: This CDSS is an educational "
        "prototype and is not intended to provide a medical "
        "diagnosis, treatment decision, or emergency medical advice. "
        "Reports generated by the system may contain errors or "
        "inaccuracies. Please verify the information with a "
        "qualified healthcare professional or relevant field expert "
        "before making any medical decision."
    )