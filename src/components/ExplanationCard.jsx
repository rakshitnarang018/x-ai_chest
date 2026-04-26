import React from "react";
import { motion } from "framer-motion";

const ExplanationCard = ({ text }) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="w-full max-w-2xl mx-auto mt-6 p-6 bg-white rounded-2xl shadow-lg border border-gray-200 hover:shadow-xl transition-shadow"
        >
            <h3 className="text-2xl font-bold text-blue-600 mb-3 tracking-wide">
                AI Radiology Explanation
            </h3>

            <p className="text-gray-700 text-lg leading-relaxed">
                {text}
            </p>
        </motion.div>
    );
};

export default ExplanationCard;
