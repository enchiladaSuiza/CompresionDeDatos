import math

k = 3
mensaje = input()

bits = list()
tabla = [dict() for i in range(k + 2)]
escape = "<$>"

tabla[0][''] = dict()
for i in range (2**8):
    tabla[0][''][chr(i)] = 1

def predecir(c, contexto, s, imposible):
    if contexto in tabla[s + 1]:
        copia = tabla[s + 1][contexto].copy()
        for llave in imposible:
            if llave in copia:
                copia.pop(llave)
        distinto = 0 if s == -1 else len(copia.keys())
        suma = sum(copia.values())
        if c in copia:
            p = float(copia[c] / float(distinto + suma))
            bits.append(-math.log(p, 2))
            if c == '':
                print()
            else:
                print(f"{c}, {p}")
        else:
            if suma > 0:
                p = float(distinto) / float(distinto + suma)
                bits.append(-math.log(p, 2))
                print(f"{escape}, {p}")
            predecir(c, contexto[1:], s - 1, imposible + list(copia.keys()))
    else:
        predecir(c, contexto[1:], s - 1, imposible)

def actualizar(c, contexto):
    for i in range(0, len(contexto) + 1):
        pre = contexto[1:]
        s = len(pre)
        if pre not in tabla[s + 1]:
            tabla[s + 1][pre] = dict()
        if c not in tabla[s + 1][pre]:
            tabla[s + 1][pre][c] = 0
        tabla[s + 1][pre][c] += 1

for i in range(len(mensaje)):
    c = mensaje[i]
    inicio = i - k if i > k else 0
    contexto = mensaje[inicio:1]
    predecir(c, contexto, len(contexto), [])
    actualizar(c, contexto)

print(f"Bits totales: {sum(bits)}")