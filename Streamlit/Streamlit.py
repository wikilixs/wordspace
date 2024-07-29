import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.impute import SimpleImputer

# Título de la aplicación
st.title('Predicción de Cáncer de Pulmón')

# Cargar los datos
@st.cache
def load_data():
    dataset = pd.read_csv('dataset.csv')
    survey = pd.read_csv('survey lung cancer.csv')
    return dataset, survey

dataset, survey = load_data()

# Ajustar nombres de las columnas si es necesario
dataset.columns = dataset.columns.str.strip().str.replace(' ', '_').str.lower()
survey.columns = survey.columns.str.strip().str.replace(' ', '_').str.lower()

# Mostrar los nombres de las columnas
st.write('Nombres de las columnas del dataset:')
st.write(dataset.columns)

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
    df['gender'] = df['gender'].map({'M': 1, 'F': 0})
    df['lung_cancer'] = df['lung_cancer'].map({'YES': 1, 'NO': 0})
    
    # Manejar valores faltantes
    if method == 'Eliminar filas con valores faltantes':
        df.dropna(inplace=True)
    elif method == 'Imputar valores faltantes':
        imputer = SimpleImputer(strategy='mean')
        df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
    
    return df

dataset = preprocess_data(dataset, missing_value_handling)

# Verificar que haya datos disponibles
if dataset.empty:
    st.write('El dataset está vacío después de procesar los valores faltantes. Por favor, revisa los datos.')
else:
    # Seleccionar las características y el objetivo
    X = dataset.drop('lung_cancer', axis=1)
    y = dataset['lung_cancer']

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
    def predict_cancer(data, method):
        data = preprocess_data(data, method)
        if data.empty:
            return []
        predictions = model.predict(data.drop('lung_cancer', axis=1))
        return predictions

    survey_predictions = predict_cancer(survey, missing_value_handling)

    # Mostrar resultados de la predicción
    if survey.empty or not survey_predictions:
        st.write('No hay datos suficientes en la encuesta para hacer una predicción.')
    else:
        survey['Predicción de Cáncer de Pulmón'] = survey_predictions
        st.write('## Predicciones para los Datos de la Encuesta')
        st.write(survey)

        # Visualización de los resultados
        fig, ax = plt.subplots()
        ax.hist(survey_predictions, bins=2, edgecolor='k', alpha=0.7)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(['No', 'Sí'])
        ax.set_xlabel('Predicción de Cáncer de Pulmón')
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)
