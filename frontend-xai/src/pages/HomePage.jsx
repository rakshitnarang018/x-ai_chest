// import React, { useState } from "react";
// import ImageUploader from "../components/ImageUploader";
// import Loader from "../components/Loader";
// import ResultPanel from "../components/ResultPanel";
// import { analyzeImage } from "../api/analyze";

// // Modern, attractive Home Page with improved UI
// export default function HomePage() {
//   const [selectedImage, setSelectedImage] = useState(null);
//   const [preview, setPreview] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [result, setResult] = useState(null);
//   const [error, setError] = useState(null);

//   const handleImageSelect = (file) => {
//     setSelectedImage(file);
//     setPreview(URL.createObjectURL(file));
//     setResult(null);
//     setError(null);
//   };

//   const handleAnalyze = async () => {
//     if (!selectedImage) {
//       setError("Please upload an X-ray first.");
//       return;
//     }

//     setLoading(true);
//     setError(null);

//     try {
//       const response = await analyzeImage(selectedImage);
//       setResult(response);
//     } catch (err) {
//       setError("Something went wrong. Try again.");
//     }

//     setLoading(false);
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex flex-col items-center py-10 px-4">
//       <div className="max-w-3xl w-full bg-white shadow-xl rounded-3xl p-10 border border-gray-100">
//         <h1 className="text-4xl font-bold text-gray-800 text-center mb-2 tracking-tight">
//           Chest X-Ray AI Diagnosis
//         </h1>
//         <p className="text-center text-gray-500 mb-10 text-lg">
//           Pneumonia • COVID‑19 • Tuberculosis • Normal
//         </p>

//         <div className="mb-6">
//           <ImageUploader onImageSelect={handleImageSelect} />
//         </div>

//         <button
//           onClick={handleAnalyze}
//           className="w-full py-3 rounded-xl bg-blue-600 text-white text-lg font-semibold hover:bg-blue-700 active:scale-95 transition-all shadow-lg"
//         >
//           Analyze X‑Ray
//         </button>

//         {loading && (
//           <div className="mt-6 flex justify-center">
//             <Loader />
//           </div>
//         )}

//         {error && (
//           <p className="text-red-500 text-center mt-4 text-lg">{error}</p>
//         )}

//         {result && (
//           <div className="mt-10">
//             <ResultPanel originalImagePreview={preview} result={result} />
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }


import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-gray-950 text-white overflow-hidden">
      <div className="absolute inset-0 bg-black/40"></div>
      
      {/* Background Glow */}
      <div className="absolute top-[-100px] left-[-100px] w-[300px] h-[300px] bg-purple-600 opacity-20 blur-3xl rounded-full"></div>
      <div className="absolute bottom-[-100px] right-[-100px] w-[300px] h-[300px] bg-blue-600 opacity-20 blur-3xl rounded-full"></div>

      {/* Main Container */}
      <div className="relative z-10 flex flex-col items-center justify-center px-6 py-16 text-center">

        {/* Title */}
        <motion.h1
          initial={{ opacity: 0, y: -40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-500 bg-clip-text text-transparent drop-shadow-[0_0_25px_rgba(99,102,241,0.6)]"
        >
          X-RAY IMAGE ANALYSIS
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.8 }}
          className="mt-6 max-w-2xl text-gray-200 text-lg leading-relaxed"
        >
          Upload medical images and get instant AI-based predictions with 
          explainability tools like <span className="text-blue-400">Grad-CAM</span>, 
          <span className="text-purple-400"> LIME</span>, and 
          <span className="text-green-400"> LLaMA</span>.
        </motion.p>

        {/* About Section */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.8 }}
          className="mt-12 max-w-3xl bg-white/10 shadow-xl shadow-blue-500/10 backdrop-blur-xl border border-white/10 rounded-2xl p-6 shadow-lg"
        >
          <h2 className="text-2xl font-semibold mb-4 text-white">
            About the Project
          </h2>

          <p className="text-gray-400 leading-relaxed">
            This system uses advanced deep learning models to analyze medical 
            images in real-time. It performs classification and provides 
            visual explanations using Grad-CAM and LIME, while LLaMA generates 
            human-like insights about the detected condition.
            <br /><br />
            The goal is to make AI-driven diagnosis more transparent, 
            interpretable, and interactive.
          </p>
        </motion.div>

        {/* CTA Button */}
        <motion.button
          whileHover={{ scale: 1.08 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => navigate("/detection")}
          className="mt-10 px-8 py-4 text-lg font-semibold rounded-xl 
                     bg-gradient-to-r from-blue-500 to-purple-600 
                     hover:from-blue-600 hover:to-purple-700
                     shadow-lg shadow-blue-500/30 transition-all duration-300"
        >
          🚀 Start Analysis
        </motion.button>

      </div>
    </div>
  );
}