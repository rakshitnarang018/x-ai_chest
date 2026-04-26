import { motion } from "framer-motion";

export default function LimeButton({ onClick, loading }) {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      disabled={loading}
      className={`w-full py-3 rounded-xl font-semibold transition-all duration-300
        ${
          loading
            ? "bg-gray-700 cursor-not-allowed"
            : "bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 shadow-lg shadow-green-500/20"
        }`}
    >
      {loading ? "Generating LIME..." : "Show LIME Explanation"}
    </motion.button>
  );
}