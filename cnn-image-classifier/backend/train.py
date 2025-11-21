"""
CIFAR-10 CNN Model Training Script
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import os

# GPU memory growth
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
    print(f"GPU topildi: {len(gpus)} ta")

# CIFAR-10 class nomlari
CLASS_NAMES = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

def create_model():
    """CNN modelini yaratish"""
    model = keras.Sequential([
        # 1-Conv block
        layers.Conv2D(32, (3, 3), padding='same', input_shape=(32, 32, 3)),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Conv2D(32, (3, 3), padding='same'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),

        # 2-Conv block
        layers.Conv2D(64, (3, 3), padding='same'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Conv2D(64, (3, 3), padding='same'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),

        # 3-Conv block
        layers.Conv2D(128, (3, 3), padding='same'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Conv2D(128, (3, 3), padding='same'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),

        # Dense layers
        layers.Flatten(),
        layers.Dense(512),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Dropout(0.5),
        layers.Dense(10, activation='softmax')
    ])
    return model

def main():
    # Dataset yuklash
    print("CIFAR-10 dataset yuklanmoqda...")
    (x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

    # Normalizatsiya
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0

    print(f"Train: {x_train.shape}, Test: {x_test.shape}")

    # Data augmentation
    data_augmentation = keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
    ])

    # Model yaratish
    model = create_model()
    model.summary()

    # Compile
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=10,
            restore_best_weights=True
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6
        ),
        keras.callbacks.ModelCheckpoint(
            'app/ml_model/saved_models/cifar10_model.h5',
            monitor='val_accuracy',
            save_best_only=True
        )
    ]

    # Training
    print("\nTraining boshlanmoqda...")
    history = model.fit(
        x_train, y_train,
        batch_size=64,
        epochs=100,
        validation_split=0.1,
        callbacks=callbacks,
        verbose=1
    )

    # Evaluation
    print("\nTest natijasi:")
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
    print(f"Test accuracy: {test_acc*100:.2f}%")
    print(f"Test loss: {test_loss:.4f}")

    # Model saqlash
    os.makedirs('app/ml_model/saved_models', exist_ok=True)
    model.save('app/ml_model/saved_models/cifar10_model.h5')
    print("\nModel saqlandi: app/ml_model/saved_models/cifar10_model.h5")

if __name__ == "__main__":
    main()
