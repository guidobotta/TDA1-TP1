import sys

def cubre_anterior(contrato, solucion):
    return solucion[-1]

def buscar_solucion(contratos, kilometros):
    contratos_ordenados = sorted(contratos, key=lambda x: x[1]) # Se podría hacer inplace para ahorrar en memoria
    solucion = [contratos_ordenados[0]]
    posicion = contratos_ordenados[0][1] + contratos_ordenados[0][2]

    for contrato in contratos_ordenados[1:]:
        while cubre_anterior(contrato, solucion):
            solucion.pop()
        
        solucion.append(contrato)

    return solucion

def leer_contratos(ruta_archivo):
    contratos = []

    with open(ruta_archivo) as archivo:
        for linea in archivo:
            nro, pos, radio = linea.split(',')
            contratos += (nro, pos, radio)

def main():
    if len(sys.argv) < 3:
        print("Error: faltan parámetros.")
        print("Uso: python3 solucion.py <kilometros> <ruta_archivo>")
        return

    kilometros = sys.argv[1]
    ruta_archivo = sys.argv[2]
    contratos = leer_contratos(ruta_archivo)
    buscar_solucion(contratos, kilometros)

main()