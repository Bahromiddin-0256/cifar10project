from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import numpy as np
from PIL import Image
import io
from datetime import datetime
from typing import List
import logging

from app.ml_model.model import CNNModel
from app.schemas import PredictionResponse, ModelInfoResponse

# Logging sozlash
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI ilovasini yaratish
app = FastAPI(
    title="CNN Image Classifier API",
    description="CIFAR-10 dataset uchun CNN model API",
    version="1.0.0"
)

# CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CNN modelini yuklash
cnn_model = CNNModel()
prediction_history = []

@app.on_event("startup")
async def startup_event():
    """Ilova ishga tushganda modelni yuklash"""
    logger.info("Loading CNN model...")
    cnn_model.load_model()
    logger.info("Model successfully loaded!")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CNN Image Classifier API",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": cnn_model.is_loaded(),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/model/info", response_model=ModelInfoResponse)
async def get_model_info():
    """Model haqida ma'lumot"""
    return ModelInfoResponse(
        model_name="CNN CIFAR-10 Classifier",
        input_shape="32x32x3",
        classes=cnn_model.class_names,
        accuracy=cnn_model.get_accuracy(),
        description="Convolutional Neural Network trained on CIFAR-10 dataset"
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict_image(file: UploadFile = File(...)):
    """
    Rasmni yuklash va klassifikatsiya qilish
    """
    try:
        # Fayl formatini tekshirish
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="Faqat rasm fayllari qabul qilinadi"
            )

        # Rasmni o'qish
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Bashorat qilish
        prediction_result = cnn_model.predict(image)

        # Tarixga qo'shish
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "filename": file.filename,
            "predicted_class": prediction_result["predicted_class"],
            "confidence": prediction_result["confidence"]
        }
        prediction_history.append(history_entry)

        # Faqat oxirgi 100 ta natijani saqlash
        if len(prediction_history) > 100:
            prediction_history.pop(0)

        logger.info(f"Prediction: {prediction_result['predicted_class']} "
                   f"({prediction_result['confidence']:.2f}%)")

        return PredictionResponse(**prediction_result)

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/batch")
async def predict_batch(files: List[UploadFile] = File(...)):
    """
    Bir nechta rasmni bir vaqtda klassifikatsiya qilish
    """
    try:
        if len(files) > 10:
            raise HTTPException(
                status_code=400,
                detail="Maksimal 10 ta rasm yuklash mumkin"
            )

        results = []
        for file in files:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            prediction_result = cnn_model.predict(image)

            results.append({
                "filename": file.filename,
                **prediction_result
            })

        return {"predictions": results, "total": len(results)}

    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_prediction_history():
    """Bashorat tarixini olish"""
    return {
        "history": prediction_history[-20:],  # Oxirgi 20 ta
        "total": len(prediction_history)
    }

@app.delete("/history")
async def clear_history():
    """Tarixni tozalash"""
    prediction_history.clear()
    return {"message": "History cleared successfully"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
