#Red neuronal multicapa complejo
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import os
import pandas as pd

mediciones = list()

os.mkdir("data")
os.mkdir("data/train")
os.mkdir("data/test")
with open("Mediciones.txt","r") as archivo:
    for linea in archivo:
        mediciones.append(linea.strip("/n"))

# Importar datos - cuanto mas datos, mejor
#reloj = np.array([125, 85, 81, 100, 113], dtype=float)
reloj = np.array(mediciones, dtype=float)
accu_check = np.array([117, 79, 90, 91, 115, 96], dtype=float)

#Capas del modelo - 1 entrada, 2 ocultas y 1 salida
oculta1 = tf.keras.layers.Dense(units=3, input_shape=[1])
oculta2 = tf.keras.layers.Dense(units=3)
salida = tf.keras.layers.Dense(units=1)
modelo = tf.keras.Sequential([oculta1, oculta2, salida])

#Compilacion del modelo
modelo.compile(optimizer=tf.keras.optimizers.Adam(0.1), loss='mean_squared_error')

#Entrenamiento del modelo
print("Comenzando entrenamiento...")
historial = modelo.fit(reloj, accu_check, epochs=600, verbose=False)
print("Entrenamiento finalizado.")

#Graficar resultados
plt.xlabel("Epocas")
plt.ylabel("Magnitud de perdida")
plt.plot(historial.history['loss'])

#Predicciones
print("Hagamos una prediccion")
resultado = int(modelo.predict([100.0]))
print(f"El resultado es {resultado} mg/dL de glucosa")

#Ver pesos y sesgos
print("Variables internas del modelo")
print(oculta1.get_weights())
print(oculta2.get_weights())
print(salida.get_weights())
