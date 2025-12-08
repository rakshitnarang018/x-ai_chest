import React from "react";
import ProbabilityChart from "./ProbabilityChart";
import ImageComparison from "./ImageComparison";
import ExplanationCard from "./ExplanationCard";
import "./Result.css";

const ResultPanel = ({ originalImagePreview, result }) => {
    if (!result) return null;

    return (
        <div className="result-panel">
            <h2>Prediction: {result.predicted_class}</h2>

            <ProbabilityChart probabilities={result.probabilities} />

            <ImageComparison
                original={originalImagePreview}
                gradcam={result.gradcam_base64}
                lime={result.lime_base64}
            />

            <ExplanationCard text={result.openai_text} />
        </div>
    );
};

export default ResultPanel;
