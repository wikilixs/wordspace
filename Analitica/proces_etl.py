import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
from tkinter import *
import threading

# Función para cargar y consolidar los archivos Excel
def cargar_archivos_excel(carpeta, columnas, fila_inicial):
    archivos = [f for f in os.listdir(carpeta) if f.endswith('.xlsx')]
    dataframes = []

    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta, archivo)
        df = pd.read_excel(ruta_archivo, sheet_name="ITEM_O", usecols=columnas, skiprows=range(fila_inicial-1))
        dataframes.append(df)

    return pd.concat(dataframes, ignore_index=True)

# Función para actualizar la barra de progreso
def actualizar_progreso(total, actual):
    porcentaje = (actual / total) * 100
    progress_bar['value'] = porcentaje
    ventana.update_idletasks()

# Función para iniciar el proceso ETL
def iniciar_proceso():
    # Obtener carpeta
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta con archivos Excel")

    if not carpeta:
        messagebox.showwarning("Advertencia", "Debe seleccionar una carpeta")
        return

    # Obtener columnas
    columnas = simpledialog.askstring("Columnas", "Ingresa el rango de columnas (ejemplo: A:D)")

    if not columnas:
        messagebox.showwarning("Advertencia", "Debe ingresar el rango de columnas")
        return

    # Obtener fila inicial
    fila_inicial = simpledialog.askinteger("Fila Inicial", "Ingresa el número de la fila inicial")

    if not fila_inicial:
        messagebox.showwarning("Advertencia", "Debe ingresar la fila inicial")
        return

    # Iniciar proceso en un hilo separado
    def etl_proceso():
        archivos = [f for f in os.listdir(carpeta) if f.endswith('.xlsx')]
        total_archivos = len(archivos)

        if total_archivos == 0:
            messagebox.showwarning("Advertencia", "No se encontraron archivos Excel en la carpeta seleccionada")
            return

        dataframes = []
        for i, archivo in enumerate(archivos):
            ruta_archivo = os.path.join(carpeta, archivo)
            df = pd.read_excel(ruta_archivo, sheet_name="ITEM_O", usecols=columnas, skiprows=range(fila_inicial-1))
            dataframes.append(df)
            actualizar_progreso(total_archivos, i + 1)

        dataset_final = pd.concat(dataframes, ignore_index=True)

        # Mostrar el dataset final en una nueva ventana
        mostrar_dataset(dataset_final)

    hilo = threading.Thread(target=etl_proceso)
    hilo.start()

# Función para mostrar el dataset final
def mostrar_dataset(dataset):
    ventana_dataset = Toplevel(ventana)
    ventana_dataset.title("Dataset Final")

    # Crear un widget Treeview para mostrar el DataFrame
    tree = ttk.Treeview(ventana_dataset)
    tree.pack(fill=BOTH, expand=True)

    # Definir columnas
    tree["column"] = list(dataset.columns)
    tree["show"] = "headings"

    for columna in tree["column"]:
        tree.heading(columna, text=columna)

    # Insertar datos en el Treeview
    for index, row in dataset.iterrows():
        tree.insert("", "end", values=list(row))

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Proceso ETL")

# Crear un botón para iniciar el proceso ETL
boton_iniciar = tk.Button(ventana, text="Iniciar Proceso ETL", command=iniciar_proceso)
boton_iniciar.pack(pady=20)

# Crear una barra de progreso
progress_bar = ttk.Progressbar(ventana, orient=HORIZONTAL, length=300, mode='determinate')
progress_bar.pack(pady=20)

ventana.mainloop()
