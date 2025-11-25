import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from analizador.lexico import Lexico
from gui.ventana_simbolos import VentanaSimbolos


class IndexCompilador:
    """
    Interfaz principal del analizador léxico.
    Contiene áreas de texto de entrada y salida, y botones de control.
    """
    
    def __init__(self):
        """Inicializa la ventana principal de la aplicación."""
        self.lexico = Lexico()
        self.archivo_entrada_path = None
        self.ventana_simbolos = None
        
        self.root = tk.Tk()
        self.root.title("Analizador Léxico")
        self.root.geometry("900x600")
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea los componentes de la interfaz gráfica."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self._crear_areas_texto(main_frame)
        self._crear_botones(main_frame)
    
    def _crear_areas_texto(self, parent):
        """
        Crea las áreas de texto de entrada y salida.
        
        Args:
            parent: Frame padre
        """
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Área de texto de entrada
        input_label = ttk.Label(text_frame, text="Texto de Entrada")
        input_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        input_frame = ttk.Frame(text_frame)
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.texto_entrada = tk.Text(input_frame, wrap=tk.WORD, width=40, height=20)
        input_scrollbar = ttk.Scrollbar(input_frame, orient=tk.VERTICAL, command=self.texto_entrada.yview)
        self.texto_entrada.configure(yscrollcommand=input_scrollbar.set)
        
        self.texto_entrada.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Área de texto de salida
        output_label = ttk.Label(text_frame, text="Texto de Salida")
        output_label.grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        
        output_frame = ttk.Frame(text_frame)
        output_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.texto_salida = tk.Text(output_frame, wrap=tk.WORD, width=40, height=20, state=tk.DISABLED)
        output_scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self.texto_salida.yview)
        self.texto_salida.configure(yscrollcommand=output_scrollbar.set)
        
        self.texto_salida.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar pesos de la cuadrícula
        text_frame.columnconfigure(0, weight=1)
        text_frame.columnconfigure(1, weight=1)
        text_frame.rowconfigure(1, weight=1)
    
    def _crear_botones(self, parent):
        """
        Crea los botones de control.
        
        Args:
            parent: Frame padre
        """
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X)
        
        btn_cargar = ttk.Button(buttons_frame, text="Cargar Archivo", command=self._cargar_archivo)
        btn_cargar.pack(side=tk.LEFT, padx=5)
        
        btn_tabla = ttk.Button(buttons_frame, text="Tabla de Símbolos", command=self._mostrar_tabla_simbolos)
        btn_tabla.pack(side=tk.LEFT, padx=5)
        
        btn_analizar = ttk.Button(buttons_frame, text="Analizar", command=self._analizar)
        btn_analizar.pack(side=tk.LEFT, padx=5)
    
    def _cargar_archivo(self):
        """Carga un archivo en el área de texto de entrada."""
        file_path = self._obtener_ruta_archivo()
        if file_path:
            self._cargar_contenido(file_path)
    
    def _obtener_ruta_archivo(self):
        """
        Obtiene la ruta del archivo desde el diálogo de archivos.
        
        Returns:
            str or None: Ruta del archivo seleccionado o None
        """
        entradas_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'entradas')
        archivo_inicial = os.path.join(entradas_dir, 'texto.txt') if os.path.exists(entradas_dir) else None
        
        if archivo_inicial and os.path.exists(archivo_inicial):
            return filedialog.askopenfilename(
                initialdir=entradas_dir,
                initialfile='texto.txt',
                title="Seleccionar archivo",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
        else:
            return filedialog.askopenfilename(
                title="Seleccionar archivo",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
    
    def _cargar_contenido(self, file_path):
        """
        Carga el contenido del archivo en el área de texto de entrada.
        
        Args:
            file_path (str): Ruta del archivo a cargar
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
                self.texto_entrada.delete(1.0, tk.END)
                self.texto_entrada.insert(1.0, contenido)
                self.archivo_entrada_path = file_path
                messagebox.showinfo("Éxito", "Archivo cargado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")
    
    def _mostrar_tabla_simbolos(self):
        """Muestra la ventana de la tabla de símbolos."""
        if self.ventana_simbolos is None or not self.ventana_simbolos.ventana.winfo_exists():
            self.ventana_simbolos = VentanaSimbolos(self.root, self.lexico.obtener_tabla_simbolos())
        else:
            self.ventana_simbolos.actualizar_tabla(self.lexico.obtener_tabla_simbolos())
            self.ventana_simbolos.ventana.lift()
    
    def _analizar(self):
        """Analiza el texto de entrada y genera la salida."""
        contenido = self.texto_entrada.get(1.0, tk.END).strip()
        
        if not contenido:
            messagebox.showwarning("Advertencia", "No hay texto para analizar")
            return
        
        log_salida = self._ejecutar_analisis(contenido)
        self._actualizar_salida(log_salida)
        self._guardar_archivo_salida(log_salida)
        self._actualizar_ventana_simbolos()
    
    def _ejecutar_analisis(self, contenido):
        """
        Ejecuta el análisis léxico sobre el contenido.
        
        Args:
            contenido (str): Contenido a analizar
            
        Returns:
            list: Entradas del log de salida
        """
        self.lexico.limpiar_log()
        self.lexico = Lexico()
        
        lineas = contenido.split('\n')
        for linea in lineas:
            if linea.strip():
                self.lexico.analizarLinea(linea)
        
        return self.lexico.obtener_log_salida()
    
    def _actualizar_salida(self, log_salida):
        """
        Actualiza el área de texto de salida con los resultados del análisis.
        
        Args:
            log_salida (list): Lista de entradas del log
        """
        self.texto_salida.config(state=tk.NORMAL)
        self.texto_salida.delete(1.0, tk.END)
        
        if log_salida:
            self.texto_salida.insert(1.0, '\n'.join(log_salida))
        else:
            self.texto_salida.insert(1.0, "No se encontraron tokens")
        
        self.texto_salida.config(state=tk.DISABLED)
    
    def _guardar_archivo_salida(self, log_salida):
        """
        Guarda el log de salida en un archivo.
        
        Args:
            log_salida (list): Lista de entradas del log
        """
        if not self.archivo_entrada_path:
            messagebox.showinfo("Éxito", "Análisis completado")
            return
        
        directorio = os.path.dirname(self.archivo_entrada_path)
        archivo_salida = os.path.join(directorio, 'salida.txt')
        
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                f.write('\n'.join(log_salida))
            messagebox.showinfo("Éxito", f"Análisis completado. Archivo de salida guardado en:\n{archivo_salida}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar archivo de salida: {str(e)}")
    
    def _actualizar_ventana_simbolos(self):
        """Actualiza la ventana de la tabla de símbolos si está abierta."""
        if self.ventana_simbolos and self.ventana_simbolos.ventana.winfo_exists():
            self.ventana_simbolos.actualizar_tabla(self.lexico.obtener_tabla_simbolos())
    
    def ejecutar(self):
        """Inicia el bucle principal de la aplicación."""
        self.root.mainloop()

