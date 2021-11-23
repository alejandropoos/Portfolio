import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# Importar datos
reloj = np.array([125, 85, 81, 100, 113], dtype=float)
accu_check = np.array([117, 79, 90, 91, 115], dtype=float)

#Capas del modelo
capa = tf.keras.layers.Dense(units=1, input_shape=[1])
modelo = tf.keras.Sequential([capa])

#Compilacion del modelo
modelo.compile(optimizer=tf.keras.optimizers.Adam(0.1), loss='mean_squared_error')

#Entrenamiento del modelo
print("Comenzando entrenamiento...")
historial = modelo.fit(reloj, accu_check, epochs=1500, verbose=False)
print("Entrenamiento finalizado.")

#Graficar resultados
plt.xlabel("Epocas")
plt.ylabel("Magnitud de perdida")
plt.plot(historial.history['loss'])

#Predicciones
print("Hagamos una prediccion")
resultado = modelo.predict([100.0])
print(f"El resultado es {resultado}mg/dL de glucosa")

#Ver pesos y sesgos
print("Variables internas del modelo")
print(capa.get_weights())
