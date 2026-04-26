import { motion } from "framer-motion";

export default function PredictionCard({ data, loading }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 shadow-lg"
    >
      <h2 className="text-xl font-semibold mb-4 text-white">
        Prediction Result
      </h2>

      {/* LOADING STATE */}
      {loading && (
        <div className="space-y-4">
          <div className="h-6 w-40 bg-white/10 rounded animate-pulse"></div>
          <div className="h-4 w-full bg-white/10 rounded animate-pulse"></div>
        </div>
      )}

      {/* DATA STATE */}
      {!loading && data && (
        <div className="space-y-4">

          {/* Label */}
          <motion.div
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            className="text-2xl font-bold text-blue-400"
          >
            {data.label}
          </motion.div>

          {/* Confidence Bar */}
          <div>
            <div className="flex justify-between text-sm text-gray-400 mb-1">
              <span>Confidence</span>
              <span>{data.confidence}%</span>
            </div>

            <div className="w-full h-3 bg-white/10 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${data.confidence}%` }}
                transition={{ duration: 1 }}
                className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"
              />
            </div>
          </div>

        </div>
      )}

      {/* EMPTY STATE */}
      {!loading && !data && (
        <p className="text-gray-400 text-sm">
          Upload an image to see prediction results.
        </p>
      )}
    </motion.div>
  );
}