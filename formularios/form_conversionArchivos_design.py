import pandas as pd
import os
import subprocess
import tkinter as tk
from tkinter import Tk, Label, Button, filedialog, messagebox, Frame, LabelFrame, Radiobutton
from config import  COLOR_CUERPO_PRINCIPAL

class ConversorArchivosDesign():
    def __init__(self, panel_principal):
        self.panel_principal = panel_principal
        self.create_gui()
        self.selected_files = []
        self.output_directory = ""

    def create_gui(self):
        # Crear paneles: barra superior
        self.barra_superior = tk.Frame(self.panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)

        # Primer Label titulo de la interfaz 
        self.labelTitulo = tk.Label(
            self.barra_superior, text="Conversor de Archivos (Excel o CSV)", padx=10, pady=10)
        self.labelTitulo.config(fg="#A7AB95", font=("Anton", 28), bg=COLOR_CUERPO_PRINCIPAL)
        self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True)

        # Frame para la selección de formato
        format_frame = LabelFrame(self.panel_principal, text="Formato de entrada: ", padx=10, pady=10)
        format_frame.pack(pady=5, padx=90, fill="both")

        self.file_type = tk.StringVar(value="excel")

        excel_radio = Radiobutton(format_frame, text="Excel", variable=self.file_type, value="excel", command=self.update_file_type)
        excel_radio.pack(side="left", padx=5)

        csv_radio = Radiobutton(format_frame, text="CSV", variable=self.file_type, value="csv", command=self.update_file_type)
        csv_radio.pack(side="left", padx=5)

        # Frame para selección de archivos
        file_frame = LabelFrame(self.panel_principal, text="Seleccion de archivos: ", padx=10, pady=10)
        file_frame.pack(pady=5, padx=90, fill="both")

        self.choose_files_button = Button(file_frame, text="Seleccionar archivos", command=self.choose_files)
        self.choose_files_button.pack(pady=5, padx=10)

        self.file_listbox = tk.Listbox(file_frame, selectmode=tk.MULTIPLE, width=60, height=10)
        self.file_listbox.pack(pady=5, padx=5)

        # Frame para selección de archivos
        folder_frame = LabelFrame(self.panel_principal, text="Carpeta de destino: ", padx=10, pady=10)
        folder_frame.pack(pady=5, padx=90, fill="both")

        # Botón para seleccionar el directorio de salida
        self.select_output_button = Button(folder_frame, text="Seleccionar carpeta", command=self.choose_output_directory)
        self.select_output_button.pack(pady=5)

        # Label para mostrar la ruta del directorio de salida
        self.output_label = Label(folder_frame, text="No seleccionado", wraplength=800)
        self.output_label.pack(pady=5)

        # Botón para iniciar la conversión
        convert_button = Button(self.panel_principal, text="Convertir archivos", command=self.convert_files, width=20, bg="#A7AB95", fg="white", relief=tk.RAISED, cursor="hand2", pady=10)
        convert_button.pack(pady=5, padx=10)

    def update_file_type(self):
        # Actualiza la lista de archivos seleccionados si se cambia el tipo de archivo
        self.selected_files = []
        self.file_listbox.delete(0, tk.END)

    def choose_files(self):
        file_type = "*.xlsx" if self.file_type.get() == "excel" else "*.csv"
        self.selected_files = filedialog.askopenfilenames(filetypes=[(f"{self.file_type.get().capitalize()} files", file_type)])
        self.update_file_listbox()

    def update_file_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for file_path in self.selected_files:
            self.file_listbox.insert(tk.END, os.path.basename(file_path))

    def choose_output_directory(self):
        self.output_directory = filedialog.askdirectory()
        if self.output_directory:
            self.output_label.config(text=f"{self.output_directory}")
        else:
            messagebox.showwarning("Advertencia", "No se ha seleccionado un directorio de salida.")

    def convert_files(self):
        if not self.selected_files:
            messagebox.showwarning("Advertencia", "Por favor selecciona al menos un archivo.")
            return
        
        if not self.output_directory:
            messagebox.showwarning("Advertencia", "Por favor selecciona un directorio de salida.")
            return
        
        try:
            for file_path in self.selected_files:
                base_name, ext = os.path.splitext(os.path.basename(file_path))
                output_path = ""
                if self.file_type.get() == "excel":  # Convertir de Excel a CSV
                    if ext.lower() == ".xlsx":
                        df = pd.read_excel(file_path)
                        output_path = os.path.join(self.output_directory, base_name + ".csv")
                        df.to_csv(output_path, index=False)
                    else:
                        messagebox.showwarning("Advertencia", f"El archivo '{file_path}' no es un archivo Excel.")
                elif self.file_type.get() == "csv":  # Convertir de CSV a Excel
                    if ext.lower() == ".csv":
                        df = pd.read_csv(file_path)
                        output_path = os.path.join(self.output_directory, base_name + ".xlsx")
                        df.to_excel(output_path, index=False)
                    else:
                        messagebox.showwarning("Advertencia", f"El archivo '{file_path}' no es un archivo CSV.")

            messagebox.showinfo("Éxito", "Los archivos se han convertido correctamente.")

            # Abrir la carpeta de destino
            if os.name == 'nt':  # Para Windows
                os.startfile(self.output_directory)
            elif os.name == 'posix':  # Para Linux y macOS
                subprocess.Popen(['xdg-open', self.output_directory])

            # Limpiar campos después de la conversión
            self.file_listbox.delete(0, tk.END)
            self.selected_files = []
            self.output_directory = ""
            self.output_label.config(text="No seleccionado")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al convertir los archivos:\n{str(e)}")
