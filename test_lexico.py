#!/usr/bin/env python3
"""
Script rápido para verificar que el analizador léxico funciona correctamente.
"""

from analizador.lexico import Lexico


def test_lexico():
    """Prueba del analizador léxico con código de ejemplo."""
    lexico = Lexico()
    
    # Test code
    codigo_prueba = """programa sumar() {
    int a, b, c;
    leer a;
    leer b;
    c = a + b;
    imprimir("la suma de ", a, " + ", b, " = ", c);
    terminar;
}"""
    
    print("=" * 60)
    print("PRUEBA DEL ANALIZADOR LÉXICO")
    print("=" * 60)
    print("\nCódigo de prueba:")
    print(codigo_prueba)
    print("\n" + "=" * 60)
    print("RESULTADOS DEL ANÁLISIS:")
    print("=" * 60)
    
    # Analyze line by line
    lineas = codigo_prueba.split('\n')
    for i, linea in enumerate(lineas, 1):
        if linea.strip():
            print(f"\n--- Línea {i}: {linea.strip()} ---")
            lexico.analizarLinea(linea)
    
    # Show results
    log_salida = lexico.obtener_log_salida()
    print("\n" + "=" * 60)
    print("TOKENS RECONOCIDOS:")
    print("=" * 60)
    for entrada in log_salida:
        print(entrada)
    
    # Show symbol table
    print("\n" + "=" * 60)
    print("TABLA DE SÍMBOLOS:")
    print("=" * 60)
    tabla = lexico.obtener_tabla_simbolos()
    print(f"{'Token':<15} {'Lexema':<20} {'Palabra Reservada':<20}")
    print("-" * 60)
    for simbolo in tabla:
        palabra_reservada = "Yes" if simbolo.palabraReservada else "No"
        print(f"{simbolo.token:<15} {simbolo.lexema:<20} {palabra_reservada:<20}")
    
    print("\n" + "=" * 60)
    print(f"Total de tokens reconocidos: {len(log_salida)}")
    print(f"Total de símbolos en tabla: {len(tabla)}")
    print("=" * 60)


if __name__ == "__main__":
    test_lexico()

