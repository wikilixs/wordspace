import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Análisis de Datos de Corazón", page_icon=":heart:")

# Título de la aplicación
st.title("Análisis de Datos de Corazón")

# Cargar los datos desde el archivo heart.xls (CSV)
data = pd.read_csv('heart.xls')

# Mostrar los primeros registros del dataset
st.subheader("Datos del archivo heart.xls")
st.write(data.head())

# Histograma de edades
st.subheader("Histograma de Edades")
plt.figure(figsize=(10, 6))
plt.hist(data['Age'], bins=20, edgecolor='black')
plt.xlabel('Edad')
plt.ylabel('Frecuencia')
plt.title('Distribución de Edades')
st.pyplot(plt)

# Gráfico de pastel de géneros
st.subheader("Gráfico de Pastel de Géneros")
gender_counts = data['Sex'].value_counts()
labels = ['Masculino' if x == 'M' else 'Femenino' for x in gender_counts.index]
plt.figure(figsize=(8, 8))
plt.pie(gender_counts, labels=labels, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Para asegurar que el gráfico de pastel sea circular
plt.title('Distribución de Géneros')
st.pyplot(plt)

# Ejecutar la aplicación: en la línea de comandos escribe `streamlit run tu_archivo.py`
    