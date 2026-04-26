import { useState } from "react";
import { motion } from "framer-motion";

import ImageUploader from "../components/upload/ImageUploader";
import PredictionCard from "../components/results/PredictionCard";
import GradCamViewer from "../components/visualization/GradCamViewer";
import LlamaResponse from "../components/ai/LlamaResponse";
import LimeButton from "../components/buttons/LimeButton";
import BoundingBoxOverlay from "../components/visualization/BoundingBoxOverlay";
import { predictDental } from "../services/dentalService";
import { getGradCam, getLlama } from "../services/predictionService";
import { convertToBase64 } from "../utils/base64";

export default function Dental() {
  const [image, setImage] = useState(null);

  const [prediction, setPrediction] = useState(null);
  const [gradcam, setGradcam] = useState(null);
  const [llama, setLlama] = useState(null);

  const [boxes, setBoxes] = useState([]);
  const [showBoxes, setShowBoxes] = useState(false);

  const [loading, setLoading] = useState({
    prediction: false,
    gradcam: false,
    llama: false,
  });

  const handleUpload = async (file) => {
  setImage(URL.createObjectURL(file));

  setLoading({
    prediction: true,
    gradcam: true,
    llama: true,
  });

  try {
    const base64 = await convertToBase64(file);

    // 🔹 Prediction + boxes
    const res = await predictDental(base64);

    setPrediction({
      label: res.label,
      confidence: res.confidence,
    });

    setBoxes(res.boxes);

    setLoading((prev) => ({ ...prev, prediction: false }));

    // 🔹 Parallel
    getGradCam(base64).then((res) => {
      setGradcam(res.image);
      setLoading((prev) => ({ ...prev, gradcam: false }));
    });

    getLlama(base64).then((res) => {
      setLlama(res.text);
      setLoading((prev) => ({ ...prev, llama: false }));
    });

  } catch (err) {
    console.error(err);
  }
};

  const handleLimeClick = () => {
    setShowBoxes(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-gray-950 text-white px-6 py-10">

      {/* Title */}
      <motion.h1
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-3xl md:text-4xl font-bold mb-8 text-center bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent"
      >
        Dental Image Analysis
      </motion.h1>

      {/* Upload */}
      <ImageUploader onUpload={handleUpload} />

      {image && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-10 grid grid-cols-1 lg:grid-cols-2 gap-8"
        >

          {/* LEFT */}
          <div className="space-y-6">
            <PredictionCard data={prediction} loading={loading.prediction} />
            <LlamaResponse data={llama} loading={loading.llama} />

            <LimeButton onClick={handleLimeClick} />
          </div>

          {/* RIGHT */}
          <div className="space-y-6">

            {/* Image with Bounding Boxes */}
            <motion.div
              className="bg-white/5 border border-white/10 rounded-2xl p-4"
              initial={{ scale: 0.95 }}
              animate={{ scale: 1 }}
            >
              <p className="text-gray-400 mb-2">Detected Regions</p>

              <BoundingBoxOverlay
                image={image}
                boxes={boxes}
                show={showBoxes}
              />
            </motion.div>

            {/* Grad-CAM */}
            <GradCamViewer data={gradcam} loading={loading.gradcam} />

          </div>
        </motion.div>
      )}
    </div>
  );
}