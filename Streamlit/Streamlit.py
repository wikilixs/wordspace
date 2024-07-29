import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Título de la aplicación
st.title('Predicción de Cáncer de Pulmón')

# Cargar los datos
@st.cache
def load_data():
    dataset = pd.read_csv('dataset.csv')
    survey = pd.read_csv('survey lung cancer.csv')
    return dataset, survey

dataset, survey = load_data()

# Mostrar los datos
st.write('## Datos del Dataset')
st.write(dataset.head())

st.write('## Datos de la Encuesta')
st.write(survey.head())

# Preprocesamiento de los datos
def preprocess_data(df):
    df = df.copy()
    df['Gender'] = df['Gender'].map({'M': 1, 'F': 0})
    df['Lung Cancer'] = df['Lung Cancer'].map({'YES': 1, 'NO': 0})
    return df

dataset = preprocess_data(dataset)

# Seleccionar las características y el objetivo
X = dataset.drop('Lung Cancer', axis=1)
y = dataset['Lung Cancer']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
model = LogisticRegression()
model.fit(X_train, y_train)

# Hacer predicciones
y_pred = model.predict(X_test)

# Evaluar el modelo
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred)

st.write('### Evaluación del Modelo')
st.write(f'Precisión: {accuracy}')
st.write('### Matriz de Confusión')
st.write(cm)
st.write('### Informe de Clasificación')
st.write(report)

# Predicción con nuevos datos de la encuesta
def predict_cancer(data):
    data = preprocess_data(data)
    predictions = model.predict(data.drop('Lung Cancer', axis=1))
    return predictions

survey_predictions = predict_cancer(survey)

# Mostrar resultados de la predicción
st.write('## Predicciones para los Datos de la Encuesta')
survey['Predicción de Cáncer de Pulmón'] = survey_predictions
st.write(survey)

# Visualización de los resultados
fig, ax = plt.subplots()
ax.hist(survey_predictions, bins=2, edgecolor='k', alpha=0.7)
ax.set_xticks([0, 1])
ax.set_xticklabels(['No', 'Sí'])
ax.set_xlabel('Predicción de Cáncer de Pulmón')
ax.set_ylabel('Frecuencia')
st.pyplot(fig)

