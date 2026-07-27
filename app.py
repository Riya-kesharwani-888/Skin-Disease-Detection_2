# ============================================================
# SKIN DISEASE CLASSIFICATION & STAGE IDENTIFICATION
# FINAL IMPROVED app.py
# ============================================================

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_file,
    url_for
)

import tensorflow as tf
import numpy as np
import os
import uuid
import json

from datetime import datetime
from werkzeug.utils import secure_filename
from reportlab.pdfgen import canvas

from config import (
    MODEL_PATH,
    UPLOAD_FOLDER,
    IMAGE_SIZE,
    ALLOWED_EXTENSIONS
)

from utils.preprocess import (
    preprocess_image,
    validate_image_array
)


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MAX_CONTENT_LENGTH"] = (
    10 * 1024 * 1024
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ============================================================
# CLASS MAPPING
# IMPORTANT:
# This MUST come from train.py
# ============================================================

CLASS_NAMES_PATH = os.path.join(
    "models",
    "class_names.json"
)


print("=" * 65)
print("Loading Skin Disease AI System")
print("=" * 65)


# ============================================================
# LOAD CLASS NAMES
# ============================================================

if not os.path.exists(
    CLASS_NAMES_PATH
):

    raise FileNotFoundError(

        "\nCLASS MAPPING FILE NOT FOUND!\n"
        f"Expected location:\n{CLASS_NAMES_PATH}\n\n"
        "Please run train.py first."

    )


try:

    with open(
        CLASS_NAMES_PATH,
        "r"
    ) as file:

        CLASSES = json.load(
            file
        )


except Exception as e:

    raise RuntimeError(

        "Unable to load class_names.json: "
        + str(e)

    )


if not isinstance(
    CLASSES,
    list
):

    raise ValueError(
        "class_names.json must contain a list."
    )


print(
    "\nLoaded Classes:"
)

for index, class_name in enumerate(
    CLASSES
):

    print(
        f"{index} -> {class_name}"
    )


# ============================================================
# DISEASE INFORMATION
# ============================================================

DISEASE_INFO = {

    "akiec": {

        "name":
            "Actinic Keratoses",

        "description":
            (
                "Actinic Keratoses is a precancerous "
                "skin condition often associated with "
                "long-term ultraviolet exposure."
            ),

        "symptoms":
            (
                "Rough or scaly skin patches, redness, "
                "dryness and changes in skin texture."
            ),

        "precautions":
            (
                "Use broad-spectrum sunscreen, limit "
                "excessive sun exposure and consult a "
                "dermatologist for evaluation."
            )
    },


    "bcc": {

        "name":
            "Basal Cell Carcinoma",

        "description":
            (
                "Basal Cell Carcinoma is a common form "
                "of skin cancer that develops from "
                "basal cells."
            ),

        "symptoms":
            (
                "A shiny bump, persistent sore, bleeding "
                "area or a non-healing skin lesion."
            ),

        "precautions":
            (
                "Avoid excessive sun exposure and seek "
                "professional dermatological evaluation "
                "for suspicious lesions."
            )
    },


    "bkl": {

        "name":
            "Benign Keratosis",

        "description":
            (
                "Benign Keratosis refers to a group of "
                "non-cancerous skin growths that may "
                "appear with age."
            ),

        "symptoms":
            (
                "Brown, black or skin-colored raised "
                "patches with a rough or waxy appearance."
            ),

        "precautions":
            (
                "Monitor changes in size, color or shape "
                "and consult a dermatologist if the "
                "lesion changes."
            )
    },


    "df": {

        "name":
            "Dermatofibroma",

        "description":
            (
                "Dermatofibroma is generally a harmless "
                "fibrous skin growth."
            ),

        "symptoms":
            (
                "Small firm bumps that may appear on "
                "the legs or other areas of the skin."
            ),

        "precautions":
            (
                "Avoid scratching the area and consult "
                "a doctor if the lesion changes or "
                "becomes painful."
            )
    },


    "mel": {

        "name":
            "Melanoma",

        "description":
            (
                "Melanoma is a serious skin cancer "
                "involving melanocytes, the cells "
                "responsible for skin pigment."
            ),

        "symptoms":
            (
                "Changes in mole size, shape, color or "
                "border; new unusual lesions; itching "
                "or bleeding."
            ),

        "precautions":
            (
                "Seek prompt professional dermatological "
                "evaluation for suspicious or changing "
                "lesions."
            )
    },


    "nv": {

        "name":
            "Melanocytic Nevus",

        "description":
            (
                "Melanocytic Nevus is a common type "
                "of mole that is often benign."
            ),

        "symptoms":
            (
                "Small pigmented spots or moles that "
                "may vary in color, size and shape."
            ),

        "precautions":
            (
                "Monitor unusual changes in existing "
                "moles and consult a dermatologist "
                "when concerned."
            )
    },


    "vasc": {

        "name":
            "Vascular Lesion",

        "description":
            (
                "Vascular lesions are skin abnormalities "
                "associated with blood vessels."
            ),

        "symptoms":
            (
                "Red, purple or bluish marks that may "
                "vary in size and appearance."
            ),

        "precautions":
            (
                "Consult a dermatologist if the lesion "
                "grows, bleeds or changes significantly."
            )
    }

}


# ============================================================
# CHECK CLASS INFORMATION
# ============================================================

for class_name in CLASSES:

    if class_name not in DISEASE_INFO:

        raise ValueError(

            f"Unknown class '{class_name}' found "
            "in class_names.json."

        )


# ============================================================
# MODEL LOADING
# ============================================================

if not os.path.exists(
    MODEL_PATH
):

    raise FileNotFoundError(

        "\nMODEL FILE NOT FOUND!\n"
        f"Expected location:\n{MODEL_PATH}\n\n"
        "Please run train.py first."

    )


try:

    model = tf.keras.models.load_model(

        MODEL_PATH,

        compile=False

    )

    print("\nModel Loaded Successfully!")

    print(
        "Model Input Shape :",
        model.input_shape
    )

    print(
        "Model Output Shape:",
        model.output_shape
    )


except Exception as e:

    print(
        "\nMODEL LOADING ERROR:"
    )

    print(e)

    raise


# ============================================================
# MODEL OUTPUT CHECK
# ============================================================

try:

    model_output_count = int(
        model.output_shape[-1]
    )

except Exception:

    raise RuntimeError(
        "Unable to determine model output size."
    )


if model_output_count != len(
    CLASSES
):

    raise ValueError(

        "MODEL / CLASS MAPPING MISMATCH!\n"

        f"Model outputs : {model_output_count}\n"

        f"Classes loaded: {len(CLASSES)}\n\n"

        "Please train the model again."

    )


# ============================================================
# FILE VALIDATION
# ============================================================

def check_file(filename):

    if not filename:

        return False


    if "." not in filename:

        return False


    extension = filename.rsplit(
        ".",
        1
    )[1].lower()


    return (
        extension
        in ALLOWED_EXTENSIONS
    )


# ============================================================
# IMAGE PREPARATION
# ============================================================

def prepare_image(
    image_path
):

    image = preprocess_image(
        image_path
    )


    image = np.asarray(
        image,
        dtype=np.float32
    )


    validate_image_array(
        image
    )


    return image


# ============================================================
# RISK INDICATOR
# ============================================================

def get_risk_stage(
    disease_class,
    confidence
):

    confidence = float(
        confidence
    )


    # --------------------------------------------------------
    # NOTE:
    # This is only a PROJECT AI RISK INDICATOR.
    # It is NOT medical cancer staging.
    # --------------------------------------------------------

    if disease_class == "mel":

        if confidence >= 90:

            return (
                "High",
                "Stage 4"
            )

        elif confidence >= 75:

            return (
                "High",
                "Stage 3"
            )

        elif confidence >= 60:

            return (
                "Moderate",
                "Stage 2"
            )

        else:

            return (
                "Low",
                "Stage 1"
            )


    if disease_class == "bcc":

        if confidence >= 90:

            return (
                "High",
                "Stage 3"
            )

        elif confidence >= 75:

            return (
                "Moderate",
                "Stage 2"
            )

        else:

            return (
                "Low",
                "Stage 1"
            )


    if disease_class == "akiec":

        if confidence >= 80:

            return (
                "Moderate",
                "Stage 2"
            )

        return (
            "Low",
            "Stage 1"
        )


    return (
        "Low",
        "Stage 1"
    )


# ============================================================
# PREDICTION
# ============================================================

def predict_disease(
    image_path
):

    # --------------------------------------------------------
    # PREPARE IMAGE
    # --------------------------------------------------------

    image = prepare_image(
        image_path
    )


    print(
        "Image shape sent to model:",
        image.shape
    )


    # --------------------------------------------------------
    # MODEL PREDICTION
    # --------------------------------------------------------

    raw_prediction = model.predict(

        image,

        verbose=0

    )


    prediction = np.asarray(
        raw_prediction,
        dtype=np.float32
    )


    # --------------------------------------------------------
    # REMOVE BATCH DIMENSION
    # --------------------------------------------------------

    if prediction.ndim == 2:

        prediction = prediction[0]


    else:

        prediction = np.squeeze(
            prediction
        )


    # --------------------------------------------------------
    # VALIDATE OUTPUT
    # --------------------------------------------------------

    if prediction.ndim != 1:

        raise ValueError(

            "Unexpected model prediction shape: "
            f"{prediction.shape}"

        )


    if len(prediction) != len(
        CLASSES
    ):

        raise ValueError(

            "Model output does not match "
            "class count.\n"

            f"Received: {len(prediction)}\n"

            f"Expected: {len(CLASSES)}"

        )


    # --------------------------------------------------------
    # SAFE PROBABILITY HANDLING
    # --------------------------------------------------------

    prediction_sum = float(
        np.sum(prediction)
    )


    # If model output isn't probability-like,
    # convert using softmax.

    if (

        np.any(
            prediction < 0
        )

        or

        not np.isclose(
            prediction_sum,
            1.0,
            atol=0.05
        )

    ):

        prediction = (
            tf.nn.softmax(
                prediction
            ).numpy()
        )


    # --------------------------------------------------------
    # REMOVE NUMERICAL ISSUES
    # --------------------------------------------------------

    prediction = np.nan_to_num(

        prediction,

        nan=0.0,

        posinf=0.0,

        neginf=0.0

    )


    # Re-normalize

    total = float(
        np.sum(prediction)
    )


    if total <= 0:

        raise ValueError(
            "Model returned invalid probabilities."
        )


    prediction = (
        prediction / total
    )


    # ========================================================
    # BEST PREDICTION
    # ========================================================

    best_index = int(
        np.argmax(prediction)
    )


    confidence = float(

        prediction[
            best_index
        ] * 100

    )


    disease_class = CLASSES[
        best_index
    ]


    details = DISEASE_INFO[
        disease_class
    ]


    # ========================================================
    # TOP 3 PREDICTIONS
    # ========================================================

    top_indexes = np.argsort(

        prediction

    )[::-1][:3]


    top_predictions = []


    for rank, index in enumerate(

        top_indexes,

        start=1

    ):

        index = int(
            index
        )


        class_code = CLASSES[
            index
        ]


        top_predictions.append({

            "rank":
                rank,

            "class":
                class_code,

            "name":
                DISEASE_INFO[
                    class_code
                ]["name"],

            "confidence":
                round(

                    float(
                        prediction[index]
                        * 100
                    ),

                    2

                )

        })


    # ========================================================
    # RISK
    # ========================================================

    risk, stage = get_risk_stage(

        disease_class,

        confidence

    )


    # ========================================================
    # RESULT
    # ========================================================

    return {

        "class":
            disease_class,

        "name":
            details["name"],

        "description":
            details["description"],

        "symptoms":
            details["symptoms"],

        "precautions":
            details["precautions"],

        "confidence":
            round(
                confidence,
                2
            ),

        "risk":
            risk,

        "stage":
            stage,

        "risk_percentage":
            round(
                confidence,
                2
            ),

        "safe_percentage":
            round(
                max(
                    0,
                    100 - confidence
                ),
                2
            ),

        "top_predictions":
            top_predictions

    }


# ============================================================
# RECOMMENDATION
# ============================================================

def get_recommendation(
    result
):

    disease = result[
        "name"
    ]

    confidence = result[
        "confidence"
    ]

    risk = result[
        "risk"
    ]


    if risk == "High":

        return (

            f"The AI model predicted "
            f"{disease} with "
            f"{confidence:.2f}% confidence. "

            "This is a project-level AI risk indicator "
            "and is not a medical diagnosis. "

            "Professional dermatological evaluation "
            "is recommended, especially for a suspicious "
            "or changing lesion."

        )


    if risk == "Moderate":

        return (

            f"The AI model predicted "
            f"{disease} with "
            f"{confidence:.2f}% confidence. "

            "This is an AI-based project prediction, "
            "not a confirmed diagnosis. "

            "Consider professional dermatological "
            "evaluation if the lesion is persistent "
            "or changing."

        )


    return (

        f"The AI model predicted "
        f"{disease} with "
        f"{confidence:.2f}% confidence. "

        "This AI result is for educational and "
        "research purposes and should not replace "
        "professional medical examination."

    )


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# PREDICTION ROUTE
# ============================================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    try:

        # ----------------------------------------------------
        # CHECK FILE
        # ----------------------------------------------------

        if "image" not in request.files:

            return jsonify({

                "success":
                    False,

                "error":
                    "No image uploaded."

            }), 400


        file = request.files[
            "image"
        ]


        if (

            not file

            or

            file.filename == ""

        ):

            return jsonify({

                "success":
                    False,

                "error":
                    "Please select an image."

            }), 400


        if not check_file(
            file.filename
        ):

            return jsonify({

                "success":
                    False,

                "error":
                    (
                        "Invalid image format. "
                        "Use JPG, JPEG, PNG or WEBP."
                    )

            }), 400


        # ----------------------------------------------------
        # SAVE IMAGE
        # ----------------------------------------------------

        original_name = secure_filename(
            file.filename
        )


        unique_name = (

            uuid.uuid4().hex

            + "_"

            + original_name

        )


        image_path = os.path.join(

            UPLOAD_FOLDER,

            unique_name

        )


        file.save(
            image_path
        )


        print(
            "\nImage saved:",
            image_path
        )


        # ----------------------------------------------------
        # PREDICT
        # ----------------------------------------------------

        result = predict_disease(
            image_path
        )


        print(
            "\nPrediction:",
            result["name"]
        )

        print(
            "Confidence:",
            result["confidence"],
            "%"
        )

        print(
            "Top predictions:",
            result["top_predictions"]
        )


        # ----------------------------------------------------
        # REPORT ID
        # ----------------------------------------------------

        report_id = (

            "SKIN-"

            + datetime.now().strftime(
                "%Y%m%d"
            )

            + "-"

            + uuid.uuid4().hex[:6]

        ).upper()


        # ----------------------------------------------------
        # ANALYSIS TIME
        # ----------------------------------------------------

        analysis_time = (

            datetime.now().strftime(

                "%d %B %Y, %I:%M %p"

            )

        )


        # ----------------------------------------------------
        # IMAGE URL
        # ----------------------------------------------------

        image_url = url_for(

            "uploaded_file",

            filename=unique_name

        )


        # ----------------------------------------------------
        # RECOMMENDATION
        # ----------------------------------------------------

        recommendation = (
            get_recommendation(
                result
            )
        )


        # ----------------------------------------------------
        # RESULT PAGE
        # ----------------------------------------------------

        return render_template(

            "result.html",

            result=result,

            image_name=unique_name,

            image_url=image_url,

            report_id=report_id,

            analysis_time=analysis_time,

            disease=result["name"],

            disease_name=result["name"],

            confidence=result["confidence"],

            confidence_score=result["confidence"],

            risk=result["risk"],

            risk_level=result["risk"],

            stage=result["stage"],

            description=result["description"],

            disease_description=result["description"],

            symptoms=result["symptoms"],

            precautions=result["precautions"],

            recommendation=recommendation,

            top_predictions=result[
                "top_predictions"
            ],

            predictions=result[
                "top_predictions"
            ],

            risk_percentage=result[
                "risk_percentage"
            ],

            safe_percentage=result[
                "safe_percentage"
            ]

        )


    except Exception as e:

        print("\n")
        print("=" * 65)
        print("PREDICTION ERROR")
        print("=" * 65)
        print(str(e))
        print("=" * 65)


        return jsonify({

            "success":
                False,

            "error":
                (
                    "Prediction failed: "
                    + str(e)
                )

        }), 500


# ============================================================
# CHATBOT API
# ============================================================

@app.route(
    "/chat",
    methods=["POST"]
)
def chat():

    try:

        data = request.get_json(
            silent=True
        ) or {}


        message = str(

            data.get(
                "message",
                ""
            )

        ).strip().lower()


        if not message:

            return jsonify({

                "success":
                    False,

                "reply":
                    "Please describe your symptoms first."

            })


        responses = []


        # ----------------------------------------------------
        # PAIN
        # ----------------------------------------------------

        if any(

            word in message

            for word in [

                "pain",
                "dard"

            ]

        ):

            responses.append(

                "Pain can be relevant when describing "
                "a skin lesion."

            )


        # ----------------------------------------------------
        # ITCHING
        # ----------------------------------------------------

        if any(

            word in message

            for word in [

                "itch",
                "itching",
                "khujli"

            ]

        ):

            responses.append(

                "Please note when the itching started "
                "and whether it is getting worse."

            )


        # ----------------------------------------------------
        # SWELLING
        # ----------------------------------------------------

        if any(

            word in message

            for word in [

                "swelling",
                "swollen",
                "sujan"

            ]

        ):

            responses.append(

                "Please monitor whether the swelling "
                "is increasing."

            )


        # ----------------------------------------------------
        # BLEEDING
        # ----------------------------------------------------

        if any(

            word in message

            for word in [

                "bleeding",
                "blood",
                "bleed",
                "khoon"

            ]

        ):

            responses.append(

                "Bleeding from a skin lesion should "
                "be evaluated by a healthcare professional."

            )


        # ----------------------------------------------------
        # REDNESS
        # ----------------------------------------------------

        if any(

            word in message

            for word in [

                "redness",
                "red",
                "lal"

            ]

        ):

            responses.append(

                "Please monitor changes in redness, "
                "size and appearance."

            )


        # ----------------------------------------------------
        # BURNING
        # ----------------------------------------------------

        if any(

            word in message

            for word in [

                "burning",
                "jalna"

            ]

        ):

            responses.append(

                "Please mention how long the burning "
                "sensation has been present."

            )


        # ----------------------------------------------------
        # DURATION
        # ----------------------------------------------------

        if any(

            word in message

            for word in [

                "how long",
                "since",
                "kab se"

            ]

        ):

            responses.append(

                "Knowing how long the symptom has been "
                "present can help describe the condition "
                "to a dermatologist."

            )


        # ----------------------------------------------------
        # DEFAULT
        # ----------------------------------------------------

        if not responses:

            responses.append(

                "Please tell me whether you have pain, "
                "itching, swelling, bleeding, burning, "
                "redness, or any recent change in the lesion."

            )


        responses.append(

            "This assistant provides general information "
            "only and does not replace professional "
            "medical examination."

        )


        return jsonify({

            "success":
                True,

            "reply":
                " ".join(
                    responses
                )

        })


    except Exception:

        return jsonify({

            "success":
                False,

            "reply":
                "Sorry, I could not process that message."

        }), 500


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route(
    "/health"
)
def health():

    return jsonify({

        "status":
            "Skin Disease AI Server Running",

        "model":
            "Loaded",

        "classes":
            len(CLASSES),

        "class_names":
            CLASSES

    })


# ============================================================
# PDF GENERATION
# ============================================================

def generate_pdf(
    data
):

    filename = (

        "Skin_AI_Report_"

        + uuid.uuid4().hex[:8]

        + ".pdf"

    )


    report_path = os.path.join(

        UPLOAD_FOLDER,

        filename

    )


    pdf = canvas.Canvas(
        report_path
    )


    pdf.setTitle(
        "Skin Disease AI Report"
    )


    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    pdf.setFont(

        "Helvetica-Bold",

        18

    )


    pdf.drawString(

        40,

        800,

        "Skin Disease Classification & Stage Identification"

    )


    pdf.setFont(

        "Helvetica",

        10

    )


    pdf.drawString(

        40,

        782,

        "Artificial Intelligence Based Skin Image Analysis Report"

    )


    y = 745


    result = data.get(

        "result",

        {}

    )


    lines = [

        f"Report ID: {data.get('report_id', 'N/A')}",

        f"Analysis Time: {data.get('analysis_time', 'N/A')}",

        "",

        f"Disease Prediction: {result.get('name', 'N/A')}",

        f"AI Confidence: {result.get('confidence', 'N/A')}%",

        f"AI Risk Indicator: {result.get('risk', 'N/A')}",

        f"AI Severity Indicator: {result.get('stage', 'N/A')}",

        "",

        "Description:",

        result.get(
            "description",
            "N/A"
        ),

        "",

        "Symptoms:",

        result.get(
            "symptoms",
            "N/A"
        ),

        "",

        "Precautions:",

        result.get(
            "precautions",
            "N/A"
        ),

        "",

        "Important Notice:",

        (
            "This AI output is for educational and "
            "research purposes only and should not "
            "be considered a medical diagnosis."
        )

    ]


    # --------------------------------------------------------
    # WRITE PDF
    # --------------------------------------------------------

    for text in lines:

        text = str(
            text
        )


        words = text.split()

        current = ""


        for word in words:

            test = (

                current

                + " "

                + word

            ).strip()


            if len(test) > 92:

                pdf.drawString(

                    40,

                    y,

                    current

                )


                y -= 17


                current = word


            else:

                current = test


        if current:

            pdf.drawString(

                40,

                y,

                current

            )


            y -= 23


        if y < 60:

            pdf.showPage()

            pdf.setFont(

                "Helvetica",

                10

            )

            y = 800


    pdf.save()


    return filename


# ============================================================
# DOWNLOAD PDF
# ============================================================

@app.route(
    "/download_report",
    methods=["POST"]
)
def download_report():

    try:

        data = request.get_json(
            silent=True
        )


        if not data:

            return jsonify({

                "error":
                    "No report data received."

            }), 400


        filename = generate_pdf(
            data
        )


        path = os.path.join(

            UPLOAD_FOLDER,

            filename

        )


        return send_file(

            path,

            as_attachment=True,

            download_name=filename,

            mimetype="application/pdf"

        )


    except Exception as e:

        return jsonify({

            "error":
                (
                    "PDF generation failed: "
                    + str(e)
                )

        }), 500


# ============================================================
# UPLOADED IMAGE
# ============================================================

@app.route(
    "/uploads/<filename>"
)
def uploaded_file(
    filename
):

    filepath = os.path.join(

        UPLOAD_FOLDER,

        filename

    )


    if not os.path.exists(
        filepath
    ):

        return jsonify({

            "error":
                "Image not found."

        }), 404


    return send_file(
        filepath
    )


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(
    error
):

    return render_template(
        "404.html"
    ), 404


@app.errorhandler(500)
def server_error(
    error
):

    return jsonify({

        "success":
            False,

        "error":
            "Internal Server Error"

    }), 500


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    print("""

============================================================
 Skin Disease Classification & Stage Identification
============================================================

 Server:
 http://127.0.0.1:5000

 Health:
 http://127.0.0.1:5000/health

 Model:
 EfficientNetB0

============================================================

""")

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )