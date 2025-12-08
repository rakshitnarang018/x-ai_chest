import React from "react";
import "./Images.css";

const ImageComparison = ({ original, gradcam, lime }) => {
    return (
        <div className="image-grid">
            <div>
                <h4>Original X-ray</h4>
                <img src={original} alt="original" />
            </div>

            <div>
                <h4>Grad-CAM Heatmap</h4>
                <img src={`data:image/png;base64,${gradcam}`} alt="gradcam" />
            </div>

            <div>
                <h4>LIME Overlay</h4>
                <img src={`data:image/png;base64,${lime}`} alt="lime" />
            </div>
        </div>
    );
};

export default ImageComparison;
