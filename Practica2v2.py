import sys
from collections import Counter

class Nodo():
    def __init__(self, izquierda=None, derecha=None):
        self.izquierda = izquierda
        self.derecha = derecha
    
    def hijos(self):
        return self.izquierda, self.derecha
    
    def __str__(self):
        return self.izquierda, self.derecha

def arbol(nodos):
    while len(nodos) > 1:
        c1, f1 = nodos[-1]
        c2, f2 = nodos[-2]
        nodos = nodos[:-2]
        nodo = Nodo(c1, c2)
        nodos.append((nodo, f1 + f2))
        nodos = sorted(nodos, key=lambda x: x[1], reverse=True)
    return nodos[0][0]

def huffman(nodo, binario=''):
    if type(nodo) is str:
        return { nodo: binario }
    (izq, der) = nodo.hijos()
    d = dict()
    d.update(huffman(izq, binario + '0'))
    d.update(huffman(der, binario + '1'))
    return d

if len(sys.argv) == 1:
    print("Provea un archivo o cadena.")
    exit()
try:
    cadena = open(sys.argv[1], "r").read()
except:
    cadena = sys.argv[1]

frecuencias = dict(Counter(cadena))
frecuencias = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)
nodo = arbol(frecuencias)
codificacion = huffman(nodo)
for i in codificacion:
    print(f"{i}: {codificacion[i]}")