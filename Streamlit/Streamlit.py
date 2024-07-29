import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.impute import SimpleImputer
import numpy as np

# Título de la aplicación
st.title('Predicción de Cáncer de Pulmón')

# Cargar los datos
@st.cache
def load_data():
    # Cargar solo el archivo de encuesta
    survey = pd.read_csv('survey lung cancer.csv')
    return survey

survey = load_data()

# Ajustar nombres de las columnas para que coincidan con el formato esperado
survey.columns = survey.columns.str.strip().str.replace(' ', '_').str.lower()

# Mostrar los nombres de las columnas
st.write('Nombres de las columnas de la encuesta:')
st.write(survey.columns)

# Seleccionar el método para manejar valores faltantes
missing_value_handling = st.selectbox(
    'Seleccione el método para manejar valores faltantes:',
    ('Eliminar filas con valores faltantes', 'Imputar valores faltantes')
)

# Preprocesamiento de los datos
def preprocess_data(df, method):
    df = df.copy()
    # Mapear valores de GENDER y LUNG_CANCER a formatos binarios
    df['gender'] = df['gender'].map({1: 1, 0: 0})  # Mapeo para GENDER
    df['lung_cancer'] = df['lung_cancer'].map({1: 1, 2: 0})  # Mapeo para LUNG_CANCER
    
    # Mostrar el DataFrame antes de manejar valores faltantes
    st.write('DataFrame antes de manejar valores faltantes:')
    st.write(df.head())

    # Manejar valores faltantes
    if method == 'Eliminar filas con valores faltantes':
        df.dropna(inplace=True)
    elif method == 'Imputar valores faltantes':
        imputer = SimpleImputer(strategy='mean')
        df[df.columns.difference(['lung_cancer'])] = imputer.fit_transform(df[df.columns.difference(['lung_cancer'])])
    
    # Mostrar el DataFrame después de manejar valores faltantes
    st.write('DataFrame después de manejar valores faltantes:')
    st.write(df.head())
    
    return df

survey_preprocessed = preprocess_data(survey, missing_value_handling)

# Verificar que haya datos disponibles
if survey_preprocessed.empty:
    st.write('El dataset está vacío después de procesar los valores faltantes. Por favor, revisa los datos.')
else:
    # Seleccionar las características y el objetivo
    X = survey_preprocessed.drop('lung_cancer', axis=1)
    y = survey_preprocessed['lung_cancer']

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrenar el modelo
    model = LogisticRegression(max_iter=1000)
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
    def predict_cancer(data, method):
        data_preprocessed = preprocess_data(data, method)
        if data_preprocessed.empty:
            return np.array([])  # Retorna un array vacío si no hay datos
        X_new = data_preprocessed.drop('lung_cancer', axis=1)
        # Verifica el tamaño de X_new antes de hacer la predicción
        st.write(f'Tamaño de X_new para predicción: {X_new.shape}')
        predictions = model.predict(X_new)
        return predictions

    survey_predictions = predict_cancer(survey, missing_value_handling)

    # Mostrar resultados de la predicción
    st.write(f'Tamaño de survey_predictions: {len(survey_predictions)}')
    st.write(f'Tamaño de survey_preprocessed: {survey_preprocessed.shape[0]}')

    if survey_preprocessed.empty or len(survey_predictions) == 0:
        st.write('No hay datos suficientes en la encuesta para hacer una predicción.')
    else:
        if len(survey_predictions) != survey_preprocessed.shape[0]:
            st.write('Error: El número de predicciones no coincide con el número de filas en el dataset.')
        else:
            survey_preprocessed['Predicción_de_Cáncer_de_Pulmón'] = survey_predictions
            st.write('## Predicciones para los Datos de la Encuesta')
            st.write(survey_preprocessed)

            # Visualización de los resultados
            fig, ax = plt.subplots()
            ax.hist(survey_preprocessed['Predicción_de_Cáncer_de_Pulmón'], bins=2, edgecolor='k', alpha=0.7)
            ax.set_xticks([0, 1])
            ax.set_xticklabels(['No', 'Sí'])
            ax.set_xlabel('Predicción de Cáncer de Pulmón')
            ax.set_ylabel('Frecuencia')
            st.pyplot(fig)
