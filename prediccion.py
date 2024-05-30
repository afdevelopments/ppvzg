from tensorflow.keras.models import load_model
import numpy as np
from joblib import load
import pandas as pd

# Carga el modelo
model = load_model('modelo_viviendas.h5')

# Cargamos el transformer y el scaler
transformer = load('transformer.joblib')
scaler = load('scaler.joblib')

# Para el transformer, podemos ver qué transformaciones se aplicaron a qué columnas
print("Transformer:")
for i, (name, trans, column) in enumerate(transformer.transformers_):
    print(f"Transformer {i}:")
    print(f"\tName: {name}")
    print(f"\tTransformer: {trans}")
    print(f"\tColumns: {column}")

# Para el scaler, podemos ver el valor medio y la desviación estándar que se utilizó para la normalización
print("\nScaler:")
print(f"\tMean: {scaler.mean_}")
print(f"\tScale: {scaler.scale_}")

# Supongamos que tienes un nuevo conjunto de características para una vivienda
# Las características se inventaron para este ejemplo y pueden no reflejar valores reales.
nueva_vivienda = pd.DataFrame({
    'Clasificación general del inmueble': [1],
    'Número de recámaras': [2],
    'Clasificación de la zona': [1],
    'Superficie construida': [60],
    'Superficie del lote': [60],
    'Número de baños': [3],
    'Edad del inmueble': [1],
    'Fecha de venta': [2024]
}, index=[0])

nueva_vivienda = nueva_vivienda[[
    'Clasificación general del inmueble',
    'Número de recámaras',
    'Clasificación de la zona',
    'Superficie construida',
    'Superficie del lote',
    'Número de baños',
    'Edad del inmueble',
    'Fecha de venta'
]]

nueva_vivienda_transformed = transformer.transform(nueva_vivienda)
nueva_vivienda_scaled = scaler.transform(nueva_vivienda_transformed)

# Usa el modelo para predecir el precio de la nueva vivienda
precio_predicho = model.predict(nueva_vivienda_scaled)

print(f"El precio predicho para la nueva vivienda es: {np.expm1(precio_predicho)[0][0]}")
