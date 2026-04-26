import { motion } from "framer-motion";

export default function LimeOverlay({ image }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 shadow-lg"
    >
      <h2 className="text-lg font-semibold mb-3 text-white">
        LIME Explanation
      </h2>

      <div className="relative rounded-xl overflow-hidden">
        
        {/* Glow Effect */}
        <div className="absolute inset-0 bg-green-500/20 blur-xl opacity-60"></div>

        {/* LIME Image */}
        <img
          src={image}
          alt="LIME"
          className="relative rounded-xl w-full object-cover"
        />
      </div>

      <p className="text-sm text-gray-400 mt-3">
        Highlighted regions show areas that influenced the model’s decision.
      </p>
    </motion.div>
  );
}