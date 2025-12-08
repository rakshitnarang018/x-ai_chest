import tensorflow as tf
import numpy as np
from tensorflow.keras.applications.efficientnet import preprocess_input

MODEL_PATH = "saved_models/chest_multidisease_ft.keras"

model = None
idx_to_class = None
class_to_idx = None


def load_model_and_classes():
    global model, idx_to_class, class_to_idx

    if model is None:
        print("🔵 Loading TensorFlow model...")
        model = tf.keras.models.load_model(MODEL_PATH)

        # Class order based on your notebook
        class_to_idx = {
            "covid-19": 0,
            "normal": 1,
            "pneumonia": 2,
            "tuberculosis": 3
        }
        idx_to_class = {v: k for k, v in class_to_idx.items()}

    return model, idx_to_class


def predict_fn(images):
    """
    Used by LIME — expects images in raw 0–255 format.
    """
    imgs = images.astype(np.float32)
    imgs_pp = preprocess_input(imgs)
    preds = model.predict(imgs_pp)
    return preds


def get_predictions(img_array):
    """
    img_array: (1,224,224,3) preprocessed for EfficientNet
    Returns:
        predicted_class (str)
        predicted_index (int)
        probabilities (dict)
    """
    preds = model.predict(img_array)[0]
    pred_idx = int(np.argmax(preds))

    return pred_idx, preds.tolist()
