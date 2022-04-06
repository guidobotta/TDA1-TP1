import sys

def leer_antenas(ruta_archivo):
    """
    Recibe la ruta del archivo y devuelve una lista de antenas con el siguiente formato
    [{"nro": int, "pos": int, "radio": int}]
    """
    antenas = []

    with open(ruta_archivo) as archivo:
        for linea in archivo:
            linea = linea.strip()
            nro, pos, radio = linea.split(',')
            antenas.append({"nro": int(nro), "pos": int(pos), "radio": int(radio)})

    return antenas

def cubre_anterior(antena, solucion):
    """
    Devuelve True si la antena recibida cubre en cobertura efectiva a la ultima antena
    de la solucion o False en caso contrario.
    """
    if not solucion: return False
    
    cubrimiento_antena = antena["pos"] - antena["radio"]
    cubrimiento_anterior = solucion[-1]["pos"] - solucion[-1]["radio"]

    if len(solucion) > 1 and solucion[-2]["pos"] + solucion[-2]["radio"] > cubrimiento_anterior:
        cubrimiento_anterior = solucion[-2]["pos"] + solucion[-2]["radio"]

    if cubrimiento_anterior < 0:
        cubrimiento_anterior = 0

    return cubrimiento_antena <= cubrimiento_anterior

def buscar_solucion(antenas, kilometros):
    """
    Recibe una lista de antenas y los kilometros de longitud de la ruta.
    Devuelve la mejor solucion posible.
    La solucion devuelta puede no ser optima. Es decir, puede que no cubra
    toda la ruta.
    """
    # Ordeno por posicion, desempatando por mayor radio
    antenas_ordenadas = sorted(antenas, key=lambda antena: (antena["pos"], -antena["radio"]))
    solucion = [antenas_ordenadas[0]]
    posicion_actual = solucion[0]["pos"] + solucion[0]["radio"]
    quito_anterior = False

    for antena in antenas_ordenadas[1:]:
        while cubre_anterior(antena, solucion):
            quito_anterior = True
            solucion.pop()
        
        if quito_anterior or (posicion_actual < kilometros and antena["pos"] + antena["radio"] > posicion_actual):
            solucion.append(antena)
            posicion_actual = antena['pos'] + antena['radio']

        quito_anterior = False

    return solucion

def comprobar_solucion(solucion, kilometros):
    """
    Recibe una solucion y los kilometros de longitud de la ruta.
    Devuelve True si la solucion cubre los kilometros de ruta o False en caso contrario.
    """
    posicion = 0

    for antena in solucion:
        if antena['pos'] - antena['radio'] <= posicion:
            posicion = antena['pos'] + antena['radio']
        else:
            # Tramo queda sin cubrir
            return False

        if posicion >= kilometros:
            return True

    # No cubre todo
    return False

def main():
    if len(sys.argv) < 3:
        print("Error: faltan parámetros.")
        print("Uso: python3 solucion.py <kilometros> <ruta_archivo>")
        return

    kilometros = int(sys.argv[1])
    ruta_archivo = sys.argv[2]
    antenas = leer_antenas(ruta_archivo)
    solucion = buscar_solucion(antenas, kilometros)

    if comprobar_solucion(solucion, kilometros):
        print(list(map(lambda x: x['nro'], solucion)))
    else:
        print("No existe solución óptima.")

main()