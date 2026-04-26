import { useState } from "react";
import { motion } from "framer-motion";
import ImageUploader from "../components/upload/ImageUploader";
import PredictionCard from "../components/results/PredictionCard";
import GradCamViewer from "../components/visualization/GradCamViewer";
import LlamaResponse from "../components/ai/LlamaResponse";
import LimeButton from "../components/buttons/LimeButton";
import LimeOverlay from "../components/visualization/LimeOverlay";
import { convertToBase64 } from "../utils/base64";
import {
  predictImage,
  getGradCam,
  getLlama,
  getLime,
} from "../services/predictionService";

export default function Detection() {
  const [image, setImage] = useState(null);
  const [imageFile, setImageFile] = useState(null);

  const [prediction, setPrediction] = useState(null);
  const [gradcam, setGradcam] = useState(null);
  const [llama, setLlama] = useState(null);
  const [lime, setLime] = useState(null);

  const [loading, setLoading] = useState({
    prediction: false,
    gradcam: false,
    llama: false,
    lime: false,
  });

  // 🚀 Main pipeline trigger
  const handleUpload = async (file) => {
    setImageFile(file);
  const imageUrl = URL.createObjectURL(file);
  setImage(imageUrl);

  setLoading({
    prediction: true,
    gradcam: true,
    llama: true,
    lime: false,
  });

  try {
    const base64 = await convertToBase64(file);

    // 🔹 FAST: Prediction first
    const predictionRes = await predictImage(base64);

    setPrediction({
      label: predictionRes.label,
      confidence: predictionRes.confidence,
    });

    setLoading((prev) => ({ ...prev, prediction: false }));

    // 🔹 PARALLEL CALLS (IMPORTANT)
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

  const handleLime = async () => {
  setLoading((prev) => ({ ...prev, lime: true }));

  try {
    const base64 = await convertToBase64(imageFile); // store file in state
    const res = await getLime(base64);

    setLime(res.image);
  } catch (err) {
    console.error(err);
  }

  setLoading((prev) => ({ ...prev, lime: false }));
};

  return (
    <div className="min-h-screen flex flex-col items-center justify-start bg-gradient-to-br from-black via-gray-900 to-gray-950 text-white px-6 py-10">

      {/* Page Title */}
      <motion.h1
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-3xl md:text-4xl font-bold mb-8 text-center bg-gradient-to-r from-blue-400 via-purple-400 to-pink-500 drop-shadow-[0_0_20px_rgba(139,92,246,0.6)] bg-clip-text text-transparent"
      >
        Medical Image Detection
      </motion.h1>

      {/* Upload Section */}
      <ImageUploader onUpload={handleUpload} />

      {/* Content Grid */}
      {image && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-10 grid grid-cols-1 lg:grid-cols-2 gap-8"
        >

          {/* LEFT SIDE */}
          <div className="space-y-6">

            {/* Prediction */}
            <PredictionCard
              data={prediction}
              loading={loading.prediction}
            />

            {/* LLaMA */}
            <LlamaResponse
              data={llama}
              loading={loading.llama}
            />

            {/* LIME Button */}
            <LimeButton onClick={handleLime} loading={loading.lime} />

          </div>

          {/* RIGHT SIDE */}
          <div className="space-y-6">

            {/* Original Image */}
            <motion.div
              className="bg-white/5 border border-white/20 shadow-xl shadow-blue-500/10 hover:shadow-purple-500/20 rounded-2xl p-4"
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
            >
              <p className="text-gray-400 mb-2">Uploaded Image</p>
              <img
                src={image}
                alt="uploaded"
                className="rounded-xl w-full object-cover"
              />
            </motion.div>

            {/* Grad-CAM */}
            <GradCamViewer
              data={gradcam}
              loading={loading.gradcam}
            />

            {/* LIME Result */}
            {lime && (
              <LimeOverlay image={lime} />
            )}

          </div>
        </motion.div>
      )}
    </div>
  );
}