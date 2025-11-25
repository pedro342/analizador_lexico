# Explicación Detallada del Analizador Léxico

## 📋 Tabla de Contenidos
1. [Arquitectura General](#arquitectura-general)
2. [Componentes del Sistema](#componentes-del-sistema)
   - [Archivos Principales](#archivos-principales)
   - [Archivos de Soporte](#archivos-de-soporte)
3. [Flujo de Ejecución](#flujo-de-ejecución)
4. [Análisis Detallado por Clase](#análisis-detallado-por-clase)
5. [Interacciones entre Componentes](#interacciones-entre-componentes)
6. [Efectos de Cambios en el Código](#efectos-de-cambios-en-el-código)

---

## 🏗️ Arquitectura General

El proyecto sigue el patrón **Modelo-Vista-Controlador (MVC)**:

```
┌─────────────────────────────────────────────────┐
│              CAPA DE PRESENTACIÓN (Vista)       │
│  ┌──────────────────┐  ┌──────────────────┐   │
│  │ IndexCompilador  │  │ VentanaSimbolos  │   │
│  │   (GUI Principal)│  │ (Ventana Popup)  │   │
│  └──────────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│          CAPA DE LÓGICA (Controlador)           │
│  ┌──────────────────────────────────────────┐  │
│  │           Lexico (Analizador)            │  │
│  │  - Procesa líneas de código              │  │
│  │  - Identifica tokens y lexemas           │  │
│  │  - Gestiona tabla de símbolos            │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌──────────────────┐  ┌──────────────────┐
│    Automatas     │  │     Simbolo      │
│  (Reconocedores) │  │  (Estructura)    │
└──────────────────┘  └──────────────────┘
```

---

## 🧩 Componentes del Sistema

### Archivos Principales

#### 1. **compilador/simbolos.py** - Clase `Simbolo`
**Propósito**: Representa un elemento de la tabla de símbolos.

**Atributos**:
- `token`: Identificador interno del token (ej: 'pro', 'id_1')
- `lexema`: Cadena literal encontrada en el código (ej: 'programa', 'a')
- `palabraReservada`: Booleano que indica si es palabra reservada

**Métodos importantes**:
- `__init__()`: Constructor que inicializa los tres atributos
- `__repr__()`: Representación en string para debugging
- `__eq__()`: Comparación de igualdad (por token y lexema)

**Ejemplo de uso**:
```python
simbolo = Simbolo('pro', 'programa', True)
# token='pro', lexema='programa', palabraReservada=True
```

---

#### 2. **analizador/automatas.py** - Clase `Automatas`
**Propósito**: Implementa autómatas finitos deterministas (AFD) para reconocer patrones.

#### 2.1 `isIdentificador(cadena)`
**Autómata para identificadores**:
- **Estado q0**: Estado inicial
- **Estado q1**: Estado de aceptación (identificador válido)
- **Transiciones**:
  - q0 → q1: Si el carácter es letra o guion bajo
  - q1 → q1: Si el carácter es letra, dígito o guion bajo
  - Cualquier otra transición → Rechazo

**Ejemplo**:
- `"variable"` → ✅ Válido (q0→q1→q1→q1...)
- `"123abc"` → ❌ Inválido (empieza con dígito)
- `"_temp"` → ✅ Válido

#### 2.2 `isNumero(cadena)`
**Autómata para números enteros**:
- **Estado q0**: Estado inicial
- **Estado q1**: Estado de aceptación
- **Transiciones**:
  - q0 → q1: Si el carácter es dígito
  - q1 → q1: Si el carácter es dígito
  - Cualquier otra → Rechazo

**Ejemplo**:
- `"123"` → ✅ Válido
- `"12.5"` → ❌ Inválido (contiene punto)
- `"abc"` → ❌ Inválido

#### 2.3 `isReal(cadena)`
**Autómata para números reales** (más complejo):
- **Estados**: q0 (inicial), q1 (dígitos antes del punto), q2 (punto sin dígitos), q3 (aceptación)
- **Estados de aceptación**: q2, q3
- **Transiciones**:
  - q0 → q1: Si es dígito
  - q0 → q2: Si es punto
  - q1 → q1: Si es dígito
  - q1 → q3: Si es punto (y no hay punto previo)
  - q2 → q3: Si es dígito
  - q3 → q3: Si es dígito

**Ejemplo**:
- `"123.45"` → ✅ Válido (q0→q1→q1→q1→q3→q3→q3)
- `".5"` → ✅ Válido (q0→q2→q3)
- `"123"` → ❌ Inválido (no tiene punto decimal)

---

#### 3. **analizador/lexico.py** - Clase `Lexico`
**Propósito**: Coordina el análisis léxico completo.

#### 3.1 Inicialización
```python
def __init__(self):
    self.tabla_simbolos = self._inicializar_tabla_simbolos()  # 28 símbolos iniciales
    self.automatas = Automatas()  # Instancia de reconocedores
    self.log_salida = []  # Lista para almacenar resultados
```

#### 3.2 Procesamiento de Líneas: `analizarLinea(linea)`
**Flujo**:
1. Valida que la línea no esté vacía
2. Llama a `_procesar_caracteres()` que itera carácter por carácter
3. Para cada carácter no-espacio:
   - Obtiene el siguiente lexema
   - Analiza el lexema

#### 3.3 Extracción de Lexemas: `_obtener_siguiente_lexema()`
**Estrategia de extracción**:
1. **Primero**: Verifica operadores de 2 caracteres (`&&`, `||`)
2. **Luego**: Extrae según el tipo:
   - Operador de 1 carácter (`+`, `-`, `*`, etc.)
   - Cadena entre comillas (`"texto"`)
   - Identificador/número/palabra reservada

**Ejemplo con `"c = a + b;"`**:
- Posición 0: `'c'` → Identificador → `"c"`
- Posición 2: `'='` → Operador → `"="`
- Posición 4: `'a'` → Identificador → `"a"`
- Posición 6: `'+'` → Operador → `"+"`
- Posición 8: `'b'` → Identificador → `"b"`
- Posición 10: `';'` → Operador → `";"`

#### 3.4 Análisis de Lexemas: `analizarLexema(lexema)`
**Árbol de decisión**:
```
¿Está en tabla de símbolos?
├─ SÍ → ¿Es palabra reservada?
│        ├─ SÍ → Procesa como palabra reservada
│        └─ NO → Procesa como identificador existente
│
└─ NO → ¿Qué tipo es?
         ├─ Identificador → Agrega a tabla si es nuevo
         ├─ Número entero → Procesa como número
         ├─ Número real → Procesa como real
         ├─ Cadena → Procesa como cadena
         └─ Otro → Marca como ERROR
```

#### 3.5 Gestión de Identificadores
Cuando encuentra un identificador nuevo:
1. Busca si ya existe en la tabla
2. Si no existe:
   - Cuenta identificadores existentes
   - Crea token `id_N` (donde N es el número)
   - Agrega a `tabla_simbolos`
   - Registra en log

**Ejemplo**:
```python
# Primera vez que encuentra "variable1"
# → Crea: Simbolo('id_1', 'variable1', False)
# → Log: "Token: id_1, Lexema: variable1, Tipo: Identificador"

# Segunda vez que encuentra "variable1"
# → Busca y encuentra el existente
# → Log: "Token: id_1, Lexema: variable1, Tipo: Identificador"
```

---

#### 4. **gui/index_compilador.py** - Clase `IndexCompilador`
**Propósito**: Interfaz gráfica principal (Vista + Controlador).

#### 4.1 Estructura de la Interfaz
```
┌─────────────────────────────────────────┐
│      Analizador Léxico (Ventana)        │
├─────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐    │
│  │Texto Entrada │  │Texto Salida  │    │
│  │              │  │              │    │
│  │  [área]      │  │  [área]      │    │
│  │              │  │              │    │
│  └──────────────┘  └──────────────┘    │
│  [Cargar] [Tabla] [Analizar]            │
└─────────────────────────────────────────┘
```

#### 4.2 Flujo de Análisis: `_analizar()`
1. Obtiene contenido del área de texto
2. Valida que haya contenido
3. Ejecuta análisis (`_ejecutar_analisis()`)
4. Actualiza área de salida
5. Guarda archivo `salida.txt`
6. Actualiza ventana de símbolos (si está abierta)

#### 4.3 Gestión de Archivos
- **Cargar**: Abre diálogo, lee archivo, muestra en área de entrada
- **Guardar**: Escribe `salida.txt` en el mismo directorio del archivo de entrada

---

#### 5. **gui/ventana_simbolos.py** - Clase `VentanaSimbolos`
**Propósito**: Muestra la tabla de símbolos en una ventana emergente.

**Componentes**:
- `Treeview`: Tabla con 3 columnas (Token, Lexema, Palabra Reservada)
- `Scrollbar`: Para navegar si hay muchos símbolos
- Se actualiza automáticamente cuando se analiza código nuevo

**Métodos principales**:
- `__init__()`: Crea la ventana emergente y configura la interfaz
- `_crear_interfaz()`: Construye el Treeview y scrollbar
- `_cargar_tabla()`: Pobla el Treeview con los símbolos actuales
- `actualizar_tabla()`: Actualiza la tabla cuando hay nuevos símbolos

---

### Archivos de Soporte

#### 6. **main.py** - Punto de Entrada
**Propósito**: Archivo principal que inicia la aplicación.

**Código**:
```python
def main():
    """Punto de entrada principal de la aplicación."""
    app = IndexCompilador()
    app.ejecutar()

if __name__ == "__main__":
    main()
```

**Funcionamiento**:
1. Crea una instancia de `IndexCompilador` (interfaz principal)
2. Llama a `ejecutar()` que inicia el bucle principal de Tkinter
3. El `if __name__ == "__main__"` asegura que solo se ejecute cuando se llama directamente (no al importar)

**Importancia**: 
- Es el punto de entrada estándar en Python
- Permite ejecutar la aplicación con `python3 main.py`
- Facilita la importación del módulo sin ejecutar código

---

#### 7. **Archivos `__init__.py`**
**Ubicaciones**: 
- `compilador/__init__.py`
- `analizador/__init__.py`
- `gui/__init__.py`

**Propósito**: Convierten los directorios en paquetes de Python.

**Contenido**: Solo comentarios simples que identifican el paquete.

**Función**:
- Permiten importar módulos usando `from compilador.simbolos import Simbolo`
- Sin estos archivos, Python no reconocería los directorios como paquetes
- Están vacíos porque no necesitan inicialización especial

**Ejemplo de uso**:
```python
# Con __init__.py, esto funciona:
from analizador.lexico import Lexico

# Sin __init__.py, Python no encontraría el módulo
```

---

#### 8. **run.sh** - Script Helper
**Propósito**: Script de shell para facilitar la ejecución de la aplicación.

**Código**:
```bash
#!/bin/bash
# Script helper para ejecutar el analizador léxico

if [ -f "/opt/homebrew/bin/python3.12" ]; then
    /opt/homebrew/bin/python3.12 main.py
elif [ -f "/usr/local/bin/python3.12" ]; then
    /usr/local/bin/python3.12 main.py
else
    python3 main.py
fi
```

**Funcionamiento**:
1. Verifica si existe Python 3.12 de Homebrew en `/opt/homebrew/bin/`
2. Si no, verifica en `/usr/local/bin/` (Homebrew en Intel Mac)
3. Si no encuentra ninguna, usa el Python del sistema

**Razón de existencia**:
- Soluciona problemas de compatibilidad con Tkinter
- El Python del sistema en macOS puede tener problemas con Tkinter
- Python 3.12 de Homebrew tiene mejor soporte

**Uso**: `./run.sh` desde la terminal

---

#### 9. **test_lexico.py** - Script de Pruebas
**Propósito**: Script de prueba para verificar el funcionamiento del analizador sin la GUI.

**Funcionalidad**:
1. Crea una instancia de `Lexico`
2. Define código de prueba predefinido
3. Analiza línea por línea
4. Muestra resultados en consola:
   - Código de prueba
   - Tokens reconocidos
   - Tabla de símbolos completa
   - Estadísticas (total de tokens y símbolos)

**Ventajas**:
- Permite probar el analizador sin interfaz gráfica
- Útil para debugging
- Muestra información detallada del proceso

**Uso**: `python3 test_lexico.py`

**Ejemplo de salida**:
```
============================================================
PRUEBA DEL ANALIZADOR LÉXICO
============================================================
Código de prueba:
programa sumar() {
    int a, b, c;
    ...
}
============================================================
TOKENS RECONOCIDOS:
============================================================
Token: pro, Lexema: programa, Tipo: Palabra Reservada
Token: id_1, Lexema: sumar, Tipo: Identificador
...
============================================================
TABLA DE SÍMBOLOS:
============================================================
Token           Lexema               Palabra Reservada   
------------------------------------------------------------
pro             programa             Yes
...
```

---

## 🔄 Flujo de Ejecución Completo

### Escenario: Usuario analiza `"int a, b;"`

```
1. Usuario escribe "int a, b;" en área de entrada
   └─> IndexCompilador.texto_entrada contiene el texto

2. Usuario hace clic en "Analizar"
   └─> IndexCompilador._analizar() se ejecuta

3. _analizar() llama a _ejecutar_analisis()
   └─> Crea nueva instancia de Lexico()
   └─> Divide texto en líneas: ["int a, b;"]

4. Para cada línea, llama a lexico.analizarLinea()
   └─> _procesar_caracteres() itera carácter por carácter

5. Extracción de lexemas:
   - Posición 0: "int" → Lexema extraído
   - Posición 4: "a" → Lexema extraído
   - Posición 6: "," → Lexema extraído
   - Posición 8: "b" → Lexema extraído
   - Posición 10: ";" → Lexema extraído

6. Para cada lexema, analizarLexema():
   a) "int":
      - Busca en tabla → ENCONTRADO
      - Es palabra reservada → Log: "Token: int, Lexema: int, Tipo: Palabra Reservada"
   
   b) "a":
      - Busca en tabla → NO ENCONTRADO
      - isIdentificador("a") → True
      - Es nuevo → Crea Simbolo('id_1', 'a', False)
      - Log: "Token: id_1, Lexema: a, Tipo: Identificador"
   
   c) ",":
      - Busca en tabla → ENCONTRADO
      - Es palabra reservada → Log: "Token: ,, Lexema: ,, Tipo: Palabra Reservada"
   
   d) "b":
      - Busca en tabla → NO ENCONTRADO
      - isIdentificador("b") → True
      - Es nuevo → Crea Simbolo('id_2', 'b', False)
      - Log: "Token: id_2, Lexema: b, Tipo: Identificador"
   
   e) ";":
      - Busca en tabla → ENCONTRADO
      - Es palabra reservada → Log: "Token: ;, Lexema: ;, Tipo: Palabra Reservada"

7. _actualizar_salida() muestra todos los logs en área de salida

8. _guardar_archivo_salida() escribe salida.txt

9. _actualizar_ventana_simbolos() actualiza la tabla si está abierta
```

---

## 🔗 Interacciones entre Componentes

### Diagrama de Dependencias
```
main.py
  └─> IndexCompilador
        ├─> Lexico
        │     ├─> Simbolo (crea instancias)
        │     └─> Automatas (usa métodos)
        │
        └─> VentanaSimbolos
              └─> Simbolo (lee atributos)
```

### Flujo de Datos
```
Archivo de Entrada
    ↓
IndexCompilador (lee archivo)
    ↓
Lexico.analizarLinea() (procesa)
    ↓
Automatas (reconoce patrones)
    ↓
Lexico (crea/actualiza Simbolo)
    ↓
Tabla de Símbolos (se actualiza)
    ↓
Log de Salida (se genera)
    ↓
IndexCompilador (muestra en GUI)
    ↓
Archivo salida.txt (se guarda)
```

---

## ⚠️ Efectos de Cambios en el Código

### 1. Cambios en `Simbolo`
**Si agregas un nuevo atributo** (ej: `tipo_dato`):
- ✅ **Impacto**: Bajo
- **Afecta**: Inicialización en `_inicializar_tabla_simbolos()`
- **Debes actualizar**: Todos los lugares donde se crea `Simbolo()`

**Si cambias `__eq__()`**:
- ⚠️ **Impacto**: Medio
- **Afecta**: Búsquedas en tabla de símbolos
- **Riesgo**: Identificadores duplicados podrían no detectarse

### 2. Cambios en `Automatas`
**Si modificas `isIdentificador()`**:
- ⚠️ **Impacto**: Alto
- **Afecta**: Reconocimiento de variables, funciones, etc.
- **Ejemplo**: Si cambias para aceptar números al inicio:
  - `"123abc"` pasaría a ser válido
  - Podría causar conflictos con números

**Si modificas `isReal()`**:
- ⚠️ **Impacto**: Medio
- **Afecta**: Reconocimiento de números decimales
- **Ejemplo**: Si cambias para aceptar solo un formato:
  - `".5"` podría dejar de ser válido
  - `"123."` podría empezar a ser válido

**Si agregas un nuevo autómata** (ej: `isHexadecimal()`):
- ✅ **Impacto**: Bajo (si se integra bien)
- **Debes**: Agregar lógica en `_procesar_lexema_no_reservado()`

### 3. Cambios en `Lexico`
**Si modificas `_inicializar_tabla_simbolos()`**:
- ⚠️ **Impacto**: Alto
- **Afecta**: Todas las palabras reservadas y operadores
- **Ejemplo**: Si eliminas `Simbolo(';', ';', True)`:
  - Los punto y coma se marcarían como ERROR
  - El análisis fallaría para código válido

**Si cambias el orden en `_obtener_siguiente_lexema()`**:
- ⚠️ **Impacto**: Alto
- **Afecta**: Extracción de lexemas
- **Ejemplo**: Si verificas operadores de 1 carácter antes de 2:
  - `"&&"` se reconocería como dos `"&"` separados
  - El análisis sería incorrecto

**Si modificas `_extraer_identificador()`**:
- ⚠️ **Impacto**: Medio
- **Afecta**: Separación de lexemas
- **Ejemplo**: Si no incluyes `';'` en delimitadores:
  - `"variable;"` se extraería como un solo lexema
  - Causaría errores de reconocimiento

**Si cambias la lógica de `_agregar_identificador()`**:
- ⚠️ **Impacto**: Medio
- **Afecta**: Numeración de identificadores
- **Ejemplo**: Si cambias `id_{len(identificadores) + 1}`:
  - Los tokens de identificadores cambiarían
  - Podría afectar análisis sintáctico posterior

### 4. Cambios en `IndexCompilador`
**Si modificas `_ejecutar_analisis()`**:
- ⚠️ **Impacto**: Medio
- **Afecta**: Proceso de análisis
- **Ejemplo**: Si no reseteas `Lexico()`:
  - Los identificadores se acumularían entre análisis
  - La tabla de símbolos crecería indefinidamente

**Si cambias la ruta de guardado en `_guardar_archivo_salida()`**:
- ✅ **Impacto**: Bajo
- **Afecta**: Ubicación del archivo de salida
- **Ejemplo**: Si cambias a ruta fija:
  - Siempre se guardaría en el mismo lugar
  - Podría sobrescribir archivos anteriores

### 5. Cambios en `VentanaSimbolos`
**Si modificas `_cargar_tabla()`**:
- ✅ **Impacto**: Bajo (solo visual)
- **Afecta**: Presentación de datos
- **Ejemplo**: Si cambias "Sí"/"No" por True/False:
  - La interfaz mostraría valores booleanos
  - Menos legible para usuarios

---

## 🎯 Puntos Clave para la Exposición

### 1. **Arquitectura MVC**
- **Modelo**: `Simbolo`, `Automatas`
- **Vista**: `IndexCompilador`, `VentanaSimbolos`
- **Controlador**: `Lexico` (coordina modelo y vista)

### 2. **Autómatas Finitos**
- Implementación explícita de AFD
- Estados y transiciones claramente definidos
- Reconocimiento de patrones sin regex

### 3. **Tabla de Símbolos**
- Estructura dinámica (se agregan identificadores)
- Separación entre palabras reservadas e identificadores
- Persistencia durante el análisis

### 4. **Procesamiento Léxico**
- Análisis carácter por carácter
- Prioridad en operadores multi-carácter
- Manejo de diferentes tipos de lexemas

### 5. **Interfaz Gráfica**
- Separación de responsabilidades
- Actualización en tiempo real
- Persistencia de resultados

---

## 📝 Ejemplo de Análisis Completo

**Código de entrada**:
```
programa ejemplo() {
    int x = 5;
    imprimir(x);
}
```

**Procesamiento**:
1. `"programa"` → Palabra reservada (token: `pro`)
2. `"ejemplo"` → Identificador nuevo (token: `id_1`)
3. `"("` → Palabra reservada
4. `")"` → Palabra reservada
5. `"{"` → Palabra reservada
6. `"int"` → Palabra reservada
7. `"x"` → Identificador nuevo (token: `id_2`)
8. `"="` → Palabra reservada
9. `"5"` → Número entero (token: `numero`)
10. `";"` → Palabra reservada
11. `"imprimir"` → Palabra reservada (token: `imp`)
12. `"("` → Palabra reservada
13. `"x"` → Identificador existente (token: `id_2`)
14. `")"` → Palabra reservada
15. `";"` → Palabra reservada
16. `"}"` → Palabra reservada

**Tabla de símbolos final**:
- 28 símbolos iniciales (palabras reservadas)
- 2 identificadores agregados: `id_1` (ejemplo), `id_2` (x)
- **Total**: 30 símbolos

---

## 🔍 Casos Especiales y Edge Cases

### 1. **Operadores Multi-carácter**
- `"&&"` se verifica antes que `"&"`
- Si no, se reconocerían como dos `"&"` separados

### 2. **Cadenas de Texto**
- Se extraen completas (incluyendo comillas)
- Si falta comilla de cierre, se toma hasta el final de línea

### 3. **Identificadores Duplicados**
- Se busca primero si existe
- Si existe, se reutiliza el token
- Evita duplicación en tabla

### 4. **Espacios en Blanco**
- Se ignoran completamente
- No generan tokens

### 5. **Tokens No Reconocidos**
- Se marcan como ERROR
- Se registran en log para debugging

---

## 💡 Mejoras Potenciales

1. **Manejo de Errores**: Agregar línea y columna a errores
2. **Comentarios**: Reconocer `//` y `/* */`
3. **Números Negativos**: Manejar `-123` como número
4. **Optimización**: Cachear resultados de autómatas
5. **Validación**: Verificar que identificadores no sean palabras reservadas

---
