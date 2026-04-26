import base64
import io
import matplotlib.pyplot as plt
import requests
from model_loader import load_model_and_classes


def ask_openai_lime_explanation(lime_np_img, predicted_label_idx):
    """
    Uses LIME explanation + predicted label to generate reasoning via local LLM.
    Optimized for low-RAM systems.
    """

    # Convert numpy image (kept for consistency, not used in API)
    buf = io.BytesIO()
    plt.imsave(buf, lime_np_img, format="png")
    buf.seek(0)

    _, idx_to_class = load_model_and_classes()
    label_name = idx_to_class[predicted_label_idx]

    # 🔥 Optimized prompt (short = faster response)
    prompt = (
        "You are a radiology assistant.\n"
        f"Prediction: {label_name}\n"
        "LIME highlighted important regions.\n\n"
        "Give 2-3 short bullet points explaining why.\n"
        "Also add 1 limitation.\n"
        "Keep it very brief.\n"
    )

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",   # ✅ lightweight model
                "prompt": prompt,
                "stream": False
            },
            timeout=180   # ✅ increased timeout
        )

        result = response.json()
        print("OLLAMA RAW RESPONSE:", result)

        # ✅ Handle all formats safely
        if "response" in result:
            return result["response"].strip()

        elif "message" in result and "content" in result["message"]:
            return result["message"]["content"].strip()

        elif "error" in result:
            return f"Ollama Error: {result['error']}"

        else:
            return "Error: Unexpected response format from Ollama"

    except requests.exceptions.Timeout:
        return "Error: Model took too long to respond (timeout). Try again."

    except Exception as e:
        return f"Error: {str(e)}"