import os

# ==========================================================
# BASE DIRECTORY
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ==========================================================
# STATIC FOLDER
# ==========================================================

STATIC_FOLDER = os.path.join(
    BASE_DIR,
    "static"
)


# ==========================================================
# UPLOAD / REPORT / MODEL FOLDERS
# ==========================================================

UPLOAD_FOLDER = os.path.join(
    STATIC_FOLDER,
    "uploads"
)

REPORT_FOLDER = os.path.join(
    STATIC_FOLDER,
    "reports"
)

MODEL_FOLDER = os.path.join(
    BASE_DIR,
    "models"
)


# ==========================================================
# CREATE REQUIRED DIRECTORIES
# ==========================================================

os.makedirs(
    STATIC_FOLDER,
    exist_ok=True
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)

os.makedirs(
    MODEL_FOLDER,
    exist_ok=True
)


# ==========================================================
# MODEL CONFIGURATION
# ==========================================================

MODEL_NAME = "skin_model.keras"

MODEL_PATH = os.path.join(
    MODEL_FOLDER,
    MODEL_NAME
)


# ==========================================================
# IMAGE CONFIGURATION
# ==========================================================

IMAGE_SIZE = (
    224,
    224
)

IMAGE_CHANNELS = 3


# ==========================================================
# UPLOAD CONFIGURATION
# ==========================================================

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}

MAX_CONTENT_LENGTH = (
    10 * 1024 * 1024
)


# ==========================================================
# PREDICTION CONFIGURATION
# ==========================================================

TOP_PREDICTIONS = 3

CONFIDENCE_THRESHOLD = 0.50


# ==========================================================
# FLASK CONFIGURATION
# ==========================================================

SECRET_KEY = "SkinAI2026"

DEBUG = True


# ==========================================================
# APPLICATION INFORMATION
# ==========================================================

APP_NAME = (
    "Skin Disease Classification "
    "& Stage Identification"
)

VERSION = "2.0"

AUTHOR = "Riya Kesharwani"


# ==========================================================
# MODEL CHECK
# ==========================================================

if os.path.exists(MODEL_PATH):

    print(
        "\n=========================================="
    )

    print(
        "AI MODEL FOUND"
    )

    print(
        "=========================================="
    )

    print(
        "Model:",
        MODEL_PATH
    )

else:

    print(
        "\n=========================================="
    )

    print(
        "WARNING: AI MODEL NOT FOUND!"
    )

    print(
        "Expected Model Path:"
    )

    print(
        MODEL_PATH
    )

    print(
        "=========================================="
    )