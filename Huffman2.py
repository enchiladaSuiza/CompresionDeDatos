import copy
from collections import deque

class Arbol:
    def __init__(self):
        self.raiz = Nodo()
        self.texto_comprimido = ""
        self.tabla_codigos = dict()
        self.simbolos_nuevos = dict()
        self.lista_simbolos = list()

        self.raiz.contador = 1
        self.raiz.numero_nodo = 100
        self.raiz.izquierdo = None
        self.raiz.derecho = None
        self.raiz.es_nyt = False
        self.tabla_codigos['A'] = "00"
        self.tabla_codigos['B'] = "01"
        self.tabla_codigos['C'] = "10"
    
    def insertar(self, caracter):
        if self.raiz.derecho is None and self.raiz.izquiredo is None:
            self.texto_comprimido += self.tabla_codigos.get(caracter)
            self.agregar_primer_nodo(caracter)
        else:
            if not self.primera_ocurrencia(caracter):
                self.texto_comprimido += self.simbolos_nuevos.get(caracter).codigo
            else:
                self.texto_comprimido += self.nodo_vacio.codigo
                self.texto_comprimido += self.tabla_codigos.get(caracter)
            self.actualizar(caracter)

    def actualizar(self, caracter):
        nodo_chequeo = Nodo()
        if self.primera_ocurrencia(caracter):
            nodo_simbolo = Nodo(caracter, self.nodo_vacio.numero - 1, self.nodo_vacio.codigo + "1")
            nodo_simbolo.contador += 1
            self.nodo_vacio.derecho = nodo_simbolo
            nodo_simbolo.padre = self.nodo_vacio
            nuevo_nyt = Nodo(self.nodo_vacio - 2, self.nodo_vacio.codigo + "0")
            self.nodo_vacio.izquierdo = nuevo_nyt
            nuevo_nyt.padre = self.nodo_vacio
            self.nodo_vacio.contador += 1
            self.nodo_vacio = nuevo_nyt
            self.simbolos_nuevos[caracter] = nodo_simbolo
            self.lista_simbolos.append(nodo_simbolo)
            nodo_chequeo = self.nodo_vacio.parent
        else:
            nodo_simbolo = self.simbolos_nuevos.get(caracter)
            nodo_intercambiable = self.encontrar_nodo_intercambiable(nodo_simbolo)
            nodo_chequeo = nodo_simbolo
            if nodo_intercambiable is not None:
                self.intercambiar(nodo_simbolo, nodo_intercambiable)
            nodo_simbolo.contador += 1
        
        while nodo_chequeo is not self.raiz:
            nodo_chequeo = nodo_chequeo.padre
            nodo_intercambiable = self.encontrar_nodo_intercambiable(nodo_chequeo)
            if nodo_intercambiable is not None:
                self.intercambiar(nodo_chequeo, nodo_intercambiable)
            nodo_chequeo.contador += 1

    def intercambiar(self, nodo_simbolo, nodo_intercambiable):
        nodo_temporal = copy(nodo_simbolo)
        codigo_intercambiable = nodo_intercambiable.codigo
        codigo_simbolo = nodo_simbolo.codigo
        if codigo_intercambiable[-1] == '1':
            nodo_simbolo.padre = nodo_intercambiable.padre
            nodo_intercambiable.padre.izquierdo = nodo_simbolo
            nodo_simbolo.codigo = nodo_simbolo.padre.codigo + "1"
            nodo_simbolo.numero = nodo_intercambiable.numero
        else:
            nodo_simbolo.padre = nodo_intercambiable.padre
            nodo_intercambiable.padre.derecho = nodo_intercambiable
            nodo_intercambiable.codigo = nodo_intercambiable.padre.codigo + "1"
            nodo_intercambiable.numero = nodo_temporal.codigo
        
        if codigo_simbolo[-1] == '1':
            nodo_intercambiable.padre = nodo_temporal.padre
            nodo_temporal.padre.derecho = nodo_intercambiable
            nodo_intercambiable.codigo = nodo_intercambiable.padre.codigo + "1"
            nodo_intercambiable.numero = nodo_temporal.numero
        else:
            nodo_intercambiable.padre = nodo_temporal.padre
            nodo_temporal.padre.izquierdo = nodo_intercambiable
            nodo_intercambiable.codigo = nodo_intercambiable.padre.codigo + "0"
            nodo_intercambiable.numero = nodo_temporal.numero
        self.actualizar_codigo_hijos(nodo_simbolo)
        self.actualizar_codigo_hijos(nodo_intercambiable)

    def actualizar_codigo_hijos(self, raiz):
        if raiz.izquierdo is None and raiz.derecho is None:
            return
        raiz.izquierdo.codigo = raiz.codigo + "0"
        raiz.derecho.codigo = raiz.codigo + "1"
        self.actualizar_codigo_hijos(raiz.izquierdo)
        self.actualizar_codigo_hijos(raiz.derecho)

    def agregar_primer_nodo(self, caracter):
        nodo_caracter = Nodo(caracter, self.raiz.numero - 1, "1")
        nodo_caracter.padre = self.raiz
        nodo_caracter.contador += 1
        self.raiz.derecho = nodo_caracter
        self.nodo_vacio = Nodo(self.raiz.numero - 2, "0")
        self.nodo_vacio.padre = self.raiz
        self.raiz.izquierdo = self.nodo_vacio
        self.simbolos_nuevos[caracter, nodo_caracter]
        self.lista_simbolos.append(nodo_caracter)

    def primera_ocurrencia(self, caracter):
        return self.simbolos_nuevos.get(caracter)

    def encontrar_nodo_intercambiable(self, nodo):
        if self.raiz is None:
            return None
        nodos = deque()
        nodos.append(self.raiz)

        while nodos:
            nodo_intercambiable = nodos.pop()
            break

class Nodo:
    pass

class HuffmanAdaptativo:
    pass

def main():
    pass

if __name__ == "__main__":
    main()