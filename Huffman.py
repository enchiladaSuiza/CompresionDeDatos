import sys, heapq, contextlib

class CodificadorHuffman:
    def __init__(self, bits_salida):
        self.salida = bits_salida
        self.arbol = None
   
    def escribir(self, simbolo):
        bits = self.arbol.conseguir_codigo(simbolo)
        for bit in bits:
            self.salida.write(bit)

class DecodificadorHuffman:
    def __init__(self, bits_entrada):
        self.entrada = bits_entrada
        self.arbol = None
   
    def leer(self):
        nodo_actual = self.entrada.raiz
        while True:
            auxiliar = self.input.leer_sin_eof()
            if auxiliar == 0:
                siguiente_nodo = nodo_actual.hijo_izquierdo
            else:
                siguiente_nodo = nodo_actual.hijo_derecho
            if isinstance(siguiente_nodo, Hoja):
                return siguiente_nodo.simbolo
            else:
                nodo_actual = siguiente_nodo

class TablaFrecuencias:
    def __init__(self, frecuencias):
        self.frecuencias = list(frecuencias)
   
    def total_simbolos(self):
        return len(self.frecuencias)
   
    def conseguir(self, simbolo):
        return self.frecuencias[simbolo]
   
    def establecer(self, simbolo, frecuencia):
        self.frecuencias[simbolo] = frecuencia
   
    def incrementar(self, simbolo):
        self.frecuencias[simbolo] += 1

    def __str__(self):
        resultado = ""
        for i, frecuencia in enumerate(self.frecuencias):
            resultado += f"{i}\t{frecuencia}\n"
        return resultado

    def constuir_arbol(self):
        cola_prioridad = []
        for i, frecuencia in enumerate(self.frecuencias):
            if frecuencia > 0:
                heapq.heappush(cola_prioridad, (frecuencia, i, Hoja(i)))
        for i, frecuencia in enumerate(self.frecuencias):
            if len(cola_prioridad) >= 2:
                break
            if frecuencia == 0:
                heapq.heappush(cola_prioridad, (frecuencia, i, Hoja(i)))
        assert len(cola_prioridad) >= 2

        while len(cola_prioridad) > 1:
            x = heapq.heappop(cola_prioridad)
            y = heapq.heappop(cola_prioridad)
            z = (x[0] + y[0], min(x[1], y[i]), NodoInterno(x[2], y[2]))
            heapq.heappush(cola_prioridad, z)
       
        return Arbol(cola_prioridad[0][2], len(self.frecuencias))

class Arbol:
    def  __init__(self, raiz, total_simbolos):
        def construir_lista_codigos(nodo, prefijo):
            if isinstance(nodo, NodoInterno):
                construir_lista_codigos(nodo.hijo_izquierdo, prefijo + (0,))
                construir_lista_codigos(nodo.hijo_derecho, prefijo + (1,))
            else:
                self.codigos[nodo.simbolo] = prefijo
       
        self.raiz = raiz
        self.codigos = [None] * total_simbolos
        construir_lista_codigos(raiz, ())
   
    def conseguir_codigo(self, simbolo):
        return self.codigos[simbolo]
   
    def __str__(self):
        def a_string(prefijo, nodo):
            if isinstance(nodo, NodoInterno):
                return a_string(prefijo + "0", nodo.hijo_izquierdo) + a_string(prefijo + "0", nodo.hijo_derecho)
            else:
                return f"Código {prefijo}: Símbolo {nodo.simbolo}\n"
        return a_string("", self.raiz)

class Nodo:
    pass

class NodoInterno(Nodo):
    def __init__(self, izquierdo, derecho):
        self.hijo_izquierdo = izquierdo
        self.hijo_derecho = derecho

class Hoja(Nodo):
    def __init__(self, simbolo):
        self.simbolo = simbolo

class CodigoCanonico:
    def __init__(self, longitudes_codigo=None, arbol=None, total_simbolos=None):
        if longitudes_codigo is not None and arbol is None and total_simbolos is None:
            longitudes = sorted(longitudes_codigo, reverse=True)
            nivel_actual = longitudes[0]
            nodos_nivel = 0
            for c1 in longitudes:
                if c1 == 0:
                    break
                while c1 < nivel_actual:
                    nodos_nivel //= 2
                    nivel_actual += 1
                nodos_nivel += 1
            while nivel_actual > 0:
                nodos_nivel //= 2
                nivel_actual -= 1
            self.longitudes_codigo = list(longitudes_codigo)
        elif arbol is not None and total_simbolos is not None and longitudes_codigo is None:
            def construir_longitudes(nodo, profundidad):
                if isinstance(nodo, NodoInterno):
                    construir_longitudes(nodo.hijo_izquierdo, profundidad + 1)
                    construir_longitudes(nodo.hijo_derecho, profundidad + 1)
                elif isinstance(nodo, Hoja):
                    self.longitudes_codigo[nodo.simbolo] = profundidad
            
            self.longitudes_codigo = [0] * total_simbolos
            construir_longitudes(arbol.raiz, 0)
    
    def conseguir_total_simbolos(self):
        return len(self.longitudes_codigo)

    def conseguir_longitud_codigo(self, simbolo):
        if 0 <= simbolo < len(self.longitudes_codigo):
            return self.longitudes_codigo[simbolo]
    
    def a_arbol(self):
        nodos = []
        for i in range(max(self.longitudes_codigo), -1, -1):
            assert len(nodos) % 2 == 0
            nodos_nuevos = []

            if i > 0:
                for j, longitud in enumerate(self.longitudes_codigo):
                    if longitud == i:
                        nodos_nuevos.append(Hoja(j))
            for j in range(0, len(nodos), 2):
                nodos_nuevos.append(NodoInterno(nodos[j], nodos[j + 1]))
            nodos = nodos_nuevos
            
        assert len(nodos) == 1
        return Arbol(nodos[0], len(self.conseguir_longitud_codigo))

class StreamBitsEntrada:
    def __init__(self, entrada):
        self.entrada = entrada
        self.byte_actual = 0
        self.bits_faltantes = 0
    
    def leer(self):
        if self.byte_actual == -1:
            return -1
        if self.bits_faltantes == 0:
            auxiliar = self.entrada.leer(1)
            if len(auxiliar) == 0:
                self.byte_actual = -1
                return -1
            self.byte_actual = auxiliar[0]
            self.bits_faltantes = 8
        assert self.bits_faltantes > 0
        self.bits_faltantes -= 1
        return (self.byte_actual >> self.bits_faltantes) & 1

    def cerrar(self):
        self.entrada.close()
        self.byte_actual = -1
        self.bits_faltantes = 0

class StreamBitsSalida:
    def __init__(self, salida):
        self.salida = salida
        self.byte_actual = 0
        self.bits_faltantes = 0
        self.bits_rellenados = 0
    
    def escribir(self, b):
        self.byte_actual = (self.byte_actual << 1) | b
        self.bits_faltantes += 1
        if self.bits_rellenados == 8:
            a_escribir = bytes((self.byte_actual,))
            self.salida.escribir(a_escribir)
            self.byte_actual = 0
            self.bits_rellenados = 0
        
    def cerrar(self):
        while self.bits_rellenados != 0:
            self.escribir(0)
        self.salida.close()

def main(argumentos):
    if len(argumentos) != 2:
        sys.exit("Provea un archivo de entrada y uno de salida.")
    archivo_entrada, archivo_salida = argumentos

    with open(archivo_entrada, "rb") as entrada, \
        contextlib.closing(StreamBitsSalida(open(archivo_salida, "wb"))) as bitout:
        comprimir(entrada, bitout)
    
def comprimir(entrada, bitout):
    frecuencias_inciales = [1] * 257
    frecuencias = TablaFrecuencias(frecuencias_inciales)
    codificacion = CodificadorHuffman(bitout)
    codificacion.arbol = frecuencias.constuir_arbol()
    count = 0
    while True:
        simbolo = entrada.read(1)
        if len(simbolo) == 0:
            break
        codificacion.escribir(simbolo[0])
        if (count < 262144 and es_potencia_de_2(count)) or count % 262144 == 0:
            codificacion.arbol = frecuencias.constuir_arbol()
        if count % 262144 == 0:
            frecuencias = TablaFrecuencias(frecuencias_inciales)
    codificacion.escribir(256)

def es_potencia_de_2(x):
    return x > 0 and x & (x - 1) == 0

if __name__ == "__main__":
    main(sys.argv[1:])