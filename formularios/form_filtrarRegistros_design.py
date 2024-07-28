import os
import tkinter as tk
from tkinter import Label, Button, filedialog, messagebox, Frame, LabelFrame, Listbox, Entry, font, Radiobutton, IntVar
import pandas as pd
import re
from config import COLOR_CUERPO_PRINCIPAL

class FiltrarRegistrosDesign():
    def __init__(self, panel_principal):
        self.panel_principal = panel_principal
        self.save_option = IntVar(value=0) 
        self.create_gui_filtrarRegistros()
        self.selected_files = []
        self.output_folder = ""

    def create_gui_filtrarRegistros(self):
        # Crear paneles: barra superior
        self.barra_superior = tk.Frame(self.panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)

        # Primer Label título de la interfaz 
        self.labelTitulo = tk.Label(
            self.barra_superior, text="Filtrar Registros", padx=10, pady=10)
        self.labelTitulo.config(fg="#A7AB95", font=("Anton", 28), bg=COLOR_CUERPO_PRINCIPAL)
        self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True)

        # Frame para la selección de archivos
        file_frame = LabelFrame(self.panel_principal, text="Selección de archivos", padx=10, pady=10)
        file_frame.pack(pady=5, padx=90, fill="both")

        self.choose_files_button = Button(file_frame, text="Seleccionar archivos", command=self.choose_files)
        self.choose_files_button.pack(pady=5, padx=10)

        self.file_listbox = Listbox(file_frame, selectmode=tk.MULTIPLE, width=60, height=5)
        self.file_listbox.pack(pady=5, padx=5)

        # Frame para búsqueda por columna y valor
        search_frame = LabelFrame(self.panel_principal, text="Búsqueda por columna y valor", padx=10, pady=10)
        search_frame.pack(pady=5, padx=90, fill="both")

        self.column_label = Label(search_frame, text="Selecciona columnas:")
        self.column_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.column_entry = Entry(search_frame, width=30) 
        self.column_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.column_entry.bind("<KeyRelease>", self.validate_column_input)  # Validar la entrada

        bold_italic_font = font.Font(self.column_label, self.column_label.cget("font"))
        bold_italic_font.configure(weight="bold", slant="italic")
        self.column_label2 = Label(search_frame, text="(separadas por: ´ ; ´)", font=bold_italic_font, fg="#263AA0")
        self.column_label2.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.value_label = Label(search_frame, text="Ingresa el valor a buscar:")
        self.value_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.value_entry = Entry(search_frame, width=30)
        self.value_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Frame para selección de carpeta de destino
        output_frame = LabelFrame(self.panel_principal, text="Seleccionar carpeta de destino", padx=10, pady=10)
        output_frame.pack(pady=5, padx=90, fill="both")

        self.choose_output_button = Button(output_frame, text="Seleccionar carpeta", command=self.choose_output_folder)
        self.choose_output_button.pack(pady=5)

        self.output_label = Label(output_frame, text="No seleccionado", wraplength=800)
        self.output_label.pack(pady=5)
        
        # Frame para selección de opciones de guardado
        save_frame = LabelFrame(self.panel_principal, text="Opciones de Guardado", padx=10, pady=10)
        save_frame.pack(pady=5, padx=90, fill="both")

        # Configurar columnas para que se expandan
        save_frame.columnconfigure(0, weight=1)
        save_frame.columnconfigure(1, weight=1)

        self.radio_button_individual = Radiobutton(save_frame, text="Archivos individuales", variable=self.save_option, value=0)
        self.radio_button_individual.grid(row=0, column=0, padx=10, pady=1, sticky="e")

        self.radio_button_acumulado = Radiobutton(save_frame, text="Archivos agrupados", variable=self.save_option, value=1)
        self.radio_button_acumulado.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.radio_button_individual.select()

        # Botón para iniciar la búsqueda y generar archivos
        search_button = Button(self.panel_principal, text="Filtrar registros", command=self.search_and_generate_files, width=30, bg="#A7AB95", fg="white", relief=tk.RAISED, cursor="hand2", pady=10)
        search_button.pack(pady=2, padx=10)

    def choose_files(self):
        self.selected_files = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx")])
        self.update_file_listbox()

    def update_file_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for file_path in self.selected_files:
            self.file_listbox.insert(tk.END, os.path.basename(file_path))

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

    def validate_column_input(self, event):
        current_value = self.column_entry.get().strip().upper()  # Convertir a mayúsculas y quitar espacios en blanco
        if not current_value.replace(';', '').isalpha():
            self.column_entry.delete(0, 'end')
            messagebox.showwarning("Atención", "Por favor ingresa solo letras para las columnas separadas por ;.")

    def search_and_generate_files(self):
        # Validación de selección de archivos
        if not self.selected_files:
            messagebox.showwarning("Advertencia", "Selecciona al menos un archivo.")
            return
        
        # Validación de búsqueda por columnas y valor
        columns_input = self.column_entry.get().strip().upper()  # Convertir a mayúsculas y quitar espacios en blanco
        if not columns_input:
            messagebox.showwarning("Advertencia", "No puedes dejar vacío la columna buscada.")
            return
        
        columns_to_search = columns_input.split(';')
        column_indices = []
        for col in columns_to_search:
            try:
                column_index = self.convert_column_letter_to_index(col.strip())
                column_indices.append(column_index)
            except ValueError:
                messagebox.showwarning("Advertencia", f"La columna '{col.strip()}' no es válida.")
                return
        
        value_value = self.value_entry.get().strip()
        if not value_value:
            messagebox.showwarning("Advertencia", "No puedes dejar vacío el valor a buscar.")
            return
        
        # Validación de selección de carpeta de destino
        if not self.output_folder:
            messagebox.showwarning("Advertencia", "Selecciona la carpeta de destino para guardar los archivos de resultado.")
            return

        # Si todas las validaciones son exitosas, procede con la búsqueda y generación de archivos
        try:
            success_messages = []  # Lista para almacenar los mensajes de éxito

            output_folder_to_open = self.output_folder  # Guardamos la carpeta de salida antes de limpiar la interfaz

            accumulated_results = pd.DataFrame()  # DataFrame para acumular todos los resultados
            found_results = False  # Bandera para indicar si se encontraron resultados en algún archivo

            for file_path in self.selected_files:
                try:
                    df = pd.read_excel(file_path, header=None)
                    
                    # Normalizar los valores en las columnas de interés
                    for column_index in column_indices:
                        df[column_index] = df[column_index].astype(str).apply(lambda x: x.strip())  # Eliminar espacios en blanco al inicio y fin

                    # Realizar la búsqueda con case=False para ignorar mayúsculas y minúsculas
                    condition = False
                    for column_index in column_indices:
                        condition |= df[column_index].str.contains(re.escape(value_value), case=False, na=False)
                    
                    filtered_df = df[condition]

                    if not filtered_df.empty:
                        found_results = True  # Se encontraron resultados en este archivo
                        
                        if self.save_option.get() == 0:
                            # Guardar el DataFrame filtrado en un archivo Excel individual
                            output_filename = os.path.splitext(os.path.basename(file_path))[0] + f"_filtrado_{value_value}.xlsx"
                            output_path = os.path.join(self.output_folder, output_filename)
                            filtered_df.to_excel(output_path, index=False, header=False)
                            success_messages.append(f"{len(filtered_df)} registros encontrados en {os.path.basename(file_path)}")
                        else:
                            # Acumular los resultados en un solo DataFrame
                            accumulated_results = pd.concat([accumulated_results, filtered_df], ignore_index=True)
                            success_messages.append(f"{len(filtered_df)} registros encontrados en {os.path.basename(file_path)}")
                    else:
                        success_messages.append(f"Sin resultados en {os.path.basename(file_path)}")

                except Exception as e:
                    success_messages.append(f"Error al procesar el archivo: {os.path.basename(file_path)}")
                    success_messages.append(f"Error detallado: {str(e)}")

            if found_results:
                # Mostrar resumen de éxito solo si se encontraron resultados en al menos un archivo
                if self.save_option.get() == 1 and not accumulated_results.empty:
                    # Guardar todos los resultados acumulados en un solo archivo Excel
                    output_filename = f"resultados_agrupados_{value_value}.xlsx"
                    output_path = os.path.join(self.output_folder, output_filename)
                    accumulated_results.to_excel(output_path, index=False, header=False)
                    success_messages.append(f"\nRegistros agrupados en el archivo:\n\t{output_filename}")
                elif self.save_option.get() == 1 and accumulated_results.empty:
                    success_messages.append("No se encontraron resultados para los archivos seleccionados.")

                success_messages.append(f"\n\tSe guardó en la ruta:\n{self.output_folder}")
                messagebox.showinfo("Búsqueda Exitosa", "\n".join(success_messages))

                # Limpiar la interfaz después de procesar
                self.clear_interface()

                # Abrir la carpeta donde se guardaron los archivos si existe
                if os.path.exists(output_folder_to_open):
                    os.startfile(output_folder_to_open)
                else:
                    messagebox.showwarning("Advertencia", f"La carpeta de salida no existe:\n{output_folder_to_open}")

            else:
                # Mostrar mensaje de que no se encontraron resultados
                messagebox.showinfo("Búsqueda Exitosa", "No se encontraron resultados en ninguno de los archivos seleccionados.")

                # No limpiar la interfaz en este caso para permitir al usuario corregir y volver a intentar

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al buscar y generar archivos:\n{str(e)}")


    def clear_interface(self):
        # Función para limpiar la interfaz después de procesar
        self.column_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
        self.file_listbox.delete(0, tk.END)
        self.output_label.config(text="No seleccionado")

    def convert_column_letter_to_index(self, col_letter):
        # Función para convertir letras de columna (como 'A', 'B', 'C', ...) a índices numéricos (0, 1, 2, ...)
        base = ord('A')
        col_letter = col_letter.upper()
        num = 0
        for c in col_letter:
            if 'A' <= c <= 'Z':
                num = num * 26 + (ord(c) - base + 1)
            else:
                raise ValueError(f"La columna '{col_letter}' no es válida.")
        return num - 1  # Restar 1 para que sea base 0 (como en Python)
