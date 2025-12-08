import base64
import io
import matplotlib.pyplot as plt
from openai import OpenAI
from model_loader import load_model_and_classes

# Requires OPENAI_API_KEY in environment
client = OpenAI()

def ask_openai_lime_explanation(lime_np_img, predicted_label_idx):
    """
    Sends LIME overlay + predicted label to OpenAI multimodal model.
    Returns explanation (text).
    """

    # Convert numpy to PNG bytes
    buf = io.BytesIO()
    plt.imsave(buf, lime_np_img, format="png")
    buf.seek(0)
    img_bytes = buf.read()

    b64_image = base64.b64encode(img_bytes).decode("utf-8")
    _, idx_to_class = load_model_and_classes()

    label_name = idx_to_class[predicted_label_idx]

    prompt = (
        "You are a radiology assistant.\n\n"
        "The attached image is a chest X-ray with a LIME explanation overlay.\n"
        "Highlighted regions show important areas for prediction.\n\n"
        f"The model predicted: {label_name}\n\n"
        "Explain why the model might be focusing on these regions.\n"
        "Include limitations & reliability considerations.\n"
    )

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": f"data:image/png;base64,{b64_image}"}
                ]
            }
        ]
    )

    return response.output_text.strip()
