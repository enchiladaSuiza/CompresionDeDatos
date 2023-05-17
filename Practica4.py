import sys
from PyQt6.QtWidgets import (
	QApplication,
	QMainWindow,
	QWidget,
	QGridLayout,
	QTextEdit,
	QPushButton,
	QFileDialog,
	QTableWidget,
	QHeaderView,
	QTableWidgetItem
)
from PyQt6.QtGui import (
	QShortcut,
	QKeySequence,
)
from PyQt6.QtCore import Qt

class Nodo:
	def __init__(self, padre=None, izquierdo=None, derecho=None, peso=0, simbolo=''):
		self.padre = padre
		self.izquierdo = izquierdo
		self.derecho = derecho
		self.peso = peso
		self.simbolo = simbolo

class HuffmanAdaptativo:
	def __init__(self):
		self.nyt = Nodo(simbolo="NYT")
		self.raiz = self.nyt
		self.nodos = []
		self.vistos = [None] * 256
		self.codigos = dict()

	def codigo(self, simbolo, nodo, codigo=''):
		if nodo.izquierdo is None and nodo.derecho is None:
			return codigo if nodo.simbolo == simbolo else ''
		else:
			temp = ''
			if nodo.izquierdo is not None:
				temp = self.codigo(simbolo, nodo.izquierdo, codigo + '0')
			if not temp and nodo.derecho is not None:
				temp = self.codigo(simbolo, nodo.derecho, codigo + '1')
			return temp
		
	def mayor_nodo(self, peso):
		for n in reversed(self.nodos):
			if n.peso == peso:
				return n
	
	def intercambiar(self, n1, n2):
		i1, i2 = self.nodos.index(n1), self.nodos.index(n2)
		self.nodos[i1], self.nodos[i2] = self.nodos[i2], self.nodos[i1]

		padre_temp = n1.padre
		n1.padre = n2.padre
		n2.padre = padre_temp

		if n1.padre.izquierdo is n2:
			n1.padre.izquierdo = n1
		else:
			n1.padre.derecho = n1
		
		if n2.padre.izquierdo is n1:
			n2.padre.izquierdo = n2
		else:
			n2.padre.derecho = n2

	def insertar(self, s):
		nodo = self.vistos[ord(s)]

		if nodo is None:
			spawn = Nodo(simbolo=s, peso=1)
			interno = Nodo(simbolo='', peso=1, padre=self.nyt.padre, izquierdo=self.nyt, derecho=spawn)
			spawn.padre = interno
			self.nyt.padre = interno

			if interno.padre is not None:
				interno.padre.izquierdo = interno
			else:
				self.raiz = interno
			
			self.nodos.insert(0, interno)
			self.nodos.insert(0, spawn)

			self.vistos[ord(s)] = spawn
			nodo = interno.padre

		while nodo is not None:
			mayor = self.mayor_nodo(nodo.peso)
			if nodo is not mayor and nodo is not mayor.padre and mayor is not nodo.padre:
				self.intercambiar(nodo, mayor)

			nodo.peso = nodo.peso + 1
			nodo = nodo.padre

	def codificar(self, texto):
		self.codigos.clear()
		resultado = ''
		for s in texto:
			if self.vistos[ord(s)]:
				codigo = self.codigo(s, self.raiz)
				resultado += codigo
			else:
				codigo = self.codigo('NYT', self.raiz) + bin(ord(s))[2:].zfill(8)
				resultado += codigo 
			self.codigos[s] = codigo
			self.insertar(s)
		return resultado
	
	def simbolo_por_ascii(self, binario):
		return chr(int(binario, 2))
	
	def decodificar(self, texto):
		resultado = ''
		simbolo = self.simbolo_por_ascii(texto[:8])
		resultado += simbolo
		self.insertar(simbolo)
		nodo = self.raiz

		i = 8
		while i < len(texto):
			nodo = nodo.izquierdo if texto[i] == '0' else nodo.derecho
			simbolo = nodo.simbolo
			if simbolo:
				if simbolo == 'NYT':
					simbolo = self.simbolo_por_ascii(texto[i+1:i+9])
					i += 8
				resultado += simbolo
				self.insertar(simbolo)
				nodo = self.raiz
			i += 1
		return resultado

class Ventana(QMainWindow):
	def __init__(self):
		super().__init__(parent=None)
		self.setWindowTitle("Práctica 4 - Codificación Adaptativa de Huffman")
		self.setMinimumWidth(400)

		cerrar = QShortcut(QKeySequence('Ctrl+Q'), self)
		cerrar.activated.connect(QApplication.instance().quit)

		contenedor = QWidget()
		layout = QGridLayout(contenedor)
		contenedor.setLayout(layout)
		self.setCentralWidget(contenedor)

		self.entrada_textedit = QTextEdit()
		self.entrada_textedit.setPlaceholderText("Entrada")
		self.entrada_textedit.textChanged.connect(self.entrada_actualizada)

		self.salida_textedit = QTextEdit()
		self.salida_textedit.setPlaceholderText("Salida")

		boton_archivo = QPushButton("Seleccionar un archivo...")
		boton_archivo.clicked.connect(self.seleccionar_archivo)

		self.codigos_tabla = QTableWidget()
		self.codigos_tabla.setColumnCount(2)
		self.codigos_tabla.setHorizontalHeaderLabels(["Carácter", "Código"])
		self.codigos_tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

		layout.addWidget(boton_archivo, 0, 0)
		layout.addWidget(self.entrada_textedit, 1, 0)
		layout.addWidget(self.codigos_tabla, 0, 1, 2, 1)
		layout.addWidget(self.salida_textedit, 2, 0, 1, 2)

	def seleccionar_archivo(self):
		nombre_archivo, _ = QFileDialog.getOpenFileName(self, "Seleccione un archivo.", "./")
		if nombre_archivo:
			texto = open(nombre_archivo, "r").read()
			self.entrada_textedit.setText(texto)

	def entrada_actualizada(self):
		huffman = HuffmanAdaptativo()
		texto = self.entrada_textedit.toPlainText()
		texto_codificado = huffman.codificar(texto)
		self.salida_textedit.setText(texto_codificado)
		self.codigos_tabla.clearContents()
		self.codigos_tabla.setRowCount(0)
		for caracter, codigo in huffman.codigos.items():
			fila = self.codigos_tabla.rowCount()
			self.codigos_tabla.insertRow(fila)
			self.codigos_tabla.setItem(fila, 0, self.item_tabla(caracter))
			self.codigos_tabla.setItem(fila, 1, self.item_tabla(codigo))

	def item_tabla(self, valor):
		item = QTableWidgetItem(valor)
		item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
		return item

def main():
	app = QApplication([])
	ventana = Ventana()
	ventana.show()
	sys.exit(app.exec())

if __name__ == "__main__":
	main()
