import { motion } from "framer-motion";

export default function PredictionCard({ data, loading }) {

  const confidencePct =
    data?.confidence
      ? Math.round(data.confidence * 100)
      : 0;

  const confidenceLabel = () => {
    if (confidencePct >= 90) return "High confidence";
    if (confidencePct >= 75) return "Moderate confidence";
    return "Low confidence";
  };

  const severityLabel = () => {
    if (data?.label === "Normal") {
      return "No abnormality detected";
    }

    switch(data?.severity?.toLowerCase()){
      case "mild":
        return "Mild involvement";
      case "moderate":
        return "Moderate involvement";
      case "severe":
        return "Significant involvement";
      default:
        return data?.severity || "Unknown";
    }
  };

  const severityColor = () => {
    if (data?.label === "Normal") {
      return "text-green-400";
    }

    switch(data?.severity?.toLowerCase()){
      case "mild":
        return "text-yellow-300";
      case "moderate":
        return "text-orange-400";
      case "severe":
        return "text-red-400";
      default:
        return "text-blue-400";
    }
  };

  return (
    <motion.div
      initial={{ opacity:0, y:40 }}
      animate={{ opacity:1, y:0 }}
      className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 shadow-lg"
    >

      <h2 className="text-xl font-semibold mb-4 text-white">
        Prediction Result
      </h2>

      {loading && (
        <div className="space-y-4">
          <div className="h-6 w-40 bg-white/10 rounded animate-pulse"></div>
          <div className="h-4 w-full bg-white/10 rounded animate-pulse"></div>
        </div>
      )}

      {!loading && data && (
        <div className="space-y-5">

          {/* Diagnosis */}
          <motion.div
            initial={{ scale:.9 }}
            animate={{ scale:1 }}
            className="text-2xl font-bold text-blue-400"
          >
            {data.label}
          </motion.div>

          {/* Severity */}
          <div className="flex justify-between items-center">
            <span className="text-gray-400">
              Clinical Severity
            </span>

            <span className={`font-semibold ${severityColor()}`}>
              {severityLabel()}
            </span>
          </div>

          {/* Certainty */}
          <div className="flex justify-between items-center">
            <span className="text-gray-400">
              Model Certainty
            </span>

            <span className="text-purple-300 font-medium">
              {confidenceLabel()}
            </span>
          </div>

        </div>
      )}

      {!loading && !data && (
        <p className="text-gray-400 text-sm">
          Upload an image to see prediction results.
        </p>
      )}

    </motion.div>
  );
}