"""
GradCAM Service
---------------

Generates Grad-CAM explanations for
classification models:

- chest
- bone
- knee

Dental skipped (patch detector already localizes)
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


# ==========================================================
# DYNAMIC LAST CONV DISCOVERY
# ==========================================================

def find_last_conv_layer(
    model
):
    """
    Dynamically find last Conv2D layer.
    """

    for layer in reversed(
        model.layers
    ):

        if isinstance(
            layer,
            tf.keras.layers.Conv2D
        ):
            return layer.name

        if (
            hasattr(layer,"layers")
            and len(
                getattr(
                  layer,
                  "layers",
                  []
                )
            )>0
        ):

            for sublayer in reversed(
                layer.layers
            ):

                if isinstance(
                    sublayer,
                    tf.keras.layers.Conv2D
                ):
                    return sublayer.name

    raise ValueError(
      "No Conv2D layer found."
    )


# ==========================================================
# HEATMAP
# ==========================================================

def make_gradcam_heatmap(
    model,
    img_tensor
):
    """
    GradCAM for transfer-learning models
    with nested backbone support.
    """

    # your model has EfficientNet submodel
    base_model = model.get_layer(
        "efficientnetb0"
    )

    last_conv_name = find_last_conv_layer(
        base_model
    )

    last_conv_layer = base_model.get_layer(
        last_conv_name
    )

    # model that outputs:
    # conv maps + backbone features
    grad_model = tf.keras.models.Model(
        inputs=base_model.input,
        outputs=[
            last_conv_layer.output,
            base_model.output
        ]
    )

    with tf.GradientTape() as tape:

        conv_outputs, features = grad_model(
            img_tensor
        )

        # pass through your custom head
        x = features

        for layer in model.layers[2:]:
            x = layer(x)

        predictions = x

        pred_index = tf.argmax(
            predictions[0]
        )

        class_channel = predictions[
            :,
            pred_index
        ]

    grads = tape.gradient(
        class_channel,
        conv_outputs
    )

    pooled_grads = tf.reduce_mean(
        grads,
        axis=(0,1,2)
    )

    conv_outputs = conv_outputs[0]

    heatmap = tf.reduce_sum(
        conv_outputs * pooled_grads,
        axis=-1
    )

    heatmap = tf.maximum(
        heatmap,
        0
    )

    heatmap /= (
        tf.reduce_max(
           heatmap
        ) + 1e-8
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
    """
    Returns RGB numpy overlay.
    """

    if isinstance(
       original_img,
       Image.Image
    ):
        img = np.array(
            original_img
        )
    else:
        img = original_img

    heatmap = cv2.resize(
        heatmap,
        (
         img.shape[1],
         img.shape[0]
        )
    )

    heatmap = np.uint8(
       255 * heatmap
    )

    heatmap = cv2.applyColorMap(
       heatmap,
       cv2.COLORMAP_JET
    )

    overlay = (
       heatmap*alpha + img
    ).astype("uint8")

    return overlay


# ==========================================================
# BASE64 ENCODE
# ==========================================================

def image_to_base64(
    img_np
):
    img_pil = Image.fromarray(
        img_np
    )

    buffer = io.BytesIO()

    img_pil.save(
       buffer,
       format="PNG"
    )

    encoded = base64.b64encode(
        buffer.getvalue()
    ).decode()

    return encoded


# ==========================================================
# MODEL PICKER
# ==========================================================

def get_model_by_domain(
    domain
):
    if domain=="chest":
        return (
          ModelRegistry
          .get_chest_model()
        )

    if domain=="bone":
        return (
          ModelRegistry
          .get_bone_model()
        )

    if domain=="knee":
        return (
          ModelRegistry
          .get_knee_model()
        )

    return None


# ==========================================================
# MAIN SERVICE
# ==========================================================

def generate_gradcam(
    prepared_image,
    prediction_payload
):
    """
    Background worker task.

    Input:
      prepared image bundle
      prediction payload

    Returns:
      frontend artifact payload
    """

    domain = (
       prediction_payload[
         "domain"
       ]
    )

    if domain=="dental":

        return {
           "available":False,
           "reason":
             "Dental uses patch localization."
        }

    model = get_model_by_domain(
       domain
    )

    img_tensor = prepared_image[
       "tensors"
    ]["efficientnet"]

    original_image = prepared_image[
       "pil_image"
    ]

    heatmap = make_gradcam_heatmap(
       model,
       img_tensor
    )

    overlay = overlay_heatmap(
       original_image,
       heatmap
    )

    encoded = image_to_base64(
       overlay
    )

    return {

       "available":True,

       "image_base64":
           encoded,

       "type":"gradcam"
    }