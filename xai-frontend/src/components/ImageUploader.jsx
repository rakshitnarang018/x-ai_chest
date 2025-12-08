import React, { useState } from "react";
import "./Uploader.css";

const ImageUploader = ({ onImageSelect }) => {
    const [preview, setPreview] = useState(null);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setPreview(URL.createObjectURL(file));
        onImageSelect(file);
    };

    return (
        <div className="uploader-box">
            <h3>Upload Chest X-Ray</h3>

            <input
                type="file"
                accept="image/png, image/jpeg, image/jpg"
                onChange={handleFileChange}
            />

            {preview && (
                <div className="preview-box">
                    <img src={preview} alt="preview" />
                </div>
            )}
        </div>
    );
};

export default ImageUploader;
