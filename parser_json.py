import sys
from lexer_json import obtener_tokens, leer_archivo

tokens = []
posicion = 0


def token_actual():
    """
    Devuelve el token actual que se está analizando.

    Si ya no hay más tokens disponibles, devuelve None.

    Returns:
        tuple | None: Token actual en la forma (tipo, valor), o None si no hay más.
    """
    global tokens, posicion

    if posicion < len(tokens):
        return tokens[posicion]
    else:
        return None


def avanzar():
    """
    Avanza a la siguiente posición de la lista de tokens.

    Esta función se utiliza cuando un token fue reconocido correctamente.
    """
    global posicion
    posicion = posicion + 1


def consumir(tipo_esperado):
    """
    Verifica que el token actual sea del tipo esperado y lo consume.

    Si el token actual no coincide con el tipo esperado, se genera un error.

    Args:
        tipo_esperado (str): Tipo de token que se espera encontrar.

    Raises:
        Exception: Si se alcanza el fin de archivo o si el token no coincide.
    """
    actual = token_actual()

    if actual is None:
        raise Exception(
            "Se esperaba " + tipo_esperado + " y se encontro fin de archivo"
        )

    tipo, valor = actual

    if tipo == tipo_esperado:
        avanzar()
    else:
        raise Exception(
            "Se esperaba " + tipo_esperado +
            " pero se encontro " + tipo +
            " con valor " + valor
        )


def analizar_objeto():
    """
    Analiza un objeto JSON.

    Gramática implementada:
        OBJETO -> { PARES }

    Raises:
        Exception: Si la estructura del objeto no es válida.
    """
    consumir("LLAVE_IZQ")
    analizar_pares ()
    consumir("LLAVE_DER")
def analizar_pares ():
    """
    PARES -> PAR | PAR, PARES
    Raises:
       Exception: Si la estructura a los pares no es válida.
    """
    # Primero debe existir al mernos un par 
    analizar_par()
    # Mientras haya comas, entonces seguimos consumiendo pares 
    while token_actual() is not None:
        tipo, valor= token_actual()
        
        if tipo == "COMA":
            consumir("COMA")
            analizar_par()
        else:
            #Si no hay coma, nos salimos del break

            
def analizar_par():
    """
    Analiza un par clave-valor.

    Gramática implementada:
        PAR -> CADENA : VALOR

    Raises:
        Exception: Si la estructura del par no es válida.
    """
    consumir("CADENA")
    consumir("DOS_PUNTOS")
    analizar_valor()


def analizar_valor():
    """
    Analiza un valor simple.

    Gramática implementada:
        VALOR -> CADENA | NUMERO

    Raises:
        Exception: Si el valor no es una cadena ni un número.
    """
    actual = token_actual()

    if actual is None:
        raise Exception("Se esperaba un valor y se encontro fin de archivo")

    tipo, valor = actual

    if tipo == "CADENA":
        consumir("CADENA")
    elif tipo == "NUMERO":
        consumir("NUMERO")

    elif tipo=="LLAVE_IZQ":
        #Significa que si encontramos una llave izquierda, es un objeto anidado
        analizar_objeto()
    else:
        raise Exception("Valor no valido: " + valor)


def analizar_json(lista_tokens):
    """
    Analiza una lista completa de tokens para verificar si forman un JSON válido
    según la gramática base.

    La gramática base es:
        OBJETO -> { PAR }
        PAR -> CADENA : VALOR
        VALOR -> CADENA | NUMERO

    Args:
        lista_tokens (list): Lista de tokens producidos por el lexer.

    Returns:
        bool: True si el JSON es válido.

    Raises:
        Exception: Si la estructura sintáctica no es válida o sobran tokens.
    """
    global tokens, posicion

    tokens = lista_tokens
    posicion = 0

    analizar_objeto()

    if token_actual() is not None:
        tipo, valor = token_actual()
        raise Exception("Hay tokens extra al final: " + tipo + " " + valor)

    return True


def main():
    """
    Función principal del programa.

    Lee la ruta de un archivo JSON desde los argumentos de la línea de comandos,
    ejecuta el lexer y luego el parser.

    Uso:
        python parser_json.py archivo.json
    """
    if len(sys.argv) != 2:
        print("Uso: python parser_json.py archivo.json")
        return

    ruta = sys.argv[1]

    try:
        texto = leer_archivo(ruta)
        lista_tokens = obtener_tokens(texto)

        print("Tokens encontrados:")
        for token in lista_tokens:
            print(token)

        analizar_json(lista_tokens)
        print("\nEl JSON es valido para la gramatica base.")

    except Exception as error:
        print("\nError:", error)


if __name__ == "__main__":
    main()

