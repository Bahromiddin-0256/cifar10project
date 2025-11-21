import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import time
import os

class CNNModel:
    """CNN model wrapper klassi"""

    def __init__(self, model_path="app/ml_model/saved_models/cifar10_model.h5"):
        self.model_path = model_path
        self.model = None
        self.class_names = [
            'airplane', 'automobile', 'bird', 'cat', 'deer',
            'dog', 'frog', 'horse', 'ship', 'truck'
        ]
        self.input_shape = (32, 32, 3)
        self.test_accuracy = 0.85  # O'zingizning haqiqiy accuracy qiymatini kiriting

    def load_model(self):
        """Modelni yuklash"""
        try:
            if os.path.exists(self.model_path):
                self.model = keras.models.load_model(self.model_path)
                print(f"Model yuklandi: {self.model_path}")
            else:
                print("Model fayli topilmadi. Demo model yaratilmoqda...")
                self.create_demo_model()
        except Exception as e:
            print(f"Model yuklashda xatolik: {e}")
            self.create_demo_model()

    def create_demo_model(self):
        """Demo model yaratish (test uchun)"""
        self.model = keras.Sequential([
            keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=self.input_shape),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.Flatten(),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(len(self.class_names), activation='softmax')
        ])
        self.model.compile(optimizer='adam',
                          loss='sparse_categorical_crossentropy',
                          metrics=['accuracy'])

    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Rasmni preprocessing qilish"""
        # RGB formatga o'tkazish
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # 32x32 ga o'lchamini o'zgartirish
        image = image.resize((32, 32), Image.Resampling.LANCZOS)

        # Numpy array ga aylantirish va normalizatsiya
        img_array = np.array(image)
        img_array = img_array.astype('float32') / 255.0

        # Batch dimension qo'shish
        img_array = np.expand_dims(img_array, axis=0)

        return img_array

    def predict(self, image: Image.Image) -> dict:
        """Rasmni klassifikatsiya qilish"""
        start_time = time.time()

        # Preprocessing
        processed_image = self.preprocess_image(image)

        # Bashorat
        predictions = self.model.predict(processed_image, verbose=0)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx] * 100)

        # Barcha sinflar ehtimolliklari
        probabilities = {
            self.class_names[i]: float(predictions[0][i] * 100)
            for i in range(len(self.class_names))
        }

        # Ehtimolliklarni tartiblash
        probabilities = dict(sorted(probabilities.items(),
                                   key=lambda x: x[1],
                                   reverse=True))

        processing_time = time.time() - start_time

        return {
            "predicted_class": self.class_names[predicted_class_idx],
            "confidence": round(confidence, 2),
            "probabilities": {k: round(v, 2) for k, v in probabilities.items()},
            "processing_time": round(processing_time, 3)
        }

    def is_loaded(self) -> bool:
        """Model yuklangan yoki yo'qligini tekshirish"""
        return self.model is not None

    def get_accuracy(self) -> float:
        """Model accuracy ni qaytarish"""
        return self.test_accuracy
