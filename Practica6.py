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

class Nodo:
	def __init__(self, s, n=0, padre=None):
		self.s = s
		self.n = n
		self.f = 1
		self.padre = padre
		self.vine = None
		self.hijos = list()

class Trie:
	def __init__(self, n=3):
		self.raiz = Nodo('')
		self.base = self.raiz
		self.n_limite = n
		self.tabla = TablaContextos()

	def insertar(self, s):
		actualizar_base = True
		x = self.base
		p = 0
		a = Nodo('')
		b = Nodo('')
		while True:
			if x.n >= self.n_limite:
				x = x.vine
				continue
			contiene = False
			for hijo in x.hijos:
					if hijo.s == s:
						contiene = True
						a = hijo
						a.f += 1
						break
			if not contiene:    
				a = Nodo(s, x.n + 1, x)
				x.hijos.append(a)
			b.vine = a
			y = a.padre
			contexto = ''
			while y:
				contexto = y.s + contexto
				y = y.padre
			self.tabla.insertar(contexto, a.s)
			if actualizar_base:
				actualizar_base = False
				self.base = a
				total = 0
				for hijo in a.padre.hijos:
					total += hijo.f + 1
				p = a.f / total
			if x.vine:
				x = x.vine
			else:
				a.vine = x
				break
			b = a
		return p

	def dfs(self, nodo):
		print(f"{nodo.s}: {nodo.f}")
		for hijo in nodo.hijos:
				self.dfs(hijo)
			
	def bfs(self, nodo):
		q = [nodo]
		while q:
			x = q.pop(0)
			print(f"{x.s}: {x.f}")
			for y in x.hijos:
				q.append(y)

	def valores(self):
		return self.tabla.valores_como_tabla()

class TablaContextos:
	def __init__(self):
		self.contextos = dict()

	def insertar(self, c, s):
		if c in self.contextos:
			if s in self.contextos[c]:
				self.contextos[c][s] += 1
			else:
				self.contextos[c][s] = 1
		else:
			self.contextos[c] = { s: 1 }

	def escape(self, c):
		if c in self.contextos:
			return len(self.contextos[c])

	def valores_como_tabla(self):
		valores = dict()
		self.contextos = dict(sorted(self.contextos.items(), key=lambda i: len(i[0])))
		for c in self.contextos.keys():
			escape = self.escape(c)
			total = escape + sum(self.contextos[c].values())
			valores[c] = list()
			for i, (s, f) in enumerate(self.contextos[c].items()):
				valores[c].append(list())
				valores[c][i].append(s)
				valores[c][i].append(f)
				valores[c][i].append(f / total)
			valores[c].append(list())
			valores[c][-1].append("esc")
			valores[c][-1].append(escape)
			valores[c][-1].append(escape / total)
			valores[c].append(list())
			valores[c][-1].append("total")
			valores[c][-1].append(total)
			valores[c][-1].append("1")
		return valores

class Codificador:
	def __init__(self, probabilidades):
		self.probabilidades = probabilidades
	
	def codificar(self, texto):
		intervalos = dict()
		acumulador = 0
		for s, p in self.probabilidades.items():
			auxiliar = acumulador
			acumulador += p
			intervalos[s] = [auxiliar, acumulador]
		a, b = 0, 1
		for s in texto:
			inf = a + (b - a) * intervalos[s][0]
			sup = a + (b - a) * intervalos[s][1]
			a, b = inf, sup
		return a, b

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

		self.entrada_textedit = QTextEdit()
		self.entrada_textedit.setPlaceholderText("Entrada")
		self.entrada_textedit.textChanged.connect(self.entrada_actualizada)

		self.selector_n = QSpinBox()
		self.selector_n.setValue(3)
		self.selector_n.valueChanged.connect(self.entrada_actualizada)

		self.tabla = QTableWidget()
		self.tabla.setColumnCount(4)
		self.tabla.setHorizontalHeaderLabels(["Contexto", "Símbolo", "Frecuencia", "Probabilidad"])
		self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

		self.salida_label = QLabel()
		self.salida_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		
		layout.addWidget(boton_archivo, 0, 0)
		layout.addWidget(self.entrada_textedit, 1, 0)
		layout.addWidget(self.selector_n, 2, 0)
		layout.addWidget(self.tabla, 3, 0)
		layout.addWidget(self.salida_label, 4, 0)

	def entrada_actualizada(self):
		texto = self.entrada_textedit.toPlainText()
		probabilidades = dict()
		trie = Trie(self.selector_n.value())
		for s in texto:
			probabilidades[s] = trie.insertar(s)
		self.actualizar_tabla(trie.valores())
		a, b = Codificador(probabilidades).codificar(texto)
		self.salida_label.setText(f"[{a}, {b})")


	def seleccionar_archivo(self):
		nombre_archivo, _ = QFileDialog.getOpenFileName(self, "Seleccione un archivo.", "./")
		if nombre_archivo:
			texto = open(nombre_archivo, "r").read()
			self.entrada_textedit.setText(texto)

	def item_tabla(self, valor):
		item = QTableWidgetItem(str(valor))
		item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
		return item

	def actualizar_tabla(self, valores):
		self.tabla.clearContents()
		self.tabla.setRowCount(0)
		c_actual = ''
		for c, info_simbolo in valores.items():
			for lista in info_simbolo:
				fila = self.tabla.rowCount()
				self.tabla.insertRow(fila)
				if c_actual != c:
					c_actual = c
					self.tabla.setItem(fila, 0, self.item_tabla(c))
				for i, valor in enumerate(lista):
					self.tabla.setItem(fila, i + 1, self.item_tabla(valor))
			
def main():
	app = QApplication([])
	ventana = Ventana()
	ventana.show()
	sys.exit(app.exec())

if __name__ == "__main__":
	main()