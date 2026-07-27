import tensorflow as tf

from tensorflow.keras.applications import EfficientNetB0

from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import GlobalAveragePooling2D

from tensorflow.keras.models import Model


def build_model(num_classes):

    base_model = EfficientNetB0(

        include_top=False,

        weights="imagenet",

        input_shape=(224,224,3)

    )

    base_model.trainable = False

    x = base_model.output

    x = GlobalAveragePooling2D()(x)

    x = Dropout(0.3)(x)

    x = Dense(

        256,

        activation="relu"

    )(x)

    output = Dense(

        num_classes,

        activation="softmax"

    )(x)

    model = Model(

        inputs=base_model.input,

        outputs=output

    )

    model.compile(

        optimizer="adam",

        loss="categorical_crossentropy",

        metrics=["accuracy"]

    )

    return model