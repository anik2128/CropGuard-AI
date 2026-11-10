def analyse_irrigation(readings):

    try:
        moisture = float(
            readings.get("Soil Moisture",
                         readings.get("soil_moisture"))
        )
    except (TypeError, ValueError):
        return {
            "status": "DATA UNAVAILABLE",
            "priority": "UNKNOWN",
            "reason": "Invalid soil moisture reading.",
            "action": "Check input data."
        }

    if not 0 <= moisture <= 100:
        return {
            "status": "INVALID READING",
            "priority": "UNKNOWN",
            "reason": "Moisture must be between 0 and 100.",
            "action": "Check input data."
        }

    if moisture <= 30:
        status = "LOW SOIL MOISTURE"
        priority = "HIGH"
        reason = "Demo soil moisture is very low."
        action = "Irrigation may be required."

    elif moisture <= 40:
        status = "MOISTURE BELOW TARGET"
        priority = "MODERATE"
        reason = "Demo soil moisture is slightly low."
        action = "Recheck soil moisture soon."

    elif moisture <= 65:
        status = "MOISTURE IN DEMO RANGE"
        priority = "LOW"
        reason = "Demo moisture is within the selected range."
        action = "No irrigation suggested."

    else:
        status = "HIGH SOIL MOISTURE"
        priority = "HOLD"
        reason = "Demo soil moisture is high."
        action = "Avoid additional watering."

    return {
        "status": status,
        "priority": priority,
        "reason": reason,
        "action": action
    }