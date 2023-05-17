import sys

class Nodo:
    def __init__(self, frecuencia, caracter, izquierda=None, derecha=None):
        self.frecuencia = frecuencia
        self.caracter = caracter
        self.izquierda = izquierda
        self.derecha = derecha
        self.codigo = ''

codigos = dict()

def calcular_frecuencia(cadena):
    caracteres = dict()
    for caracter in cadena:
        if caracteres.get(caracter) == None:
            caracteres[caracter] = 1
        else:
            caracteres[caracter] += 1
    return caracteres

def calcular_codigos(nodo, valor=''):
    nuevo_valor = valor + str(nodo.codigo)
    if nodo.izquierda:
        calcular_codigos(nodo.izquierda, nuevo_valor)
    if nodo.derecha:
        calcular_codigos(nodo.derecha, nuevo_valor)
    if not nodo.izquierda and not nodo.derecha:
        codigos[nodo.caracter] = nuevo_valor

def salida_codificada(cadena, codificacion):
    salida = []
    for caracter in cadena:
        salida.append(codificacion[caracter])
    binario = ''.join([str(bits) for bits in salida])
    return binario

def imprimir_codigos():
    print("Car.\tCod.")
    for caracter, codigo in codigos.items():
        print(f"{caracter}\t{codigo}")

def huffman(cadena):
    caracteres_frecuencias = calcular_frecuencia(cadena)
    nodos = []
    for caracter, frecuencia in caracteres_frecuencias.items():
        nodos.append(Nodo(frecuencia, caracter))

    while len(nodos) > 1:
        nodos = sorted(nodos, key=lambda x:(x.frecuencia, x.caracter))
        derecha = nodos[1]
        izquierda = nodos[0]
        derecha.codigo = 1
        izquierda.codigo = 0
        nuevo_nodo = Nodo(izquierda.frecuencia + derecha.frecuencia, izquierda.caracter + derecha.caracter, izquierda, derecha)
        nodos.remove(derecha)
        nodos.remove(izquierda)
        nodos.append(nuevo_nodo)
    
    calcular_codigos(nodos[0])
    imprimir_codigos()

    salida = salida_codificada(cadena, codigos)
    return salida

if len(sys.argv) == 1:
    print("Provea un archivo o cadena.")
    exit()
try:
    cadena = open(sys.argv[1], "r").read()
except:
    cadena = sys.argv[1]

codificacion = huffman(cadena)
print(codificacion)