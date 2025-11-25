class Simbolo:
    """
    Representa un símbolo en la tabla de símbolos.
    Cada símbolo tiene un token, lexema y bandera de palabra reservada.
    """
    
    def __init__(self, token, lexema, palabra_reservada):
        """
        Inicializa un símbolo.
        
        Args:
            token (str): Representación del token
            lexema (str): Lexema asociado
            palabra_reservada (bool): Si es una palabra reservada
        """
        self.token = token
        self.lexema = lexema
        self.palabraReservada = palabra_reservada
    
    def __repr__(self):
        return f"Simbolo(token='{self.token}', lexema='{self.lexema}', palabraReservada={self.palabraReservada})"
    
    def __eq__(self, other):
        if not isinstance(other, Simbolo):
            return False
        return self.token == other.token and self.lexema == other.lexema

