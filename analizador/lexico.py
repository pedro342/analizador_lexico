from compilador.simbolos import Simbolo
from analizador.automatas import Automatas


class Lexico:
    """
    Analizador léxico que procesa código fuente línea por línea,
    reconoce tokens usando la tabla de símbolos y autómatas.
    """
    
    def __init__(self):
        """Inicializa el analizador léxico con la tabla de símbolos inicial."""
        self.tabla_simbolos = self._inicializar_tabla_simbolos()
        self.automatas = Automatas()
        self.log_salida = []
    
    def _inicializar_tabla_simbolos(self):
        """
        Inicializa la tabla de símbolos con palabras reservadas y operadores.
        
        Returns:
            list: Lista de objetos Simbolo
        """
        simbolos = [
            Simbolo('pro', 'programa', True),
            Simbolo('int', 'int', True),
            Simbolo('char', 'char', True),
            Simbolo('float', 'float', True),
            Simbolo('leer', 'leer', True),
            Simbolo('imp', 'imprimir', True),
            Simbolo('+', '+', True),
            Simbolo('-', '-', True),
            Simbolo('*', '*', True),
            Simbolo('/', '/', True),
            Simbolo('=', '=', True),
            Simbolo('ter', 'terminar', True),
            Simbolo('min', 'mientras', True),
            Simbolo('si', 'si', True),
            Simbolo('sino', 'sino', True),
            Simbolo('.', '.', True),
            Simbolo(',', ',', True),
            Simbolo(':', ':', True),
            Simbolo('(', '(', True),
            Simbolo(')', ')', True),
            Simbolo('{', '{', True),
            Simbolo('}', '}', True),
            Simbolo('&', '&', True),
            Simbolo('&&', '&&', True),
            Simbolo('|', '|', True),
            Simbolo('||', '||', True),
            Simbolo('<', '<', True),
            Simbolo('>', '>', True),
            Simbolo(';', ';', True),
        ]
        return simbolos
    
    def obtener_tabla_simbolos(self):
        """
        Obtiene la tabla de símbolos actual.
        
        Returns:
            list: Tabla de símbolos actual
        """
        return self.tabla_simbolos
    
    def analizarLinea(self, linea):
        """
        Analiza una línea de código carácter por carácter,
        identificando lexemas y tokens.
        
        Args:
            linea (str): Línea de código a analizar
        """
        if not linea or len(linea.strip()) == 0:
            return
        
        self._procesar_caracteres(linea)
    
    def _procesar_caracteres(self, linea):
        """
        Procesa los caracteres de una línea, extrayendo lexemas.
        
        Args:
            linea (str): Línea de código a procesar
        """
        i = 0
        while i < len(linea):
            if linea[i].isspace():
                i += 1
                continue
            
            lexema, avance = self._obtener_siguiente_lexema(linea, i)
            if lexema:
                self.analizarLexema(lexema)
            i += avance
    
    def _obtener_siguiente_lexema(self, linea, inicio):
        """
        Obtiene el siguiente lexema de la línea a partir de la posición dada.
        
        Args:
            linea (str): Línea de código
            inicio (int): Posición inicial
            
        Returns:
            tuple: (lexema, cantidad_avance)
        """
        if inicio >= len(linea):
            return "", 0
        
        # Verificar primero operadores de múltiples caracteres
        if inicio < len(linea) - 1:
            dos_chars = linea[inicio:inicio+2]
            if self._buscar_en_tabla(dos_chars):
                return dos_chars, 2
        
        lexema = self._extraer_lexema(linea, inicio)
        return lexema, len(lexema)
    
    def _extraer_lexema(self, linea, inicio):
        """
        Extrae un lexema de la línea a partir de la posición dada.
        
        Args:
            linea (str): Línea de código
            inicio (int): Posición inicial
            
        Returns:
            str: Lexema extraído
        """
        if inicio >= len(linea):
            return ""
        
        char = linea[inicio]
        
        operador = self._extraer_operador(char)
        if operador:
            return operador
        
        cadena = self._extraer_cadena(linea, inicio)
        if cadena:
            return cadena
        
        return self._extraer_identificador(linea, inicio)
    
    def _extraer_operador(self, char):
        """
        Extrae un operador o delimitador de un solo carácter.
        
        Args:
            char (str): Carácter a verificar
            
        Returns:
            str or None: Operador si se encuentra, None en caso contrario
        """
        operadores = ['+', '-', '*', '/', '=', '.', ',', ':', '(', ')', '{', '}', '&', '|', '<', '>', ';']
        return char if char in operadores else None
    
    def _extraer_cadena(self, linea, inicio):
        """
        Extrae una cadena de texto literal (entre comillas).
        
        Args:
            linea (str): Línea de código
            inicio (int): Posición inicial
            
        Returns:
            str or None: Cadena literal si se encuentra, None en caso contrario
        """
        if inicio >= len(linea) or linea[inicio] != '"':
            return None
        
        fin = inicio + 1
        while fin < len(linea) and linea[fin] != '"':
            fin += 1
        
        if fin < len(linea):
            return linea[inicio:fin+1]
        return linea[inicio:]
    
    def _extraer_identificador(self, linea, inicio):
        """
        Extrae un identificador, número o palabra reservada.
        
        Args:
            linea (str): Línea de código
            inicio (int): Posición inicial
            
        Returns:
            str: Identificador extraído
        """
        delimitadores = ['+', '-', '*', '/', '=', '.', ',', ':', '(', ')', '{', '}', '&', '|', '<', '>', '"', ';']
        
        fin = inicio
        while fin < len(linea) and not linea[fin].isspace():
            if linea[fin] in delimitadores:
                break
            fin += 1
        
        return linea[inicio:fin]
    
    def _buscar_en_tabla(self, lexema):
        """
        Busca un lexema en la tabla de símbolos.
        
        Args:
            lexema (str): Lexema a buscar
            
        Returns:
            Simbolo or None: Símbolo encontrado o None
        """
        for simbolo in self.tabla_simbolos:
            if simbolo.lexema == lexema:
                return simbolo
        return None
    
    def analizarLexema(self, lexema):
        """
        Analiza un lexema y determina si es una palabra reservada o identificador.
        Actualiza la tabla de símbolos si es un nuevo identificador.
        
        Args:
            lexema (str): Lexema a analizar
        """
        if not lexema:
            return
        
        simbolo = self._buscar_en_tabla(lexema)
        if simbolo:
            if simbolo.palabraReservada:
                self._procesar_palabra_reservada(simbolo)
            else:
                self._procesar_identificador_existente(simbolo)
        else:
            self._procesar_lexema_no_reservado(lexema)
    
    def _procesar_palabra_reservada(self, simbolo):
        """
        Procesa una palabra reservada u operador de la tabla de símbolos.
        
        Args:
            simbolo (Simbolo): Símbolo a procesar
        """
        self.log_salida.append(f"Token: {simbolo.token}, Lexema: {simbolo.lexema}, Tipo: Palabra Reservada")
    
    def _procesar_identificador_existente(self, simbolo):
        """
        Procesa un identificador que ya existe en la tabla de símbolos.
        
        Args:
            simbolo (Simbolo): Símbolo identificador a procesar
        """
        self.log_salida.append(f"Token: {simbolo.token}, Lexema: {simbolo.lexema}, Tipo: Identificador")
    
    def _procesar_lexema_no_reservado(self, lexema):
        """
        Procesa un lexema que no está en la tabla de símbolos.
        
        Args:
            lexema (str): Lexema a procesar
        """
        if self.automatas.isIdentificador(lexema):
            self._procesar_identificador(lexema)
        elif self.automatas.isNumero(lexema):
            self._procesar_numero(lexema)
        elif self.automatas.isReal(lexema):
            self._procesar_real(lexema)
        elif lexema.startswith('"') and lexema.endswith('"'):
            self._procesar_cadena(lexema)
        else:
            self.log_salida.append(f"Token: ERROR, Lexema: {lexema}, Tipo: No reconocido")
    
    def _procesar_identificador(self, lexema):
        """
        Procesa un identificador, agregándolo a la tabla de símbolos si es nuevo.
        
        Args:
            lexema (str): Lexema del identificador
        """
        simbolo_existente = self._buscar_identificador_existente(lexema)
        if simbolo_existente:
            self.log_salida.append(f"Token: {simbolo_existente.token}, Lexema: {simbolo_existente.lexema}, Tipo: Identificador")
        else:
            self._agregar_identificador(lexema)
    
    def _buscar_identificador_existente(self, lexema):
        """
        Busca un identificador existente en la tabla de símbolos.
        
        Args:
            lexema (str): Lexema del identificador a buscar
            
        Returns:
            Simbolo or None: Símbolo identificador existente o None
        """
        for simbolo in self.tabla_simbolos:
            if simbolo.lexema == lexema and not simbolo.palabraReservada:
                return simbolo
        return None
    
    def _agregar_identificador(self, lexema):
        """
        Agrega un nuevo identificador a la tabla de símbolos.
        
        Args:
            lexema (str): Lexema del identificador a agregar
        """
        identificadores = [s for s in self.tabla_simbolos if not s.palabraReservada]
        nuevo_token = f"id_{len(identificadores) + 1}"
        nuevo_simbolo = Simbolo(nuevo_token, lexema, False)
        self.tabla_simbolos.append(nuevo_simbolo)
        self.log_salida.append(f"Token: {nuevo_token}, Lexema: {lexema}, Tipo: Identificador")
    
    def _procesar_numero(self, lexema):
        """
        Procesa un número entero.
        
        Args:
            lexema (str): Lexema del número
        """
        self.log_salida.append(f"Token: numero, Lexema: {lexema}, Tipo: Número Entero")
    
    def _procesar_real(self, lexema):
        """
        Procesa un número real.
        
        Args:
            lexema (str): Lexema del número real
        """
        self.log_salida.append(f"Token: real, Lexema: {lexema}, Tipo: Número Real")
    
    def _procesar_cadena(self, lexema):
        """
        Procesa una cadena de texto literal.
        
        Args:
            lexema (str): Lexema de la cadena
        """
        self.log_salida.append(f"Token: cadena, Lexema: {lexema}, Tipo: Cadena de Texto")
    
    def obtener_log_salida(self):
        """
        Obtiene el log de salida.
        
        Returns:
            list: Lista de entradas del log
        """
        return self.log_salida
    
    def limpiar_log(self):
        """Limpia el log de salida."""
        self.log_salida = []

