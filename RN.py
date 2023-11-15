import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense

# Intentamos cargar el modelo existente esto para seguir entrenando el modelo
try:
    model = load_model("multiplication_model.h5")
    print("Modelo cargado exitosamente.")
except:
    # Si no existe el modelo, creamos uno nuevo
    print("No se encontró el modelo existente. Se creará uno nuevo.")
    model = Sequential()
    model.add(Dense(8, input_dim=2, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mean_squared_error', optimizer='adam')

# Generamos nuevos datos de entrenamiento en el rango de 0 a 10 en este caso
X_train = np.random.random((10000, 2)) * 10.0  # Números aleatorios entre 0 y 10
y_train = X_train[:, 0] * X_train[:, 1]

# Normalizamos los nuevos datos
X_train_normalized = X_train / 10.0
y_train_normalized = y_train / 100.0  # Normalizamos y en un rango más pequeño

# Entrenamos el modelo con los nuevos datos
model.fit(X_train_normalized, y_train_normalized, epochs=50, batch_size=32, verbose=2)

# Guardamos el modelo actualizado
model.save("multiplication_model.h5")
