import tkinter as tk
from tkinter import ttk
from compilador.simbolos import Simbolo


class VentanaSimbolos:
    """
    Ventana emergente que muestra la tabla de símbolos.
    Muestra tokens, lexemas y estado de palabra reservada.
    """
    
    def __init__(self, parent, tabla_simbolos):
        """
        Inicializa la ventana de la tabla de símbolos.
        
        Args:
            parent: Ventana padre
            tabla_simbolos: Lista de objetos Simbolo a mostrar
        """
        self.parent = parent
        self.tabla_simbolos = tabla_simbolos
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Tabla de Símbolos")
        self.ventana.geometry("600x400")
        
        self._crear_interfaz()
        self._cargar_tabla()
    
    def _crear_interfaz(self):
        """Crea los componentes de la interfaz gráfica."""
        # Frame para el treeview
        frame = ttk.Frame(self.ventana, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview para la tabla de símbolos
        columns = ('Token', 'Lexema', 'Palabra Reservada')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        # Configurar encabezados de columnas
        self.tree.heading('Token', text='Token')
        self.tree.heading('Lexema', text='Lexema')
        self.tree.heading('Palabra Reservada', text='Palabra Reservada')
        
        # Configurar anchos de columnas
        self.tree.column('Token', width=150, anchor=tk.CENTER)
        self.tree.column('Lexema', width=200, anchor=tk.CENTER)
        self.tree.column('Palabra Reservada', width=200, anchor=tk.CENTER)
        
        # Barra de desplazamiento
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar componentes
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _cargar_tabla(self):
        """Carga los datos de la tabla de símbolos en el treeview."""
        # Limpiar elementos existentes
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Agregar símbolos al treeview
        for simbolo in self.tabla_simbolos:
            palabra_reservada = "Sí" if simbolo.palabraReservada else "No"
            self.tree.insert('', tk.END, values=(
                simbolo.token,
                simbolo.lexema,
                palabra_reservada
            ))
    
    def actualizar_tabla(self, nueva_tabla_simbolos):
        """
        Actualiza la tabla de símbolos con nuevos datos.
        
        Args:
            nueva_tabla_simbolos: Lista actualizada de objetos Simbolo
        """
        self.tabla_simbolos = nueva_tabla_simbolos
        self._cargar_tabla()

