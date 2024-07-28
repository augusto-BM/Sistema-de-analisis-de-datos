import os
import tkinter as tk
from tkinter import Tk, Label, Button, filedialog, messagebox, Frame, LabelFrame, Listbox
import pandas as pd
import re
from config import COLOR_CUERPO_PRINCIPAL

class DuplicadosArchivosDesign():
    def __init__(self, panel_principal):
        self.panel_principal = panel_principal
        self.create_gui_duplicadosArchivos()
        self.selected_files = []
        self.reference_files = []
        self.output_folder = ""

    def create_gui_duplicadosArchivos(self):
        # Crear paneles: barra superior
        self.barra_superior = tk.Frame(self.panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)

        # Primer Label título de la interfaz 
        self.labelTitulo = tk.Label(
            self.barra_superior, text="Filtrar Duplicados", padx=10, pady=10)
        self.labelTitulo.config(fg="#A7AB95", font=("Anton", 28), bg=COLOR_CUERPO_PRINCIPAL)
        self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True)

        # Frame para la selección de archivos
        file_frame = LabelFrame(self.panel_principal, text="Selección de filtro", padx=10, pady=10)
        file_frame.pack(pady=5, padx=90, fill="both")

        self.choose_files_button = Button(file_frame, text="Seleccionar archivos", command=self.choose_files)
        self.choose_files_button.pack(pady=5, padx=10)

        self.file_listbox = Listbox(file_frame, selectmode=tk.MULTIPLE, width=60, height=2)
        self.file_listbox.pack(pady=5, padx=5)

        # Frame para selección de archivos de referencia
        ref_frame = LabelFrame(self.panel_principal, text="Selección de archivos de referencia", padx=10, pady=10)
        ref_frame.pack(pady=5, padx=90, fill="both")

        self.choose_ref_button = Button(ref_frame, text="Seleccionar archivos", command=self.choose_reference_files)
        self.choose_ref_button.pack(pady=5)

        self.ref_listbox = Listbox(ref_frame, selectmode=tk.MULTIPLE, width=60, height=6)
        self.ref_listbox.pack(pady=5, padx=5)

        # Definir el label para mostrar cantidad de archivos de referencia seleccionados
        self.ref_label = Label(ref_frame, text="No seleccionados")
        self.ref_label.pack(pady=5)

        # Frame para selección de carpeta de destino
        output_frame = LabelFrame(self.panel_principal, text="Seleccionar carpeta de destino", padx=10, pady=10)
        output_frame.pack(pady=5, padx=90, fill="both")

        self.choose_output_button = Button(output_frame, text="Seleccionar carpeta", command=self.choose_output_folder)
        self.choose_output_button.pack(pady=5)

        self.output_label = Label(output_frame, text="No seleccionado", wraplength=800)
        self.output_label.pack(pady=5)

        # Botón para iniciar la comparación y eliminar duplicados
        compare_button = Button(self.panel_principal, text="Filtrar duplicados", command=self.compare_and_remove_duplicates, width=30, bg="#A7AB95", fg="white", relief=tk.RAISED, cursor="hand2", pady=10)
        compare_button.pack(pady=5, padx=10)

    def choose_files(self):
        self.selected_files = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx")])
        self.update_file_listbox()

    def update_file_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for file_path in self.selected_files:
            self.file_listbox.insert(tk.END, os.path.basename(file_path))

    def choose_reference_files(self):
        self.reference_files = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx")])
        if self.reference_files:
            self.ref_listbox.delete(0, tk.END)
            for file_path in self.reference_files:
                self.ref_listbox.insert(tk.END, os.path.basename(file_path))
            self.ref_label.config(text=f"{len(self.reference_files)} archivo(s) seleccionado(s)")
        else:
            self.ref_label.config(text="No seleccionados")

    def choose_output_folder(self):
        self.output_folder = filedialog.askdirectory(title="Selecciona la carpeta para guardar los archivos de resultado")
        if self.output_folder:
            self.output_label.config(text=self.output_folder)
        else:
            self.output_label.config(text="No seleccionado")

    def normalize_column(self, df, column_index):
        # Función para normalizar los valores de una columna eliminando espacios en blanco y caracteres no numéricos
        df[column_index] = df[column_index].astype(str).apply(lambda x: re.sub(r'\D', '', x))
        return df

    def compare_and_remove_duplicates(self):
        # Método principal para comparar y eliminar duplicados
        if not self.selected_files:
            messagebox.showwarning("Advertencia", "Selecciona al menos un archivo de filtro.")
            return
        
        if not self.reference_files:
            messagebox.showwarning("Advertencia", "Selecciona al menos un archivo de referencia.")
            return

        if not self.output_folder:
            messagebox.showwarning("Advertencia", "Selecciona la carpeta de destino para guardar los archivos de resultado.")
            return

        success_messages = []  # Lista para almacenar los mensajes de éxito
        output_folder_to_open = self.output_folder  # Guardamos la carpeta de salida antes de limpiar la interfaz

        try:
            for ref_file in self.reference_files:
                ref_df = pd.read_excel(ref_file, header=None)
                ref_df = self.normalize_column(ref_df, 0)
                ref_df = ref_df[ref_df[0].str.len() == 9]
                
                unique_values_set = set()

                for file_path in self.selected_files:
                    curr_df = pd.read_excel(file_path, header=None)
                    curr_df = self.normalize_column(curr_df, 0)
                    curr_df = curr_df[curr_df[0].str.len() == 9]
                    unique_values_set.update(curr_df[0].tolist())

                initial_rows = len(ref_df)
                filtered_df = ref_df[~ref_df[0].isin(unique_values_set)]
                removed_duplicates = initial_rows - len(filtered_df)
                filtered_df = filtered_df.drop_duplicates()

                output_filename = os.path.splitext(os.path.basename(ref_file))[0] + "_sin_duplicados.xlsx"
                output_path = os.path.join(self.output_folder, output_filename)
                filtered_df[0] = filtered_df[0].astype(int)
                filtered_df.to_excel(output_path, index=False, header=False)

                # Agregar mensaje de éxito solo una vez por carpeta de salida
                success_messages.append(f"Se eliminaron {removed_duplicates} duplicados de: {os.path.basename(ref_file)}")

            # Mostrar resumen de éxito una vez al final
            success_messages.append(f"\n\tArchivos guardados en:\n{self.output_folder}")
            messagebox.showinfo("FILTRADO EXITOSO DE REGISTROS DUPLICADOS ", "\n".join(success_messages))

            # Limpiar la interfaz después de procesar
            self.selected_files = []
            self.reference_files = []
            self.file_listbox.delete(0, tk.END)
            self.ref_listbox.delete(0, tk.END)
            self.ref_label.config(text="No seleccionados")
            self.output_label.config(text="No seleccionado")
            self.output_folder = ""

            # Abrir la carpeta donde se guardaron los archivos si existe
            if os.path.exists(output_folder_to_open):
                os.startfile(output_folder_to_open)
            else:
                messagebox.showwarning("Advertencia", f"La carpeta de salida no existe:\n{output_folder_to_open}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al comparar y eliminar duplicados:\n{str(e)}")
