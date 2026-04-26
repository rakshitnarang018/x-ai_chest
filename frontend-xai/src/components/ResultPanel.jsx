import React from "react";
import ProbabilityChart from "./ProbabilityChart";
import ImageComparison from "./ImageComparison";
import ExplanationCard from "./ExplanationCard";

const ResultPanel = ({ originalImagePreview, result }) => {
    if (!result) return null;

    return (
        <div className="w-full max-w-4xl mx-auto mt-10 bg-white shadow-xl border border-gray-200 rounded-3xl p-8 space-y-10">
            
            {/* Prediction Title */}
            <div className="text-center">
                <h2 className="text-3xl font-bold text-blue-700 drop-shadow-sm">
                    Prediction: {result.predicted_class}
                </h2>
                <p className="text-gray-500 mt-1 tracking-wide">
                    AI Model Diagnostic Summary
                </p>
            </div>

            {/* Probability Chart */}
            <ProbabilityChart probabilities={result.probabilities} />

            {/* Image Comparison Section */}
            <div>
                <h3 className="text-2xl font-semibold text-gray-800 mb-4 text-center">
                    Diagnostic Visualizations
                </h3>
                <ImageComparison
                    original={originalImagePreview}
                    gradcam={result.gradcam_base64}
                    lime={result.lime_base64}
                />
            </div>

            {/* Explanation Card */}
            <ExplanationCard text={result.openai_text} />
        </div>
    );
};

export default ResultPanel;
