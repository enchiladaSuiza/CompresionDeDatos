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
	QLabel
)
from PyQt6.QtGui import (
	QShortcut,
	QKeySequence,
)
from PyQt6.QtCore import Qt

class Ventana(QMainWindow):
	def __init__(self):
		super().__init__(parent=None)
		self.setWindowTitle("Práctica 5 - Codificación Aritmética")
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

		self.salida_label = QLabel()
		self.salida_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

		boton_archivo = QPushButton("Seleccionar un archivo...")
		boton_archivo.clicked.connect(self.seleccionar_archivo)

		self.tabla = QTableWidget()
		self.tabla.setColumnCount(4)
		self.tabla.setHorizontalHeaderLabels(["Carácter", "Frecuencia", "Probabilidad", "Intervalo"])
		self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

		layout.addWidget(boton_archivo, 0, 0)
		layout.addWidget(self.entrada_textedit, 1, 0)
		layout.addWidget(self.tabla, 2, 0)
		layout.addWidget(self.salida_label, 3, 0)

	def entrada_actualizada(self):
		texto = self.entrada_textedit.toPlainText()
		longitud = len(texto)
		frecuencias = dict(Counter(texto))
		probabilidades = { c: f / longitud for c, f in frecuencias.items() }
		intervalos = dict()
		acumulador = 0
		
		self.tabla.clearContents()
		self.tabla.setRowCount(0)
		for c, p in probabilidades.items():
			auxiliar = acumulador
			acumulador += p
			intervalos[c] = [auxiliar, acumulador]
			fila = self.tabla.rowCount()
			self.tabla.insertRow(fila)
			self.tabla.setItem(fila, 0, self.item_tabla(c))
			self.tabla.setItem(fila, 1, self.item_tabla(str(frecuencias[c])))
			self.tabla.setItem(fila, 2, self.item_tabla(str(probabilidades[c])))
			self.tabla.setItem(fila, 3, self.item_tabla(f"[{auxiliar}, {acumulador})"))
		
		a, b = 0, 1
		for c in texto:
			inf = a + (b - a) * intervalos[c][0]
			sup = a + (b - a) * intervalos[c][1]
			a, b = inf, sup
			
		self.salida_label.setText(f"[{a}, {b})")
		
	def seleccionar_archivo(self):
		nombre_archivo, _ = QFileDialog.getOpenFileName(self, "Seleccione un archivo.", "./")
		if nombre_archivo:
			texto = open(nombre_archivo, "r").read()
			self.entrada_textedit.setText(texto)

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
