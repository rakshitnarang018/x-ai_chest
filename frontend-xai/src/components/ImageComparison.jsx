import React from "react";

const ImageComparison = ({ original, gradcam, lime }) => {
    const images = [
        { title: "Original X-ray", src: original },
        { title: "Grad-CAM Heatmap", src: `data:image/png;base64,${gradcam}` },
        { title: "LIME Overlay", src: `data:image/png;base64,${lime}` },
    ];

    return (
        <div className="w-full grid grid-cols-1 md:grid-cols-3 gap-8 mt-8">
            {images.map((img, i) => (
                <div
                    key={i}
                    className="bg-white p-5 rounded-2xl shadow-md hover:shadow-xl border border-gray-200 transition-all"
                >
                    <h4 className="text-xl font-semibold text-center text-gray-700 mb-3">
                        {img.title}
                    </h4>

                    <div className="w-full flex justify-center">
                        <img
                            src={img.src}
                            alt={img.title}
                            className="w-full h-64 object-contain rounded-xl"
                        />
                    </div>
                </div>
            ))}
        </div>
    );
};

export default ImageComparison;
