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

# Función para generar gráficos a partir de un archivo .exe
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
        
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
        
        # Ajustar el tamaño de 'explode' según el número de categorías
        explode = [0.1] * min(4, len(labels)) + [0] * (len(labels) - min(4, len(labels)))

        fig, ax = plt.subplots(figsize=(6, 6))

        # Gráfico de pastel
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        ax.axis('equal')  # Para que sea un círculo

        # Mostrar gráficos en la interfaz
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, pady=20)

    except Exception as e:
        messagebox.showerror("Error", f"Error al generar gráficos desde el archivo .exe: {e}")

# Función para generar gráficos a partir de un archivo .xlsx
def generate_charts_from_xlsx(file_path):
    try:
        # Leer datos del archivo .xlsx
        df = pd.read_excel(file_path, sheet_name=0)
        
        # Asumiendo que el DataFrame tiene dos columnas: 'Label' y 'Size'
        labels = df.iloc[:, 0].tolist()
        sizes = df.iloc[:, 1].tolist()
        
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
        
        # Ajustar el tamaño de 'explode' según el número de categorías
        explode = [0.1] * min(4, len(labels)) + [0] * (len(labels) - min(4, len(labels)))

        fig, ax = plt.subplots(figsize=(6, 6))

        # Gráfico de pastel
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        ax.axis('equal')  # Para que sea un círculo

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
