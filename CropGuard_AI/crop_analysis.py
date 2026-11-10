def analyse_tomato(readings):

    air = readings["Air Temperature"]
    humidity = readings["Humidity"]
    soil_temp = readings["Soil Temperature"]
    soil_moisture = readings["Soil Moisture"]

    results = []

    # Air temperature assessment
    if 20 <= air <= 28:
        results.append(("Air temperature", "FAVOURABLE",
                        "Within the preferred daytime range"))
    elif air > 35:
        results.append(("Air temperature", "HIGH STRESS",
                        "Temperature is very high"))
    else:
        results.append(("Air temperature", "CAUTION",
                        "Outside the preferred daytime range"))

    # Humidity assessment
    if 65 <= humidity <= 75:
        results.append(("Humidity", "FAVOURABLE",
                        "Within the preferred range"))
    elif humidity > 85:
        results.append(("Humidity", "WARNING",
                        "High humidity may affect pollination"))
    else:
        results.append(("Humidity", "CAUTION",
                        "Outside the preferred range"))

    # Soil readings are displayed, but need calibration
    results.append((
        "Soil temperature",
        "MONITORING",
        f"Measured value: {soil_temp} °C"
    ))

    results.append((
        "Soil moisture",
        "CALIBRATION NEEDED",
        f"Measured value: {soil_moisture}%"
    ))

    return results