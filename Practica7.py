import sys
from collections import Counter
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
	QTableWidgetItem,
	QLabel,
	QSpinBox
)
from PyQt6.QtGui import (
	QShortcut,
	QKeySequence,
)
from PyQt6.QtCore import Qt

class Ventana(QMainWindow):
	def __init__(self):
		super().__init__(parent=None)
		self.setWindowTitle("Práctica 6 - PPM")
		self.setMinimumWidth(600)

		cerrar = QShortcut(QKeySequence('Ctrl+Q'), self)
		cerrar.activated.connect(QApplication.instance().quit)

		contenedor = QWidget()
		layout = QGridLayout(contenedor)
		contenedor.setLayout(layout)
		self.setCentralWidget(contenedor)

		boton_archivo = QPushButton("Seleccionar un archivo...")
		boton_archivo.clicked.connect(self.seleccionar_archivo)

		self.entrada = QTextEdit()
		self.entrada.setPlaceholderText("Entrada")
		self.entrada.textChanged.connect(self.entrada_actualizada)

		self.tabla_diccionario = QTableWidget()
		self.tabla_diccionario.setColumnCount(2)
		self.tabla_diccionario.setHorizontalHeaderLabels(["Índice", "Cadena"])
		self.tabla_diccionario.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

		self.tabla_cadenas = QTableWidget()
		self.tabla_cadenas.setColumnCount(4)
		self.tabla_cadenas.setHorizontalHeaderLabels(["Índice", "P", "C", "P + C"])
		self.tabla_cadenas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

		self.salida = QLabel()
		self.salida.setAlignment(Qt.AlignmentFlag.AlignCenter)
		
		layout.addWidget(boton_archivo, 0, 0, 1, 2)
		layout.addWidget(self.entrada, 1, 0, 1, 2)
		layout.addWidget(self.tabla_diccionario, 2, 0)
		layout.addWidget(self.tabla_cadenas, 2, 1)
		layout.addWidget(self.salida, 3, 0, 1, 2)

	def entrada_actualizada(self):
		texto = self.entrada.toPlainText()
		diccionario, cadenas, salida = Lzm().codificar(texto)

		self.tabla_diccionario.clearContents()
		self.tabla_diccionario.setRowCount(len(diccionario))
		for i, cadena in enumerate(diccionario):
			self.tabla_diccionario.setItem(i, 0, self.item_tabla(i))
			self.tabla_diccionario.setItem(i, 1, self.item_tabla(cadena))

		self.tabla_cadenas.clearContents()
		self.tabla_cadenas.setRowCount(len(cadenas))
		for i, fila in enumerate(cadenas):
			for j, item in enumerate(fila):
				self.tabla_cadenas.setItem(i, j, self.item_tabla(item))

		self.salida.setText(str(salida))

	def seleccionar_archivo(self):
		nombre_archivo, _ = QFileDialog.getOpenFileName(self, "Seleccione un archivo.", "./")
		if nombre_archivo:
			texto = open(nombre_archivo, "r").read()
			self.entrada.setText(texto)

	def item_tabla(self, valor):
		item = QTableWidgetItem(str(valor))
		item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
		return item
			
class Lzm:
	def __init__(self):
		pass

	def codificar(self, texto):
		diccionario = list(sorted(set(texto)))
		cadenas = list()
		codificacion = list()
		texto += '§'
		p = ''
		for c in texto:
			f = p + c
			if not p:
				cadenas.append(['-', p, c, f])
				p = c
				continue
			if f in diccionario:
				cadenas.append(['-', p, c, f])
				p = f
				continue
			diccionario.append(f)
			resultado = diccionario.index(p)
			codificacion.append(resultado)
			cadenas.append([resultado, p, c, f])
			p = c
		
		return diccionario, cadenas, codificacion

def main():
	app = QApplication([])
	ventana = Ventana()
	ventana.show()
	sys.exit(app.exec())

if __name__ == "__main__":
	main()