def analyse_soil(soil_data):

    parameters = {
        "pH": soil_data.get("pH"),
        "Nitrogen": soil_data.get("nitrogen"),
        "Phosphorus": soil_data.get("phosphorus"),
        "Potassium": soil_data.get("potassium"),
        "Organic Carbon": soil_data.get("organic_carbon"),
        "Soil Moisture": soil_data.get("soil_moisture")
    }

    missing = [
        name for name, value in parameters.items()
        if value is None
    ]

    # General pH classification
    ph = parameters["pH"]

    if ph is None:
        ph_status = "NOT AVAILABLE"
    elif not 0 <= float(ph) <= 14:
        ph_status = "INVALID VALUE"
    elif ph < 5.5:
        ph_status = "STRONGLY ACIDIC"
    elif ph < 6.5:
        ph_status = "MODERATELY ACIDIC"
    elif ph <= 7.5:
        ph_status = "NEAR NEUTRAL"
    elif ph <= 8.5:
        ph_status = "MODERATELY ALKALINE"
    else:
        ph_status = "STRONGLY ALKALINE"

    moisture = parameters["Soil Moisture"]

    if moisture is None:
        moisture_status = "NOT AVAILABLE"
    elif not 0 <= float(moisture) <= 100:
        moisture_status = "INVALID VALUE"
    elif moisture < 20:
        moisture_status = "LOW"
    elif moisture <= 60:
        moisture_status = "MODERATE"
    else:
        moisture_status = "HIGH"

    return {
        "ph_status": ph_status,
        "moisture_status": moisture_status,
        "available_parameters": len(parameters) - len(missing),
        "total_parameters": len(parameters),
        "missing_parameters": missing,
        "assessment": (
            "INCOMPLETE - MORE SOIL DATA REQUIRED"
            if missing else "ALL INPUTS PROVIDED - VALIDATION REQUIRED"
        )
    }