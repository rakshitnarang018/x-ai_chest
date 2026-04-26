import React from "react";

const ProbabilityChart = ({ probabilities }) => {
    const entries = Object.entries(probabilities);

    return (
        <div className="w-full max-w-2xl bg-white rounded-2xl border border-gray-200 shadow-lg p-6 mx-auto mt-6">
            <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">
                Model Confidence
            </h3>

            <div className="space-y-5">
                {entries.map(([label, prob]) => {
                    const percentage = (prob * 100).toFixed(1);

                    return (
                        <div key={label}>
                            <div className="flex justify-between mb-1">
                                <span className="text-gray-700 font-medium">{label}</span>
                                <span className="text-gray-600">{percentage}%</span>
                            </div>

                            <div className="w-full h-4 bg-gray-200 rounded-full overflow-hidden shadow-inner">
                                <div
                                    className="h-full bg-blue-600 rounded-full transition-all duration-700 ease-out"
                                    style={{ width: `${percentage}%` }}
                                ></div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default ProbabilityChart;
