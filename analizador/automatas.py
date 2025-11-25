class Automatas:
    """
    Implementa autómatas finitos (AFN/AFD) para reconocer
    identificadores, números enteros y números reales.
    """
    
    def isIdentificador(self, cadena):
        """
        Determina si una cadena es un identificador válido.
        Reglas de identificador: comienza con letra o guion bajo,
        seguido de letras, dígitos o guiones bajos.
        
        Args:
            cadena (str): Cadena a analizar
            
        Returns:
            bool: True si es un identificador válido, False en caso contrario
        """
        if not cadena or len(cadena) == 0:
            return False
        
        estado = 'q0'
        estados_aceptacion = {'q1'}
        
        for char in cadena:
            # Estado q0: el primer carácter debe ser letra o guion bajo
            if estado == 'q0':
                if char.isalpha() or char == '_':
                    estado = 'q1'
                    continue
                return False
            
            # Estado q1: los caracteres siguientes pueden ser letra, dígito o guion bajo
            if estado == 'q1':
                if not (char.isalnum() or char == '_'):
                    return False
        
        return estado in estados_aceptacion
    
    def isNumero(self, cadena):
        """
        Determina si una cadena es un número entero válido.
        Entero: secuencia de uno o más dígitos.
        
        Args:
            cadena (str): Cadena a analizar
            
        Returns:
            bool: True si es un número entero válido, False en caso contrario
        """
        if not cadena or len(cadena) == 0:
            return False
        
        estado = 'q0'
        estados_aceptacion = {'q1'}
        
        for char in cadena:
            # Estado q0: el primer carácter debe ser un dígito
            if estado == 'q0':
                if char.isdigit():
                    estado = 'q1'
                    continue
                return False
            
            # Estado q1: los caracteres siguientes deben ser dígitos
            if estado == 'q1':
                if not char.isdigit():
                    return False
        
        return estado in estados_aceptacion
    
    def isReal(self, cadena):
        """
        Determina si una cadena es un número real válido.
        Real: dígitos, punto decimal opcional, más dígitos.
        Formato: [dígitos].[dígitos] o .[dígitos] o [dígitos].
        
        Args:
            cadena (str): Cadena a analizar
            
        Returns:
            bool: True si es un número real válido, False en caso contrario
        """
        if not cadena or len(cadena) == 0:
            return False
        
        estado = 'q0'
        estados_aceptacion = {'q2', 'q3'}
        tiene_punto = False
        
        for char in cadena:
            # Estado q0: estado inicial
            if estado == 'q0':
                if char.isdigit():
                    estado = 'q1'
                    continue
                if char == '.':
                    estado = 'q2'
                    tiene_punto = True
                    continue
                return False
            
            # Estado q1: dígitos antes del punto decimal
            if estado == 'q1':
                if char.isdigit():
                    continue
                if char == '.' and not tiene_punto:
                    estado = 'q3'
                    tiene_punto = True
                    continue
                return False
            
            # Estado q2: punto decimal sin dígitos iniciales
            if estado == 'q2':
                if char.isdigit():
                    estado = 'q3'
                    continue
                return False
            
            # Estado q3: dígitos después del punto decimal
            if estado == 'q3':
                if not char.isdigit():
                    return False
        
        return estado in estados_aceptacion

