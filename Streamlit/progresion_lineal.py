import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Cargar datos
@st.cache
def load_data():
    return pd.read_csv('lung_cancer_data.csv')

data = load_data()

# Mostrar datos en la aplicación
st.write("Datos cargados:")
st.write(data.head())

# Seleccionar características y variable objetivo
features = ['Age', 'Smoking_Pack_Years', 'Tumor_Size_mm']
X = data[features]
y = data['Survival_Months']

# Dividir datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear y entrenar el modelo de regresión lineal
model = LinearRegression()
model.fit(X_train, y_train)

# Hacer predicciones
y_pred = model.predict(X_test)

# Evaluar el modelo
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Mostrar métricas
st.write(f"Error Cuadrático Medio (MSE): {mse}")
st.write(f"R² Score: {r2}")

# Entrada del usuario para nuevas predicciones
st.sidebar.header('Ingresar datos para predicción')
age = st.sidebar.number_input('Edad', min_value=0, value=50)
smoking_pack_years = st.sidebar.number_input('Años de Fumador', min_value=0, value=10)
tumor_size_mm = st.sidebar.number_input('Tamaño del Tumor (mm)', min_value=0, value=20)

# Realizar la predicción
input_data = pd.DataFrame([[age, smoking_pack_years, tumor_size_mm]], columns=features)
prediction = model.predict(input_data)

st.write(f"La tasa de supervivencia estimada es: {prediction[0]:.2f} meses")
