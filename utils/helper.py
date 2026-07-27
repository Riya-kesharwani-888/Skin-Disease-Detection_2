from config import ALLOWED_EXTENSIONS


# ==========================================================
# Check Allowed File Extension
# ==========================================================

def allowed_file(filename):
    """
    Check whether uploaded file has a valid image extension.
    """

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS


# ==========================================================
# Format Confidence
# ==========================================================

def format_confidence(confidence):
    """
    Convert confidence into percentage with 2 decimal places.
    """

    return round(float(confidence), 2)


# ==========================================================
# Risk Level
# ==========================================================

def get_risk_level(disease):

    """
    Estimate disease risk based on predicted disease class.
    This is NOT a medical diagnosis.
    """

    HIGH_RISK = {
        "mel",      # Melanoma
        "bcc",      # Basal Cell Carcinoma
        "akiec"     # Actinic Keratoses
    }

    MEDIUM_RISK = {
        "bkl"
    }

    LOW_RISK = {
        "nv",
        "df",
        "vasc"
    }

    if disease in HIGH_RISK:
        return "High Risk"

    elif disease in MEDIUM_RISK:
        return "Medium Risk"

    elif disease in LOW_RISK:
        return "Low Risk"

    return "Unknown"


# ==========================================================
# Stage Information
# ==========================================================

def get_stage(disease):

    """
    HAM10000 dataset does not contain stage labels.

    Therefore stage prediction is not possible.
    """

    return "Not Available"


# ==========================================================
# Disease Description
# ==========================================================

def get_short_description(disease):

    descriptions = {

        "akiec": "Actinic Keratoses is a precancerous skin lesion caused by long-term sun exposure.",

        "bcc": "Basal Cell Carcinoma is the most common type of skin cancer.",

        "bkl": "Benign Keratosis is a non-cancerous skin lesion.",

        "df": "Dermatofibroma is a harmless fibrous skin growth.",

        "mel": "Melanoma is an aggressive type of skin cancer requiring urgent medical evaluation.",

        "nv": "Melanocytic Nevus is a common mole that is usually harmless.",

        "vasc": "Vascular lesions are abnormalities of blood vessels in the skin."

    }

    return descriptions.get(disease, "No description available.")