import pandas as pd
import os
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox, StringVar, IntVar, Canvas
from tkinter.ttk import Progressbar
import string

# Función para convertir letras de columna a índice (A=0, B=1, etc.)
def col_letter_to_index(letter):
    letter = letter.upper()
    column_number = 0
    for char in letter:
        column_number = column_number * 26 + (ord(char) - ord('A')) + 1
    return column_number - 1

# Función para seleccionar la carpeta
def select_folder():
    folder_path = filedialog.askdirectory()
    folder_var.set(folder_path)

# Función para seleccionar la fila inicial y las columnas
def select_columns_row():
    global initial_row, columns_range
    try:
        initial_row = int(initial_row_var.get())
        columns_range_input = [col.strip() for col in columns_range_var.get().split(',')]
        if len(columns_range_input) == 2:
            start_col, end_col = columns_range_input

            # Convertir letras a índices de columna
            if start_col.isdigit():
                start_col_index = int(start_col) - 1
            else:
                start_col_index = col_letter_to_index(start_col)
                
            if end_col.isdigit():
                end_col_index = int(end_col) - 1
            else:
                end_col_index = col_letter_to_index(end_col)
                
            columns_range = list(range(start_col_index, end_col_index + 1))
        else:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Por favor, introduzca un rango de columnas válido en el formato inicio,fin.")
        return

    if not (0 <= initial_row):
        messagebox.showerror("Error", "La fila inicial debe ser un valor positivo.")
        return

    if not columns_range:
        messagebox.showerror("Error", "Debe introducir al menos una columna.")
        return

    load_data()

# Función para cargar datos desde los archivos Excel
def load_data():
    folder_path = folder_var.get()
    if not folder_path:
        messagebox.showerror("Error", "Debe seleccionar una carpeta.")
        return

    progress_bar['value'] = 0
    root.update_idletasks()

    data_frames = []
    files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

    for i, file in enumerate(files):
        file_path = os.path.join(folder_path, file)
        try:
            df = pd.read_excel(file_path, sheet_name='ITEM_O', header=None)
            df = df.iloc[initial_row-1:, columns_range]
            
            # Detectar y extraer fechas
            date_columns = df.select_dtypes(include=['datetime64']).columns.tolist()
            for col in date_columns:
                df[f'{col}_year'] = df[col].dt.year
                df[f'{col}_month'] = df[col].dt.month
                df[f'{col}_day'] = df[col].dt.day

            data_frames.append(df)
            progress_bar['value'] = (i+1)/len(files)*100
            root.update_idletasks()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar el archivo {file}: {e}")

    if not data_frames:
        messagebox.showinfo("Información", "No se encontraron datos para consolidar.")
        return

    final_df = pd.concat(data_frames, ignore_index=True)
    final_df_path = os.path.join(folder_path, 'dataset_final.xlsx')
    final_df.to_excel(final_df_path, index=False)
    messagebox.showinfo("Éxito", f"El dataset final se ha guardado en {final_df_path}")

# Configuración de la interfaz gráfica
root = Tk()
root.title("Proceso ETL")

folder_var = StringVar()
initial_row_var = StringVar()
columns_range_var = StringVar()

# Etiquetas y campos de entrada
Label(root, text="Selecciona la carpeta con archivos Excel:").grid(row=0, column=0, padx=10, pady=10)
Button(root, text="Seleccionar Carpeta", command=select_folder).grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Fila inicial (número):").grid(row=1, column=0, padx=10, pady=10)
Entry(root, textvariable=initial_row_var).grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Rango de columnas (separadas por coma):").grid(row=2, column=0, padx=10, pady=10)
Entry(root, textvariable=columns_range_var).grid(row=2, column=1, padx=10, pady=10)

Button(root, text="Cargar Datos", command=select_columns_row).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Barra de progreso
progress_bar = Progressbar(root, orient='horizontal', length=300, mode='determinate')
progress_bar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
