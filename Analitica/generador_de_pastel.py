import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para seleccionar un archivo
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe"), ("Excel files", "*.xlsx")])
    if file_path:
        file_var.set(file_path)
        if file_path.endswith('.exe'):
            generate_charts_from_exe(file_path)
        elif file_path.endswith('.xlsx'):
            generate_charts_from_xlsx(file_path)

# Función para generar gráficos de barras a partir de un archivo .exe
def generate_charts_from_exe(file_path):
    try:
        # Ejecutar el archivo .exe y capturar la salida
        output = subprocess.check_output([file_path], universal_newlines=True)
        
        # Parsear la salida para obtener datos estadísticos
        labels = []
        sizes = []
        
        for line in output.splitlines():
            label, size = line.split()
            labels.append(label)
            sizes.append(int(size))
        
        fig, ax = plt.subplots(figsize=(8, 6))

        # Gráfico de barras
        ax.bar(labels, sizes, color='skyblue')
        ax.set_xlabel('Categorías')
        ax.set_ylabel('Valores')
        ax.set_title('Gráfico de Barras')

        # Mostrar gráficos en la interfaz
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, pady=20)

    except Exception as e:
        messagebox.showerror("Error", f"Error al generar gráficos desde el archivo .exe: {e}")

# Función para generar gráficos de barras a partir de un archivo .xlsx
def generate_charts_from_xlsx(file_path):
    try:
        # Leer datos del archivo .xlsx
        df = pd.read_excel(file_path, sheet_name=0)
        
        # Asumiendo que el DataFrame tiene dos columnas: 'Label' y 'Size'
        labels = df.iloc[:, 0].tolist()
        sizes = df.iloc[:, 1].tolist()
        
        fig, ax = plt.subplots(figsize=(8, 6))

        # Gráfico de barras
        ax.bar(labels, sizes, color='skyblue')
        ax.set_xlabel('Categorías')
        ax.set_ylabel('Valores')
        ax.set_title('Gráfico de Barras')

        # Mostrar gráficos en la interfaz
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, pady=20)

    except Exception as e:
        messagebox.showerror("Error", f"Error al generar gráficos desde el archivo .xlsx: {e}")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Visualización de Archivos .exe y .xlsx")

file_var = tk.StringVar()

# Etiquetas y campos de entrada
tk.Label(root, text="Selecciona un archivo (.exe o .xlsx):").grid(row=0, column=0, padx=10, pady=10)
tk.Button(root, text="Seleccionar Archivo", command=select_file).grid(row=0, column=1, padx=10, pady=10)

root.mainloop()
