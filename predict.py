import tensorflow as tf
import numpy as np

from config import MODEL_PATH
from utils.preprocess import preprocess_image

# =========================
# Load model only once
# =========================
model = tf.keras.models.load_model(MODEL_PATH, compile=False)

# =========================
# Class names
# =========================
class_names = [
    "akiec",
    "bcc",
    "bkl",
    "df",
    "mel",
    "nv",
    "vasc"
]
def predict(image_path):

    # preprocess image
    image = preprocess_image(image_path)

    # prediction
    prediction = model.predict(image, verbose=0)[0]

    # index
    index = int(np.argmax(prediction))

    # confidence in percentage
    confidence = float(prediction[index] * 100)

    return {
        "class": class_names[index],
        "confidence": round(confidence, 2),
        "all_predictions": prediction.tolist()
    }