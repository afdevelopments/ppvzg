import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import GridSearchCV
from joblib import dump
import statsmodels.api as sm


data = pd.read_csv('datos_viviendas.csv')

data['Fecha de venta'] = pd.to_datetime(data['Fecha de venta']).dt.year
data['Precio'] = np.log1p(data['Precio'])

X = data.drop('Precio', axis=1)
y = data['Precio']

categorical_features = ['Clasificación general del inmueble', 'Número de recámaras', 'Clasificación de la zona', 'Número de baños']
one_hot = OneHotEncoder()
transformer = ColumnTransformer([("one_hot", one_hot, categorical_features)], remainder="passthrough")
X_transformed = transformer.fit_transform(X)

# Guardamos el transformer
dump(transformer, 'transformer.joblib')

#Imprimimos los nombres de las características después de la transformación
feature_names = transformer.get_feature_names_out()
print(feature_names)

X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.2, random_state=42)

scaler = StandardScaler(with_mean=False)
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Guardamos el scaler
dump(scaler, 'scaler.joblib')

def create_model(optimizer='adam', dropout_rate=0.0, hidden_units=64, hidden_layers=1):
    model = Sequential()
    model.add(Dense(hidden_units, input_dim=X_train.shape[1], activation='elu'))
    model.add(Dropout(dropout_rate))

    for _ in range(hidden_layers - 1):
        model.add(Dense(hidden_units, activation='elu'))
        model.add(Dropout(dropout_rate))

    model.add(Dense(1, activation='linear'))
    model.compile(loss='mean_squared_error', optimizer=optimizer)
    return model

model = KerasRegressor(build_fn=create_model)

param_grid = {
    'optimizer': ['adam', 'rmsprop'],
    'dropout_rate': [0.0, 0.1, 0.2, 0.3],
    'hidden_units': [32, 64, 128],
    'hidden_layers': [1, 2, 3],
    'batch_size': [4, 8, 16],
    'epochs': [50, 100, 150, 200]
}

grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring='neg_mean_squared_error', cv=3)
grid_result = grid.fit(X_train, y_train)
best_params = grid_result.best_params_
print(f"Mejores hiperparámetros: {best_params}")

best_model = grid_result.best_estimator_.model
train_mse = best_model.evaluate(X_train, y_train)
test_mse = best_model.evaluate(X_test, y_test)

print(f"MSE en el conjunto de entrenamiento: {train_mse}")
print(f"MSE en el conjunto de prueba: {test_mse}")

if test_mse / np.mean(y_test) < 0.1:
    print("El margen de error es aceptable, el modelo está listo para su uso.")
    best_model.save('modelo_viviendas.h5')
else:
    print("El margen de error es muy grande, necesitamos mejorar el modelo.")



# Preparación de los datos para el análisis OLS
X_train_Sm = sm.add_constant(X_train)

# Crear y entrenar el modelo OLS con los datos de entrenamiento
ls = sm.OLS(y_train, X_train_Sm).fit()

# Imprimir el resumen del modelo
print(ls.summary())