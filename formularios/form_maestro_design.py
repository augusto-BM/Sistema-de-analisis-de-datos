import tkinter as tk
from tkinter import font
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import util.util_ventana as util_ventana
import util.util_imagenes as util_img

from formularios.form_graficas_design import FormularioGraficasDesign
from formularios.form_sitio_construccion import FormularioSitioConstruccionDesign
from formularios.form_info_design import FormularioInfoDesign
from formularios.form_divisorArchivos_design import DivisorArchivosDesign
from formularios.form_conversionArchivos_design import ConversorArchivosDesign
from formularios.form_datosDuplicados_design import DuplicadosArchivosDesign
from formularios.form_filtrarRegistros_design import FiltrarRegistrosDesign
from PIL import Image, ImageTk

class FormularioMaestroDesign(tk.Tk):

    def __init__(self):
        super().__init__()

        self.logo = util_img.leer_imagen("./imagenes/jbg_operator_slider.jpeg", (860, 306))
        self.perfil = util_img.leer_imagen("./imagenes/admin_logo.png", (100, 100))
        self.img_sitio_construccion = util_img.leer_imagen("./imagenes/sitio_construccion.png", (200, 200))
        self.icono_menu_lateral = ImageTk.PhotoImage(Image.open("./imagenes/barra-de-menus.png").resize((30, 30)))

        self.config_window()
        self.paneles()
        self.controles_barra_superior()        
        self.controles_menu_lateral()
        self.controles_cuerpo()
    
    def config_window(self):
        # Configuración inicial de la ventana
        self.title('Sistema de analisis de datos')
        self.iconbitmap("./imagenes/logo.ico")
        w, h = 1024, 650        
        util_ventana.centrar_ventana(self, w, h)     
        self.resizable(False, False)
   

    def paneles(self):        
         # Crear paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(
            self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')      

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False) 
        
        self.cuerpo_principal = tk.Frame(
            self, bg=COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)
    
    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = font.Font(family='FontAwesome', size=12)

        # Etiqueta de título
        self.labelTitulo = tk.Label(self.barra_superior, text="Administrador")
        self.labelTitulo.config(fg="#fff", font=(
            "Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        # Botón del menú lateral
        self.buttonMenuLateral = tk.Button(self.barra_superior, image=self.icono_menu_lateral,
                                           command=self.toggle_panel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.buttonMenuLateral.pack(side=tk.LEFT)

        # Etiqueta de informacion
        self.labelTitulo = tk.Label(
            self.barra_superior, text="soporte@escandiobusiness.com")
        self.labelTitulo.config(fg="#fff", font=(
            "Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=30)
        self.labelTitulo.pack(side=tk.RIGHT)
    
    def controles_menu_lateral(self):
        # Configuración del menú lateral
        ancho_menu = 20
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=10)
         
         # Etiqueta de perfil
        self.labelPerfil = tk.Label(
            self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL)
        self.labelPerfil.pack(side=tk.TOP, pady=10)

        # Botones del menú lateral
        self.buttonConversorArchivos = tk.Button(self.menu_lateral)        
        self.buttonDivisorArchivos = tk.Button(self.menu_lateral)        
        self.buttonFiltrarDuplicados = tk.Button(self.menu_lateral)
        self.buttonFiltrarRegistros = tk.Button(self.menu_lateral)
        self.buttonInfo = tk.Button(self.menu_lateral)        
        self.buttonSettings = tk.Button(self.menu_lateral)

        buttons_info = [
            ("Conversor", "\uf109", self.buttonConversorArchivos,self.abrir_conversor_archivos ),
            ("Divisor de archivos", "\uf007", self.buttonDivisorArchivos,self.abrir_panel_divisor_archivos),
            ("Filtrar duplicados", "\uf107", self.buttonFiltrarDuplicados,self.abrir_panel_filtrarDatos),
            ("Filtrar registros", "\uf104", self.buttonFiltrarRegistros,self.abrir_panel_filtrar_registros)
        ]


        for text, icon, button,comando in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu,comando)                    
    
    def controles_cuerpo(self):
        # Texto de bienvenida
        texto_bienvenida = "👈🏼 Hola, soporte bienvenido !!! 🖐🏼"
        label_bienvenida = tk.Label(self.cuerpo_principal, text=texto_bienvenida, 
                                    font=("Anton", 30), fg="#A7AB95", bg=COLOR_CUERPO_PRINCIPAL)
        label_bienvenida.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        # Imagen en el cuerpo principal
        label_imagen = tk.Label(self.cuerpo_principal, image=self.logo, bg=COLOR_CUERPO_PRINCIPAL)
        label_imagen.place(relx=0.5, rely=0.5, anchor=tk.CENTER)    
  
    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu, comando):
        button.config(text=f"  {icon}    {text}", anchor="w", font=font_awesome,
                      bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu,
                      command = comando)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg='white')

    def toggle_panel(self):
        # Alternar visibilidad del menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')

    # ABRIR INTERFAZ DE GRAFICAS
    def abrir_panel_graficas(self):   
        self.limpiar_panel(self.cuerpo_principal)     
        FormularioGraficasDesign(self.cuerpo_principal)   
        
    
    # ABRIR INTERFAZ DE CONVERSOR DE ARCHIVOS
    def abrir_conversor_archivos(self):
        self.limpiar_panel(self.cuerpo_principal)  
        ConversorArchivosDesign(self.cuerpo_principal) 

    # ABRIR INTERFAZ DE DIVISOR DE ARCHIVOS
    def abrir_panel_divisor_archivos(self):
        self.limpiar_panel(self.cuerpo_principal)  
        DivisorArchivosDesign(self.cuerpo_principal) 

    # ABRIR INTERFAZ DE FILTRAR DATOS
    def abrir_panel_filtrarDatos(self):
        self.limpiar_panel(self.cuerpo_principal)  
        DuplicadosArchivosDesign(self.cuerpo_principal) 

    # ABRIR INTERFAZ DE FILTRAR REGISTROS
    def abrir_panel_filtrar_registros(self):
        self.limpiar_panel(self.cuerpo_principal)  
        FiltrarRegistrosDesign(self.cuerpo_principal) 

    def abrir_panel_en_construccion(self):   
        self.limpiar_panel(self.cuerpo_principal)     
        FormularioSitioConstruccionDesign(self.cuerpo_principal,self.img_sitio_construccion) 

    def abrir_panel_info(self):           
        FormularioInfoDesign()                    

    def limpiar_panel(self,panel):
    # Función para limpiar el contenido del panel
        for widget in panel.winfo_children():
            widget.destroy()