import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para seleccionar el archivo .exe
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
    if file_path:
        file_var.set(file_path)
        generate_charts(file_path)

# Función para generar gráficos
def generate_charts(file_path):
    try:
        # Ejecutar el archivo .exe y capturar la salida
        output = subprocess.check_output([file_path], universal_newlines=True)
        
        # Parsear la salida para obtener datos estadísticos
        # Asumiendo que la salida es del tipo:
        # "A 15\nB 30\nC 45\nD 10\n"
        labels = []
        sizes = []
        
        for line in output.splitlines():
            label, size = line.split()
            labels.append(label)
            sizes.append(int(size))
        
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
        explode = (0.1, 0, 0, 0)  # "Explota" el primer segmento si hay 4 categorías

        fig, ax = plt.subplots(figsize=(6, 6))

        # Gráfico de pastel
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        ax.axis('equal')  # Para que sea un círculo

        # Mostrar gráficos en la interfaz
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, pady=20)

    except Exception as e:
        messagebox.showerror("Error", f"Error al generar gráficos: {e}")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Visualización de Archivos .exe")

file_var = tk.StringVar()

# Etiquetas y campos de entrada
tk.Label(root, text="Selecciona un archivo .exe:").grid(row=0, column=0, padx=10, pady=10)
tk.Button(root, text="Seleccionar Archivo", command=select_file).grid(row=0, column=1, padx=10, pady=10)

root.mainloop()
