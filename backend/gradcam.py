import numpy as np
import tensorflow as tf
import cv2
from model_loader import load_model_and_classes

def make_gradcam_heatmap(img_array):
    """
    img_array must be preprocessed for EfficientNet.
    Returns:
        heatmap (H,W) float
        predicted index (int)
    """
    model, idx_to_class = load_model_and_classes()

    # EfficientNetB0 inside your model
    base_model = model.get_layer("efficientnetb0")
    last_conv = base_model.get_layer("top_activation")

    grad_model = tf.keras.models.Model(
        inputs=base_model.input,
        outputs=[last_conv.output, base_model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, features = grad_model(img_array)

        x = features
        for layer in model.layers[2:]:
            x = layer(x)

        predictions = x
        pred_index = tf.argmax(predictions[0])
        class_channel = predictions[:, pred_index]

    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    heatmap = tf.reduce_sum(conv_outputs * pooled_grads, axis=-1)

    heatmap = tf.maximum(heatmap, 0)
    heatmap /= (tf.reduce_max(heatmap) + 1e-8)

    return heatmap.numpy(), int(pred_index)


def overlay_gradcam_on_image(original_pil_image, heatmap, alpha=0.4):
    """
    Returns final Grad-CAM visualization (numpy array RGB)
    """
    orig_array = np.array(original_pil_image)

    hmap = cv2.resize(heatmap, (orig_array.shape[1], orig_array.shape[0]))
    hmap = np.uint8(255 * hmap)
    hmap = cv2.applyColorMap(hmap, cv2.COLORMAP_JET)

    superimposed = (hmap * alpha + orig_array).astype("uint8")
    return superimposed
