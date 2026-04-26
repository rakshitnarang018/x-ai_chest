import React, { useState } from "react";
import { Upload } from "lucide-react";

const ImageUploader = ({ onImageSelect }) => {
    const [preview, setPreview] = useState(null);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setPreview(URL.createObjectURL(file));
        onImageSelect(file);
    };

    return (
        <div className="w-full flex flex-col items-center">
            <h3 className="text-2xl font-semibold text-gray-700 mb-4">
                Upload Chest X-Ray
            </h3>

            <label
                className="
                w-full max-w-xl 
                flex flex-col items-center justify-center
                p-8 border-2 border-dashed border-gray-300
                rounded-2xl cursor-pointer bg-white
                hover:border-blue-500 hover:bg-blue-50
                transition-all shadow-sm hover:shadow-lg
            "
            >
                <Upload className="w-10 h-10 text-blue-600 mb-3" />
                <p className="text-gray-600 mb-2 font-medium">
                    Click to upload or drag & drop
                </p>
                <span className="text-sm text-gray-400">
                    PNG, JPG, JPEG allowed
                </span>

                <input
                    type="file"
                    accept="image/png, image/jpeg, image/jpg"
                    onChange={handleFileChange}
                    className="hidden"
                />
            </label>

            {preview && (
                <div className="mt-6 w-full max-w-xl">
                    <p className="text-gray-600 font-medium mb-2">
                        Preview:
                    </p>

                    <div className="rounded-xl overflow-hidden shadow-lg border border-gray-200">
                        <img
                            src={preview}
                            alt="preview"
                            className="w-full object-contain max-h-96 bg-black/5"
                        />
                    </div>
                </div>
            )}
        </div>
    );
};

export default ImageUploader;
