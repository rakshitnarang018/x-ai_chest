"""
GradCAM Service
Cleaned + fixed input handling
"""

import io
import base64
import cv2
import numpy as np
import tensorflow as tf

from PIL import Image

from app.core.model_registry import (
    ModelRegistry
)

from app.core.config import (
    GRADCAM_ALPHA
)

from tensorflow.keras.applications.mobilenet_v2 import (
    preprocess_input as mobilenet_preprocess
)



# ==========================================================
# FIND LAST CONV
# ==========================================================

def find_last_conv_layer(
    model
):
    for layer in reversed(
        model.layers
    ):

        if isinstance(
            layer,
            tf.keras.layers.Conv2D
        ):
            return layer.name

        if hasattr(
            layer,
            "layers"
        ):

            for sub in reversed(
                getattr(
                    layer,
                    "layers",
                    []
                )
            ):
                if isinstance(
                    sub,
                    tf.keras.layers.Conv2D
                ):
                    return sub.name

    raise ValueError(
      "No Conv layer found"
    )



# ==========================================================
# GRADCAM
# ==========================================================

def make_gradcam_heatmap(
    model,
    img_tensor
):

    try:

        # transfer-learning models
        base_model=model.get_layer(
            "efficientnetb0"
        )

        last_conv_name=(
            find_last_conv_layer(
                base_model
            )
        )

        grad_model=tf.keras.models.Model(
            inputs=base_model.input,
            outputs=[
                base_model.get_layer(
                    last_conv_name
                ).output,
                base_model.output
            ]
        )


        with tf.GradientTape() as tape:

            conv_outputs,features=(
                grad_model(
                    img_tensor,
                    training=False
                )
            )

            x=features

            for layer in model.layers[2:]:
                x=layer(
                   x,
                   training=False
                )

            predictions=x

            pred_index=tf.argmax(
                predictions[0]
            )

            class_channel=predictions[
                :,
                pred_index
            ]

        grads=tape.gradient(
            class_channel,
            conv_outputs
        )


    except Exception:

        # generic fallback (dental etc)

        last_conv_name=(
            find_last_conv_layer(
                model
            )
        )

        grad_model=tf.keras.models.Model(
            inputs=model.inputs,
            outputs=[
                model.get_layer(
                    last_conv_name
                ).output,
                model.output
            ]
        )


        with tf.GradientTape() as tape:

            conv_outputs,preds=(
                grad_model(
                    img_tensor,
                    training=False
                )
            )

            pred_index=tf.argmax(
                preds[0]
            )

            class_channel=preds[
                :,
                pred_index
            ]

        grads=tape.gradient(
            class_channel,
            conv_outputs
        )


    pooled_grads=tf.reduce_mean(
        grads,
        axis=(0,1,2)
    )

    conv_outputs=conv_outputs[0]

    heatmap=tf.reduce_sum(
        conv_outputs*pooled_grads,
        axis=-1
    )

    heatmap=tf.maximum(
        heatmap,
        0
    )

    heatmap/=(
        tf.reduce_max(
            heatmap
        )+1e-8
    )

    return heatmap.numpy()



# ==========================================================
# OVERLAY
# ==========================================================

def overlay_heatmap(
    original_img,
    heatmap,
    alpha=GRADCAM_ALPHA
):

    if isinstance(
        original_img,
        Image.Image
    ):
        img=np.array(
            original_img
        )
    else:
        img=original_img

    heatmap=cv2.resize(
        heatmap,
        (
            img.shape[1],
            img.shape[0]
        )
    )

    heatmap=np.uint8(
       255*heatmap
    )

    heatmap=cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    overlay=(
       heatmap*alpha + img
    ).astype(
       "uint8"
    )

    return overlay



# ==========================================================
# BASE64
# ==========================================================

def image_to_base64(
    img_np
):
    img_pil=Image.fromarray(
        img_np
    )

    buffer=io.BytesIO()

    img_pil.save(
       buffer,
       format="PNG"
    )

    return base64.b64encode(
       buffer.getvalue()
    ).decode()



# ==========================================================
# MODEL PICKER
# ==========================================================

def get_model_by_domain(
    domain
):
    if domain=="chest":
        return ModelRegistry.get_chest_model()

    if domain=="bone":
        return ModelRegistry.get_bone_model()

    if domain=="knee":
        return ModelRegistry.get_knee_model()

    if domain=="dental":
        return ModelRegistry.get_dental_model()

    return None



# ==========================================================
# DENTAL TENSOR FIX
# ==========================================================

def get_dental_tensor(
    pil_image
):
    img=pil_image.resize(
        (224,224)
    )

    img=np.asarray(
        img,
        dtype=np.float32
    )

    img=np.expand_dims(
        img,
        axis=0
    )

    return mobilenet_preprocess(
        img
    )



# ==========================================================
# MAIN
# ==========================================================

def generate_gradcam(
    prepared_image,
    prediction_payload
):

    domain=prediction_payload[
        "domain"
    ]

    model=get_model_by_domain(
        domain
    )

    if model is None:
        return {
            "available":False
        }


    # important fix:
    if domain=="dental":

        img_tensor=get_dental_tensor(
            prepared_image[
               "pil_image"
            ]
        )

    else:

        img_tensor=prepared_image[
           "tensors"
        ]["efficientnet"]


    heatmap=make_gradcam_heatmap(
        model,
        img_tensor
    )

    overlay=overlay_heatmap(
        prepared_image[
          "pil_image"
        ],
        heatmap
    )

    encoded=image_to_base64(
        overlay
    )

    return {
        "available":True,
        "image_base64":encoded,
        "type":"gradcam"
    }