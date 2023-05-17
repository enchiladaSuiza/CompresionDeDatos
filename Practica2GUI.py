import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFileDialog,
)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Práctica 2 - Algoritmo de Huffman")
        self.setGeometry(400, 200, 600, 400)
        
        contenedor = QWidget(self)
        gridlayout = QGridLayout()
        contenedor.setLayout(gridlayout)
        self.setCentralWidget(contenedor)

        entrada_widget = QWidget()
        self.entrada_textedit = QTextEdit()
        self.entrada_textedit.setPlaceholderText("Escriba aquí la cadena de entrada o seleccione un archivo.")
        self.entrada_textedit.textChanged.connect(self.entrada_actualizada)
        entrada_boton = QPushButton("Seleccionar un archivo...")
        entrada_boton.clicked.connect(self.seleccionar_archivo)

        entrada_vbox = QVBoxLayout()
        entrada_widget.setLayout(entrada_vbox)
        entrada_vbox.addWidget(self.entrada_textedit)
        entrada_vbox.addWidget(entrada_boton)

        codigos_widget = QWidget()
        self.codigos_tabla = QTableWidget()
        self.codigos_tabla.setColumnCount(2)
        self.codigos_tabla.setHorizontalHeaderLabels(["Carácter", "Código"])
        self.codigos_tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        codigos_vbox = QVBoxLayout()
        codigos_widget.setLayout(codigos_vbox)
        codigos_vbox.addWidget(self.codigos_tabla)

        salida_widget = QWidget()
        self.salida_textedit = QTextEdit()
        self.salida_textedit.setPlaceholderText("Aquí aparecerá la cadena de bits del texto codificado.")
        self.salida_textedit.setReadOnly(True)

        salida_vbox = QVBoxLayout()
        salida_widget.setLayout(salida_vbox)
        salida_vbox.addWidget(self.salida_textedit)

        gridlayout.addWidget(entrada_widget, 0, 0)
        gridlayout.addWidget(codigos_widget, 0, 1)
        gridlayout.addWidget(salida_widget, 1, 0, 1, 2)
    
    def entrada_actualizada(self):
        texto = self.entrada_textedit.toPlainText()
        salida = huffman(texto)

        self.codigos_tabla.clearContents()
        self.codigos_tabla.setRowCount(0)
        for caracter, codigo in codigos.items():
            fila = self.codigos_tabla.rowCount()
            self.codigos_tabla.insertRow(fila)
            self.codigos_tabla.setItem(fila, 0, QTableWidgetItem(caracter))
            self.codigos_tabla.setItem(fila, 1, QTableWidgetItem(codigo))
        
        codigos.clear()
        self.salida_textedit.setText(salida)

    def seleccionar_archivo(self):
        nombre_archivo, ok = QFileDialog.getOpenFileName(self, "Seleccione un archivo.", "./")
        if nombre_archivo:
            texto = open(nombre_archivo, "r").read()
            self.entrada_textedit.setText(texto)

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

def huffman(cadena):
    if not cadena:
        return
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

    salida = salida_codificada(cadena, codigos)
    return salida

def main():
    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()