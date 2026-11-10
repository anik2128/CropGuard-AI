def analyse_disease_risk(readings):

    temperature = readings["Air Temperature"]
    humidity = readings["Humidity"]

    risk_score = 0
    reasons = []

    # Humidity assessment
    if humidity >= 90:
        risk_score += 50
        reasons.append("Very high humidity")
    elif humidity >= 85:
        risk_score += 35
        reasons.append("High humidity")
    elif humidity >= 75:
        risk_score += 15
        reasons.append("Elevated humidity")

    # Temperature assessment
    if 18 <= temperature <= 30 and humidity >= 85:
        risk_score += 25
        reasons.append("Conditions may favour fungal disease development")

    if temperature >= 35:
        reasons.append("High-temperature crop stress")

    # Risk classification
    if risk_score >= 60:
        risk_level = "HIGH"
    elif risk_score >= 30:
        risk_level = "MODERATE"
    else:
        risk_level = "LOW"

    if not reasons:
        reasons.append("No major environmental risk indicators detected")

    return {
        "risk_level": risk_level,
        "risk_score": min(risk_score, 100),
        "reasons": reasons,
        "warning": "Environmental risk estimate only. "
                   "This does not diagnose a plant disease."
    }