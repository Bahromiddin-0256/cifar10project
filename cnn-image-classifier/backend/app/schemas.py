from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime

class PredictionResponse(BaseModel):
    """Bashorat natijasi sxemasi"""
    predicted_class: str = Field(..., description="Bashorat qilingan sinf")
    confidence: float = Field(..., description="Ishonch darajasi (0-100)")
    probabilities: Dict[str, float] = Field(..., description="Barcha sinflar ehtimolliklari")
    processing_time: float = Field(..., description="Qayta ishlash vaqti (sekundlarda)")

class ModelInfoResponse(BaseModel):
    """Model ma'lumotlari sxemasi"""
    model_name: str
    input_shape: str
    classes: List[str]
    accuracy: float
    description: str

class HistoryEntry(BaseModel):
    """Tarix yozuvi sxemasi"""
    timestamp: datetime
    filename: str
    predicted_class: str
    confidence: float
