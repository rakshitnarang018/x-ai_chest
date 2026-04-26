import uuid
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from pipeline import analyze_image

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Make a unique temp filename
    ext = os.path.splitext(file.filename)[1]
    temp_name = f"{uuid.uuid4().hex}{ext}"
    temp_path = os.path.join(UPLOAD_FOLDER, temp_name)

    # Save uploaded file to disk
    file.save(temp_path)

    try:
        # Now pipeline sees a normal path string, just like /test-analyze
        result = analyze_image(temp_path)
        return jsonify(result), 200
    except Exception as e:
        # Optional: log the error
        print("Error in /analyze:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)



@app.route("/test-analyze", methods=["GET"])
def test_analyze():
    test_path = "test_images/sample.png"   # add any sample here

    if not os.path.exists(test_path):
        return jsonify({"error": "Test image not found"}), 500

    result = analyze_image(test_path)
    return jsonify(result), 200


if __name__ == "__main__":
    print("🚀 Starting Flask backend on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
