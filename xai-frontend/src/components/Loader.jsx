import React from "react";
import "./Loader.css";

const Loader = () => {
    return (
        <div className="loader-container">
            <div className="spinner"></div>
            <p>Analyzing X-ray…</p>
        </div>
    );
};

export default Loader;
