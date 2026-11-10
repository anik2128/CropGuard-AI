# CropGuard AI - Crop Suitability Engine
# Preliminary rule-based demonstration

CROP_DATABASE = {

    "rice": {
        "ph_min": 5.0,
        "ph_max": 7.0
    },

    "wheat": {
        "ph_min": 6.0,
        "ph_max": 7.5
    },

    "maize": {
        "ph_min": 5.5,
        "ph_max": 7.5
    },

    "potato": {
        "ph_min": 5.0,
        "ph_max": 6.5
    },

    "tomato": {
        "ph_min": 5.5,
        "ph_max": 7.0
    },

    "mustard": {
        "ph_min": 6.0,
        "ph_max": 7.5
    }
}


def analyse_crop_suitability(crop_name, soil_data):

    if not crop_name or not crop_name.strip():

        return {
            "crop": "NOT SELECTED",
            "status": "GENERAL SOIL ASSESSMENT",
            "reason": "No crop name was provided."
        }

    crop_name = crop_name.strip().lower()

    if crop_name not in CROP_DATABASE:

        return {
            "crop": crop_name.title(),
            "status": "CROP NOT IN DATABASE",
            "reason": "No reference profile is available."
        }

    ph = soil_data.get("pH")

    if ph is None:
        return {
            "crop": crop_name.title(),
            "status": "INSUFFICIENT DATA",
            "reason": "Soil pH is required for comparison."
        }

    try:
        ph = float(ph)
    except (TypeError, ValueError):
        return {
            "crop": crop_name.title(),
            "status": "INVALID DATA",
            "reason": "Soil pH must be numeric."
        }

    if not 0 <= ph <= 14:
        return {
            "crop": crop_name.title(),
            "status": "INVALID DATA",
            "reason": "Soil pH must be between 0 and 14."
        }

    profile = CROP_DATABASE[crop_name]

    if profile["ph_min"] <= ph <= profile["ph_max"]:

        status = "PRELIMINARY PH MATCH"
        reason = "Soil pH falls within the demo reference range."

    else:

        status = "PH OUTSIDE REFERENCE RANGE"
        reason = "Soil pH falls outside the demo reference range."

    return {
        "crop": crop_name.title(),
        "status": status,
        "reason": reason,
        "reference_range": (
            f"{profile['ph_min']} - {profile['ph_max']}"
        ),
        "measured_ph": ph
    }