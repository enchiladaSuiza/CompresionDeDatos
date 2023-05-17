import sys
import math

if len(sys.argv) == 1:
    print("Provea un archivo o cadena.")
    exit()
try:
    contenido = open(sys.argv[1], "r").read()
except:
    contenido = sys.argv[1]

diccionario = { }
total = len(contenido)
for caracter in contenido:
    if diccionario.get(caracter) == None:
        diccionario[caracter] = 1
    else:
        diccionario[caracter] += 1
       
caracteres = len(diccionario)
ordenamiento = sorted(diccionario.items(), key=lambda x:x[1], reverse=True)
diccionario_ordenado = dict(ordenamiento)

print("Car.\tAbs.\tAbs.Ac.\tRel.\tAbs.Rel.")
frec_abs_ac = 0
frec_rel_ac = 0
for caracter, frecuencia in diccionario_ordenado.items():
    frec_abs_ac += frecuencia
    frec_rel = round(frecuencia / total, 5)
    frec_rel_ac = round(frec_rel_ac + frec_rel, 5)
    print(f"{caracter}\t{frecuencia}\t{frec_abs_ac}\t{frec_rel}\t{frec_rel_ac}")

media = total / caracteres
lista_frecuencias = list(diccionario_ordenado.values())
if caracteres % 2 == 0:
    mediana = lista_frecuencias[int(caracteres / 2)]
else:
    primero = lista_frecuencias[int(caracteres / 2)]
    segundo = lista_frecuencias[int((caracteres + 1) / 2)]
    mediana = (primero + segundo) / 2
moda = max(set(lista_frecuencias), key=lista_frecuencias.count)

rango = lista_frecuencias[0] - lista_frecuencias[-1]
varianza = 0
for frecuencia in lista_frecuencias:
    varianza += (frecuencia - media) ** 2
varianza /= caracteres
desviacion = math.sqrt(varianza)

print(f"Media: {media}, Mediana: {mediana}, Moda: {moda}")
print(f"Rango: {rango}, Varianza: {varianza}, Desviación Estándar: {desviacion}")