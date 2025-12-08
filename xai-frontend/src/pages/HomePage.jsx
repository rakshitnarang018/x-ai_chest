import React, { useState } from "react";
import ImageUploader from "../components/ImageUploader";
import Loader from "../components/Loader";
import ResultPanel from "../components/ResultPanel";
import { analyzeImage } from "../api/analyze";

// Modern, attractive Home Page with improved UI
export default function HomePage() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleImageSelect = (file) => {
    setSelectedImage(file);
    setPreview(URL.createObjectURL(file));
    setResult(null);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (!selectedImage) {
      setError("Please upload an X-ray first.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await analyzeImage(selectedImage);
      setResult(response);
    } catch (err) {
      setError("Something went wrong. Try again.");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex flex-col items-center py-10 px-4">
      <div className="max-w-3xl w-full bg-white shadow-xl rounded-3xl p-10 border border-gray-100">
        <h1 className="text-4xl font-bold text-gray-800 text-center mb-2 tracking-tight">
          Chest X-Ray AI Diagnosis
        </h1>
        <p className="text-center text-gray-500 mb-10 text-lg">
          Pneumonia • COVID‑19 • Tuberculosis • Normal
        </p>

        <div className="mb-6">
          <ImageUploader onImageSelect={handleImageSelect} />
        </div>

        <button
          onClick={handleAnalyze}
          className="w-full py-3 rounded-xl bg-blue-600 text-white text-lg font-semibold hover:bg-blue-700 active:scale-95 transition-all shadow-lg"
        >
          Analyze X‑Ray
        </button>

        {loading && (
          <div className="mt-6 flex justify-center">
            <Loader />
          </div>
        )}

        {error && (
          <p className="text-red-500 text-center mt-4 text-lg">{error}</p>
        )}

        {result && (
          <div className="mt-10">
            <ResultPanel originalImagePreview={preview} result={result} />
          </div>
        )}
      </div>
    </div>
  );
}