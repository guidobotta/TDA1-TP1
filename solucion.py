import sys

def leer_contratos(ruta_archivo):
    contratos = []

    with open(ruta_archivo) as archivo:
        for linea in archivo:
            linea = linea.strip()
            nro, pos, radio = linea.split(',')
            contratos.append({"nro": int(nro), "pos": int(pos), "radio": int(radio)})

    return contratos

def cubre_anterior(contrato, solucion):
    if not solucion: return False
    
    cubrimiento_contrato = contrato["pos"] - contrato["radio"]
    cubrimiento_anterior = solucion[-1]["pos"] - solucion[-1]["radio"]

    if len(solucion) > 1 and solucion[-2]["pos"] + solucion[-2]["radio"] > cubrimiento_anterior:
        cubrimiento_anterior = solucion[-2]["pos"] + solucion[-2]["radio"]

    if cubrimiento_anterior < 0:
        cubrimiento_anterior = 0

    return cubrimiento_contrato <= cubrimiento_anterior

def buscar_solucion(contratos, kilometros):
    contratos_ordenados = sorted(contratos, key=lambda antena: (antena["pos"], antena["radio"])) # Se podría hacer inplace para ahorrar en memoria
    solucion = [contratos_ordenados[0]]
    quito_anterior = False

    for antena in contratos_ordenados[1:]:
        while cubre_anterior(antena, solucion):
            quito_anterior = True
            solucion.pop()
        
        if quito_anterior or antena["pos"] < kilometros:
            solucion.append(antena)
        quito_anterior = False

    return solucion

def comprobar_solucion(solucion, kilometros):
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
    contratos = leer_contratos(ruta_archivo)
    solucion = buscar_solucion(contratos, kilometros)

    if comprobar_solucion(solucion, kilometros):
        print(list(map(lambda x: x['nro'], solucion)))
    else:
        print("No existe solución óptima.")

main()