import React, { useState } from "react";
import ImageUploader from "../components/ImageUploader";
import Loader from "../components/Loader";
import ResultPanel from "../components/ResultPanel";
import { analyzeImage } from "../api/analyze";
import "./Home.css";

const HomePage = () => {
    const [selectedImage, setSelectedImage] = useState(null);
    const [preview, setPreview] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleImageSelect = (file) => {
        setSelectedImage(file);
        setPreview(URL.createObjectURL(file));
        setResult(null);
        setError(null);
    };

    const handleAnalyze = async () => {
        if (!selectedImage) {
            setError("Please upload an X-ray first.");
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const response = await analyzeImage(selectedImage);
            setResult(response);
        } catch (err) {
            setError("Something went wrong. Try again.");
        }

        setLoading(false);
    };

    return (
        <div className="home-container">
            <h1>Chest X-Ray AI Diagnosis</h1>
            <p className="subtitle">Pneumonia / COVID-19 / Tuberculosis / Normal</p>

            <ImageUploader onImageSelect={handleImageSelect} />

            <button className="analyze-btn" onClick={handleAnalyze}>
                Analyze
            </button>

            {loading && <Loader />}

            {error && <p className="error-text">{error}</p>}

            {result && (
                <ResultPanel
                    originalImagePreview={preview}
                    result={result}
                />
            )}
        </div>
    );
};

export default HomePage;
