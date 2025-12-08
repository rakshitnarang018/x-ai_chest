MODULES = {
    "chest_multidisease": {
        "model_path": "backend/saved_models/chest_multidisease.h5",
        "image_size": (224, 224),
        "classes": ["Normal", "Pneumonia", "Tuberculosis", "COVID-19"]
    },
    "brain_tumor": {
        "model_path": "backend/saved_models/brain_tumor.h5",
        "image_size": (224, 224),
        "classes": ["No Tumor", "Tumor"]
    }
}
