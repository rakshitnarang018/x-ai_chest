import { motion } from "framer-motion";
import { useEffect, useState } from "react";

export default function LlamaResponse({ data, loading }) {
  const [displayText, setDisplayText] = useState("");

  // ✨ Typing effect
  useEffect(() => {
    if (!data) return;

    let i = 0;
    setDisplayText("");

    const interval = setInterval(() => {
      setDisplayText((prev) => prev + data.charAt(i));
      i++;
      if (i >= data.length) clearInterval(interval);
    }, 20);

    return () => clearInterval(interval);
  }, [data]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 shadow-lg"
    >
      <h2 className="text-xl font-semibold mb-4 text-white">
        AI Explanation (LLaMA)
      </h2>

      {/* LOADING STATE */}
      {loading && (
        <div className="flex items-center gap-3 text-gray-400">
          
          {/* Animated dots */}
          <div className="flex gap-1">
            <motion.div
              animate={{ y: [0, -5, 0] }}
              transition={{ repeat: Infinity, duration: 0.6 }}
              className="w-2 h-2 bg-blue-400 rounded-full"
            />
            <motion.div
              animate={{ y: [0, -5, 0] }}
              transition={{ repeat: Infinity, duration: 0.6, delay: 0.2 }}
              className="w-2 h-2 bg-purple-400 rounded-full"
            />
            <motion.div
              animate={{ y: [0, -5, 0] }}
              transition={{ repeat: Infinity, duration: 0.6, delay: 0.4 }}
              className="w-2 h-2 bg-green-400 rounded-full"
            />
          </div>

          <span>Analyzing with AI...</span>
        </div>
      )}

      {/* DATA STATE */}
      {!loading && data && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-gray-300 leading-relaxed whitespace-pre-line"
        >
          {displayText}
          <span className="animate-pulse">|</span>
        </motion.p>
      )}

      {/* EMPTY STATE */}
      {!loading && !data && (
        <p className="text-gray-400 text-sm">
          AI explanation will appear here.
        </p>
      )}
    </motion.div>
  );
}