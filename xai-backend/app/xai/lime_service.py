"""
LIME Service
------------

On-demand explanation generation.

User-triggered only.

Optimized for speed.
"""

import io
import base64

import numpy as np
from PIL import Image

from lime import lime_image

from skimage.segmentation import (
    mark_boundaries
)

from tensorflow.keras.applications.efficientnet import (
    preprocess_input
)

from app.core.model_registry import (
    ModelRegistry
)

from app.core.config import (
    LIME_NUM_SAMPLES,
    LIME_NUM_FEATURES,
    LIME_HIDE_COLOR,
    LIME_RESIZE
)


# =========================================================
# GLOBAL EXPLAINER
# =========================================================

explainer = (
    lime_image
    .LimeImageExplainer()
)


# =========================================================
# PREDICTION FUNCTION FOR LIME
# =========================================================

def predict_fn(
    images
):
    """
    LIME prediction wrapper.
    Uses correct domain model.
    """

    global _lime_model

    imgs = images.astype(
        np.float32
    )

    imgs_pp = preprocess_input(
        imgs
    )

    preds = _lime_model.predict(
        imgs_pp,
        verbose=0
    )

    return preds


# =========================================================
# BASE64
# =========================================================

def image_to_base64(
    img_np
):
    img_np = (
       img_np*255
    ).astype(
       np.uint8
    )

    img = Image.fromarray(
       img_np
    )

    buf = io.BytesIO()

    img.save(
      buf,
      format="PNG"
    )

    return base64.b64encode(
      buf.getvalue()
    ).decode()


# =========================================================
# MODEL PICKER
# =========================================================

def get_domain_model(
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

    raise ValueError(
      "LIME unsupported for domain"
    )


# =========================================================
# MAIN SERVICE
# =========================================================

def generate_lime(
    prepared_image,
    prediction_payload
):
    """
    On-demand LIME worker.
    """

    global _lime_model

    domain = prediction_payload[
        "domain"
    ]

    if domain=="dental":

        return {
          "available":False,
          "reason":
            "LIME disabled for dental."
        }

    _lime_model = get_domain_model(
       domain
    )

    # lighter image for speed
    img_np = prepared_image[
        "image_np"
    ]

    img_small = np.array(
       Image.fromarray(
          img_np.astype(
             np.uint8
          )
       ).resize(
          (
            LIME_RESIZE,
            LIME_RESIZE
          )
       )
    ).astype("double")


    explanation = (
      explainer.explain_instance(
          img_small,

          predict_fn,

          top_labels=1,

          hide_color=
              LIME_HIDE_COLOR,

          num_samples=
              LIME_NUM_SAMPLES
      )
    )

    top_label = (
      explanation.top_labels[0]
    )

    temp,mask = (
       explanation
       .get_image_and_mask(

          top_label,

          positive_only=True,

          num_features=
              LIME_NUM_FEATURES,

          hide_rest=False
       )
    )

    lime_img = mark_boundaries(
        temp.astype(
          "uint8"
        )/255.0,
        mask
    )

    encoded = image_to_base64(
        lime_img
    )

    return {

       "available":True,

       "image_base64":
           encoded,

       "type":"lime"
    }