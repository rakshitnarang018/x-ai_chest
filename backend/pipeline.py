import numpy as np

from utils import load_image_as_array, numpy_image_to_base64
from model_loader import load_model_and_classes, get_predictions
from gradcam import make_gradcam_heatmap, overlay_gradcam_on_image
from lime_explainer import generate_lime_overlay
from openai_client import ask_openai_lime_explanation


def analyze_image(image_file_or_path):
    """
    Full pipeline:
      - Load image
      - Predict
      - Grad-CAM
      - LIME
      - OpenAI text explanation
    Returns dictionary:
      {
        "predicted_class": str,
        "probabilities": dict,
        "gradcam_base64": str,
        "lime_base64": str,
        "openai_text": str
      }
    """
    model, idx_to_class = load_model_and_classes()

    # 1. Load + preprocess image
    pil_img, img_array = load_image_as_array(image_file_or_path)

    # 2. Predict disease
    pred_idx, prob_list = get_predictions(img_array)
    predicted_class = idx_to_class[pred_idx]

    probs = {idx_to_class[i]: float(prob_list[i]) for i in range(len(prob_list))}

    # 3. Grad-CAM
    heatmap, _ = make_gradcam_heatmap(img_array)
    gradcam_img = overlay_gradcam_on_image(pil_img, heatmap)
    gradcam_base64 = numpy_image_to_base64(gradcam_img)

    # 4. LIME explanation
    lime_np_img, top_label = generate_lime_overlay(image_file_or_path)
    lime_base64 = numpy_image_to_base64((lime_np_img * 255).astype("uint8"))

    # 5. OpenAI radiology explanation
    openai_text = ask_openai_lime_explanation(lime_np_img, top_label)

    return {
        "predicted_class": predicted_class,
        "probabilities": probs,
        "gradcam_base64": gradcam_base64,
        "lime_base64": lime_base64,
        "openai_text": openai_text
    }
