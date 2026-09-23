import pandas as pd


# ---------------------------------------------------------
# Identify possible risk indicators
# ---------------------------------------------------------

def identify_risk_indicators(row):

    warnings = []

    if row["Systolic_BP"] >= 140:
        warnings.append("High systolic blood pressure")

    if row["Diastolic_BP"] >= 90:
        warnings.append("High diastolic blood pressure")

    if row["Heart_Rate"] > 100:
        warnings.append("High heart rate")

    if row["Heart_Rate"] < 60:
        warnings.append("Low heart rate")

    if row["Glucose"] >= 126:
        warnings.append("Elevated blood glucose")

    if row["SpO2"] < 95:
        warnings.append("Low oxygen saturation")

    if row["Temperature"] >= 38:
        warnings.append("High temperature")

    if row["Respiratory_Rate"] > 20:
        warnings.append("High respiratory rate")

    if row["BMI"] >= 30:
        warnings.append("BMI in obesity range")

    return warnings


# ---------------------------------------------------------
# Analyze patient
# ---------------------------------------------------------

def analyze_patient(data):

    df = pd.DataFrame([data])

    risk_indicators = identify_risk_indicators(df.iloc[0])

    df["Risk_Indicators"] = (
        ", ".join(risk_indicators)
        if risk_indicators
        else "No flagged observation"
    )

    return df


# ---------------------------------------------------------
# Calculate descriptive statistics
# ---------------------------------------------------------

def calculate_statistics(df):

    columns = [
        "Age",
        "Systolic_BP",
        "Diastolic_BP",
        "Heart_Rate",
        "Glucose",
        "SpO2",
        "Temperature",
        "Respiratory_Rate",
        "BMI"
    ]

    available_columns = [
        column for column in columns
        if column in df.columns
    ]

    return df[available_columns].describe().T


# ---------------------------------------------------------
# Create analytical summary
# ---------------------------------------------------------

def create_summary(data):

    risk_indicators = identify_risk_indicators(data)

    summary = {
        "Total Risk Indicators": len(risk_indicators),
        "Risk Indicators": risk_indicators
    }

    return summary


# ---------------------------------------------------------
# Generate alerts
# ---------------------------------------------------------

def generate_alerts(data):

    alerts = []

    if data["Systolic_BP"] >= 140 or data["Diastolic_BP"] >= 90:
        alerts.append(
            "Blood pressure is above the selected project threshold."
        )

    if data["Glucose"] >= 126:
        alerts.append(
            "Blood glucose is above the selected project threshold."
        )

    if data["SpO2"] < 95:
        alerts.append(
            "Oxygen saturation is below the selected project threshold."
        )

    if data["Heart_Rate"] > 100:
        alerts.append(
            "Heart rate is above the selected project threshold."
        )

    if data["Heart_Rate"] < 60:
        alerts.append(
            "Heart rate is below the selected project threshold."
        )

    if data["Temperature"] >= 38:
        alerts.append(
            "Temperature is above the selected project threshold."
        )

    if data["Respiratory_Rate"] > 20:
        alerts.append(
            "Respiratory rate is above the selected project threshold."
        )

    if data["BMI"] >= 30:
        alerts.append(
            "BMI is in the obesity range."
        )

    return alerts


# ---------------------------------------------------------
# Generate decision-support information
# ---------------------------------------------------------

def generate_recommendations(data):

    recommendations = []

    if data["Systolic_BP"] >= 140 or data["Diastolic_BP"] >= 90:
        recommendations.append(
            "Consider repeat blood pressure measurement and "
            "clinical review if elevated readings persist."
        )

    if data["Glucose"] >= 126:
        recommendations.append(
            "Consider repeat glucose assessment and appropriate "
            "clinical evaluation."
        )

    if data["SpO2"] < 95:
        recommendations.append(
            "Repeat oxygen saturation measurement and consider "
            "clinical assessment if the low value persists."
        )

    if data["Heart_Rate"] > 100 or data["Heart_Rate"] < 60:
        recommendations.append(
            "Consider repeating the heart-rate measurement and "
            "reviewing it in the clinical context."
        )

    if data["Temperature"] >= 38:
        recommendations.append(
            "Monitor temperature and consider clinical evaluation "
            "if fever persists or symptoms are present."
        )

    if data["Respiratory_Rate"] > 20:
        recommendations.append(
            "Repeat respiratory-rate measurement and consider "
            "clinical assessment if elevated."
        )

    if data["BMI"] >= 30:
        recommendations.append(
            "Consider lifestyle assessment and appropriate "
            "weight-management counselling."
        )

    if not recommendations:
        recommendations.append(
            "No project-defined risk indicators were detected. "
            "Continue routine monitoring as appropriate."
        )

    return recommendations