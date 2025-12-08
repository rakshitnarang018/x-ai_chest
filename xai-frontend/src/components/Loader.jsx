import React from "react";

const Loader = () => {
    return (
        <div className="flex flex-col items-center justify-center py-6">
            
            {/* Animated Spinner */}
            <div className="relative w-14 h-14">
                <div className="absolute inset-0 rounded-full border-4 border-blue-300"></div>
                <div className="absolute inset-0 rounded-full border-4 border-blue-600 border-t-transparent animate-spin"></div>
            </div>

            <p className="text-gray-700 text-lg font-medium mt-4 animate-pulse">
                Analyzing X-ray…
            </p>
        </div>
    );
};

export default Loader;
