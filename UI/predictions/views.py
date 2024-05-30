from django.shortcuts import render
from .forms import PredictionForm
from tensorflow.keras.models import load_model
import numpy as np
from joblib import load
import pandas as pd



# Carga el modelo y los transformadores
model = load_model('resources/modelo_viviendas.h5')
transformer = load(open('resources/transformer.joblib', 'rb'))
scaler = load('resources/scaler.joblib')
def index(request):
    # Vista para la página de inicio
    return render(request, 'predictions/index.html')

def predict(request):
    # Vista para el formulario de predicción
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            return predict_price(request, form)
    else:
        form = PredictionForm()
    return render(request, 'predictions/form.html', {'form': form})

def predict_price(request, form):

    # Prepara los datos y realiza la predicción
    data = pd.DataFrame({
        'Clasificación general del inmueble': [form.cleaned_data['clasificacion_general']],
        'Número de recámaras': [form.cleaned_data['numero_de_recamaras']],
        'Clasificación de la zona': [form.cleaned_data['clasificacion_zona']],
        'Superficie construida': [form.cleaned_data['superficie_construida']],
        'Superficie del lote': [form.cleaned_data['superficie_lote']],
        'Número de baños': [form.cleaned_data['numero_de_banos']],
        'Edad del inmueble': [form.cleaned_data['edad_del_inmueble']],
        'Fecha de venta': [form.cleaned_data['fecha_de_venta']]
    }, index=[0])

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
    data_transformed = transformer.transform(nueva_vivienda)
    data_scaled = scaler.transform(data_transformed)
    predicted_price = model.predict(data_scaled)
    price = np.expm1(predicted_price)[0][0]
    return render(request, 'predictions/result.html', {'price': price})

def result(request):
    # Esta vista es opcional, dependiendo de cómo manejes la respuesta de resultados
    return render(request, 'predictions/result.html')
