import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

st.title('Regresión Lineal Simple con Streamlit')

# Crear un dataframe de ejemplo
st.write('## Datos de Ejemplo')
data = {
    'X': np.random.rand(100) * 10,
    'Y': np.random.rand(100) * 10
}
df = pd.DataFrame(data)
st.write(df)

st.write('## Ajustar Regresión Lineal')

X = df[['X']]
y = df['Y']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

st.write('### Coeficientes del Modelo')
st.write(f'Coeficiente: {model.coef_[0]}')
st.write(f'Intersección: {model.intercept_}')

st.write('### Métricas del Modelo')
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
st.write(f'Error Cuadrático Medio (MSE): {mse}')
st.write(f'Coeficiente de Determinación (R^2): {r2}')

# Visualizar resultados
fig, ax = plt.subplots()
ax.scatter(X_test, y_test, color='blue', label='Datos Reales')
ax.plot(X_test, y_pred, color='red', linewidth=2, label='Línea de Regresión')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.legend()
st.pyplot(fig)

