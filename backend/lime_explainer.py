import numpy as np
import tensorflow as tf
from lime import lime_image
from skimage.segmentation import mark_boundaries

from model_loader import predict_fn, load_model_and_classes
from utils import IMG_SIZE

explainer = lime_image.LimeImageExplainer()


def generate_lime_overlay(img_path_or_file):
    """
    Input:
        - image file path
        - or FileStorage object from Flask
    
    Returns:
        lime_img (numpy array)
        top_label (int)
    """
    # 1. Load image (WITHOUT preprocess_input)
    if hasattr(img_path_or_file, "read"):  # Flask uploaded file
        img = tf.keras.preprocessing.image.load_img(img_path_or_file, target_size=IMG_SIZE)
    else:
        img = tf.keras.preprocessing.image.load_img(img_path_or_file, target_size=IMG_SIZE)

    img_np = tf.keras.preprocessing.image.img_to_array(img).astype("double")

    # 2. Run LIME
    explanation = explainer.explain_instance(
        img_np,
        predict_fn,
        top_labels=1,
        hide_color=0,
        num_samples=400     # can be increased if needed
    )

    top_label = explanation.top_labels[0]

    # 3. Get masked overlay
    temp, mask = explanation.get_image_and_mask(
        top_label,
        positive_only=True,
        num_features=5,
        hide_rest=False
    )

    lime_img = mark_boundaries(temp.astype("uint8") / 255.0, mask)

    return lime_img, top_label
