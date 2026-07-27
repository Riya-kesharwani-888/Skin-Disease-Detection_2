# ============================================================
# SKIN DISEASE AI
# IMAGE PREPROCESSING
# Compatible with EfficientNetB0
# ============================================================

from PIL import Image
import numpy as np

from config import IMAGE_SIZE


# ============================================================
# PREPROCESS IMAGE FROM FILE PATH
# ============================================================

def preprocess_image(image_path):
    """
    Prepare an uploaded image for EfficientNetB0.

    Training pipeline:
        ImageDataGenerator
        target_size = (224, 224)
        No manual /255 normalization

    Output:
        NumPy array with shape:
        (1, 224, 224, 3)
    """

    try:

        # ----------------------------------------------------
        # OPEN IMAGE
        # ----------------------------------------------------

        image = Image.open(
            image_path
        )


        # ----------------------------------------------------
        # CONVERT TO RGB
        # ----------------------------------------------------

        image = image.convert(
            "RGB"
        )


        # ----------------------------------------------------
        # RESIZE
        # ----------------------------------------------------

        image = image.resize(
            IMAGE_SIZE,
            Image.Resampling.LANCZOS
        )


        # ----------------------------------------------------
        # CONVERT TO NUMPY
        # ----------------------------------------------------

        image_array = np.asarray(
            image,
            dtype=np.float32
        )


        # ----------------------------------------------------
        # SAFETY CHECK
        # ----------------------------------------------------

        if image_array.ndim != 3:

            raise ValueError(
                "Image must have 3 dimensions."
            )


        if image_array.shape[2] != 3:

            raise ValueError(
                "Image must have 3 RGB channels."
            )


        # ----------------------------------------------------
        # IMPORTANT
        # ----------------------------------------------------
        # DO NOT USE:
        #
        # image_array /= 255.0
        #
        # EfficientNetB0's preprocessing is handled
        # by the TensorFlow EfficientNet implementation.
        # ----------------------------------------------------


        # ----------------------------------------------------
        # ADD BATCH DIMENSION
        # ----------------------------------------------------

        image_array = np.expand_dims(
            image_array,
            axis=0
        )


        # ----------------------------------------------------
        # FINAL SHAPE CHECK
        # ----------------------------------------------------

        expected_shape = (
            1,
            IMAGE_SIZE[0],
            IMAGE_SIZE[1],
            3
        )


        if image_array.shape != expected_shape:

            raise ValueError(

                f"Invalid processed image shape: "
                f"{image_array.shape}. "

                f"Expected: "
                f"{expected_shape}"

            )


        return image_array


    except Exception as e:

        raise RuntimeError(

            f"Image preprocessing failed: {str(e)}"

        )


# ============================================================
# PREPROCESS EXISTING PIL IMAGE
# ============================================================

def preprocess_array(image):
    """
    Prepare an already-loaded PIL image.

    Output:
        NumPy array with shape:
        (1, 224, 224, 3)
    """

    try:

        # ----------------------------------------------------
        # CHECK INPUT
        # ----------------------------------------------------

        if image is None:

            raise ValueError(
                "No image was provided."
            )


        # ----------------------------------------------------
        # CONVERT TO RGB
        # ----------------------------------------------------

        image = image.convert(
            "RGB"
        )


        # ----------------------------------------------------
        # RESIZE
        # ----------------------------------------------------

        image = image.resize(
            IMAGE_SIZE,
            Image.Resampling.LANCZOS
        )


        # ----------------------------------------------------
        # NUMPY ARRAY
        # ----------------------------------------------------

        image_array = np.asarray(
            image,
            dtype=np.float32
        )


        # ----------------------------------------------------
        # CHANNEL CHECK
        # ----------------------------------------------------

        if image_array.ndim != 3:

            raise ValueError(
                "Image must have 3 dimensions."
            )


        if image_array.shape[2] != 3:

            raise ValueError(
                "Image must have 3 RGB channels."
            )


        # ----------------------------------------------------
        # NO /255 NORMALIZATION
        # ----------------------------------------------------

        image_array = np.expand_dims(
            image_array,
            axis=0
        )


        # ----------------------------------------------------
        # FINAL SHAPE CHECK
        # ----------------------------------------------------

        expected_shape = (
            1,
            IMAGE_SIZE[0],
            IMAGE_SIZE[1],
            3
        )


        if image_array.shape != expected_shape:

            raise ValueError(

                f"Invalid processed image shape: "
                f"{image_array.shape}. "

                f"Expected: "
                f"{expected_shape}"

            )


        return image_array


    except Exception as e:

        raise RuntimeError(

            f"Image array preprocessing failed: "
            f"{str(e)}"

        )


# ============================================================
# OPTIONAL HELPER
# ============================================================

def validate_image_array(image_array):
    """
    Validate a processed image before prediction.
    """

    if not isinstance(
        image_array,
        np.ndarray
    ):

        raise TypeError(
            "Image must be a NumPy array."
        )


    if image_array.ndim != 4:

        raise ValueError(

            f"Expected 4D input, "
            f"got {image_array.ndim}D."

        )


    if image_array.shape[0] != 1:

        raise ValueError(
            "Batch size must be 1."
        )


    if image_array.shape[1:] != (
        IMAGE_SIZE[0],
        IMAGE_SIZE[1],
        3
    ):

        raise ValueError(

            f"Invalid image shape: "
            f"{image_array.shape}"

        )


    return True