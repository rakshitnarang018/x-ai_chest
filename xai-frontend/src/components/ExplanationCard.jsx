import React from "react";
import "./Explanation.css";

const ExplanationCard = ({ text }) => {
    return (
        <div className="explanation-card">
            <h3>AI Radiology Explanation</h3>
            <p>{text}</p>
        </div>
    );
};

export default ExplanationCard;
