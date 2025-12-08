import React from "react";
import "./Chart.css";

const ProbabilityChart = ({ probabilities }) => {
    const entries = Object.entries(probabilities);

    return (
        <div className="prob-chart">
            <h3>Model Confidence</h3>
            {entries.map(([label, prob]) => (
                <div key={label} className="prob-row">
                    <span>{label}</span>
                    <div className="bar">
                        <div
                            className="bar-fill"
                            style={{ width: `${(prob * 100).toFixed(1)}%` }}
                        ></div>
                    </div>
                    <span>{(prob * 100).toFixed(1)}%</span>
                </div>
            ))}
        </div>
    );
};

export default ProbabilityChart;
