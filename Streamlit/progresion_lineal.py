import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Configuración de la página
st.set_page_config(page_title="Análisis de Datos de Corazón", page_icon=":heart:")

# Título de la aplicación
st.title("Análisis de Datos de Corazón")

# Cargar los datos desde el archivo heart.csv
data = pd.read_csv('heart.csv')

# Convertir variables categóricas a numéricas
le = LabelEncoder()
data['Sex'] = le.fit_transform(data['Sex'])
data['ChestPainType'] = le.fit_transform(data['ChestPainType'])
data['RestingECG'] = le.fit_transform(data['RestingECG'])
data['ExerciseAngina'] = le.fit_transform(data['ExerciseAngina'])
data['ST_Slope'] = le.fit_transform(data['ST_Slope'])

# Definir características y objetivo
X = data.drop('HeartDisease', axis=1)
y = data['HeartDisease']

# Entrenar el modelo de Random Forest
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X, y)

# Obtener importancias de características
feature_importances = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values(ascending=False)

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
plt.figure(figsize=(8, 8))
plt.pie(gender_counts, labels=['M', 'F'], autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Para asegurar que el gráfico de pastel sea circular
plt.title('Distribución de Géneros')
st.pyplot(plt)

# Gráfico de barras de tipos de dolor torácico
st.subheader("Frecuencia de Cada Tipo de Dolor Torácico")
chest_pain_counts = data['ChestPainType'].value_counts()
plt.figure(figsize=(10, 6))
sns.barplot(x=chest_pain_counts.index, y=chest_pain_counts.values, palette='viridis')
plt.xlabel('Tipo de Dolor Torácico')
plt.ylabel('Frecuencia')
plt.title('Frecuencia de Cada Tipo de Dolor Torácico')
plt.xticks(ticks=chest_pain_counts.index, labels=['ATA', 'NAP', 'ASY', 'TA'])
st.pyplot(plt)

# Histograma de niveles de colesterol
st.subheader("Histograma de Niveles de Colesterol")
plt.figure(figsize=(10, 6))
plt.hist(data['Cholesterol'], bins=20, edgecolor='black')
plt.xlabel('Nivel de Colesterol')
plt.ylabel('Frecuencia')
plt.title('Distribución de Niveles de Colesterol')
st.pyplot(plt)

# Gráfico de barras de individuos con y sin enfermedad cardíaca
st.subheader("Cantidad de Individuos con y sin Enfermedad Cardíaca")
heart_disease_counts = data['HeartDisease'].value_counts()
plt.figure(figsize=(10, 6))
sns.barplot(x=heart_disease_counts.index, y=heart_disease_counts.values, palette='magma')
plt.xlabel('Enfermedad Cardíaca (0: No, 1: Sí)')
plt.ylabel('Cantidad de Individuos')
plt.title('Cantidad de Individuos con y sin Enfermedad Cardíaca')
st.pyplot(plt)

# Gráficos de barras apiladas para la relación entre tipo de dolor torácico y enfermedad cardíaca
st.subheader("Relación entre Tipo de Dolor Torácico y Enfermedad Cardíaca")
stacked_bar_data = data.groupby(['ChestPainType', 'HeartDisease']).size().unstack()
stacked_bar_data.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='viridis')
plt.xlabel('Tipo de Dolor Torácico')
plt.ylabel('Cantidad de Individuos')
plt.title('Relación entre Tipo de Dolor Torácico y Enfermedad Cardíaca')
plt.xticks(ticks=stacked_bar_data.index, labels=['ATA', 'NAP', 'ASY', 'TA'])
st.pyplot(plt)

# Heatmap de correlación
st.subheader("Heatmap de Correlación")
plt.figure(figsize=(12, 10))
numeric_data = data.select_dtypes(include=['float64', 'int64'])
correlation_matrix = numeric_data.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Mapa de Calor de Correlaciones')
st.pyplot(plt)

# Gráfico de importancias de características del modelo Random Forest
st.subheader("Importancia de Características (Random Forest)")
plt.figure(figsize=(12, 8))
sns.barplot(x=feature_importances, y=feature_importances.index, palette='viridis')
plt.xlabel('Importancia')
plt.ylabel('Características')
plt.title('Importancia de Características (Random Forest)')
st.pyplot(plt)

# Mostrar los primeros registros del dataset
st.subheader("Datos del archivo heart.csv")
st.write(data.head())

# Ejecutar la aplicación: en la línea de comandos escribe `streamlit run tu_archivo.py`
