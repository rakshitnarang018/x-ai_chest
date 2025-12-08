import base64
import io
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input

IMG_SIZE = (224, 224)

def load_image_as_array(file_or_path):
    """
    Accepts either:
      - an uploaded file (werkzeug FileStorage)
      - a file path string
    Returns:
      - original PIL image
      - numpy array preprocessed for model: shape (1,224,224,3)
    """
    if hasattr(file_or_path, "read"):  # FileStorage object from Flask
        img = Image.open(file_or_path).convert("RGB")
    else:
        img = Image.open(file_or_path).convert("RGB")

    img = img.resize(IMG_SIZE)
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    return img, img_array


def numpy_image_to_base64(np_img):
    """
    Converts a numpy image array (H,W,3) to PNG base64 string.
    """
    if np_img.dtype != np.uint8:
        np_img = np_img.astype("uint8")

    pil_img = Image.fromarray(np_img)
    buffer = io.BytesIO()
    pil_img.save(buffer, format="PNG")
    base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return base64_img
