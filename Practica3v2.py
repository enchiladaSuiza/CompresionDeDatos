import sys, math, collections, huffman
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QLabel,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QStyledItemDelegate,
    QLineEdit,
)
from PyQt6.QtGui import (
    QKeySequence,
    QShortcut,
    QRegularExpressionValidator,
)
from PyQt6.QtCore import (
    Qt,
    QRegularExpression,
    qInstallMessageHandler
)

frecuencias = dict()
codigos = dict()
probabilidades = dict()
logaritmos = dict()
entropia = 0
longitud_media = 0

frecuencia_editada = False

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Práctica 3 - Entropía de la información")
        self.setMinimumWidth(400)

        contenedor = QWidget(self)
        layout = QVBoxLayout(contenedor)
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)

        shortcut_cerrar = QShortcut(QKeySequence('Ctrl+Q'), self)
        shortcut_cerrar.activated.connect(QApplication.instance().quit)

        boton_archivo = QPushButton("Seleccionar un archivo...")
        boton_archivo.clicked.connect(self.seleccionar_archivo)

        self.textedit = QTextEdit()
        self.textedit.setPlaceholderText("Escriba aquí la cadena de entrada o seleccione un archivo.")
        self.textedit.textChanged.connect(self.entrada_actualizada)

        self.label_total = QLabel("Total de carácteres: ")
        self.label_total.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tabla = QTableWidget(self)
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Carácter", "Código", "Frecuencia", "p(a)", "log2(1/p(a)"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setItemDelegateForColumn(2, DelegadoNumerico())
        self.tabla.cellActivated.connect(self.editar_frecuencia)
        self.tabla.cellChanged.connect(self.actualizar_frecuencia)

        self.label_entropia = QLabel("Entropía: ")
        self.label_entropia.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_longitud = QLabel("Longitud Media: ")
        self.label_longitud.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(boton_archivo)
        layout.addWidget(self.textedit)
        layout.addWidget(self.label_total)
        layout.addWidget(self.tabla)
        layout.addWidget(self.label_entropia)
        layout.addWidget(self.label_longitud)

    def seleccionar_archivo(self):
        nombre_archivo, _ = QFileDialog.getOpenFileName(self, "Seleccione un archivo.", "./")
        if nombre_archivo:
            texto = open(nombre_archivo, "r").read()
            self.textedit.setText(texto)

    def entrada_actualizada(self):
        global entropia, longitud_media, total_caracteres
        texto = self.textedit.toPlainText()
        total_caracteres = len(texto)
        self.label_total.setText(f"Total de carácteres: {total_caracteres}")
        calcular(texto)
        self.actualizar_tabla()
        self.label_entropia.setText(f"Entropía: {entropia}")
        self.label_longitud.setText(f"Longitud Media: {longitud_media}")
    
    def actualizar_tabla(self):
        global frecuencias, codigos, probabilidades, logaritmos
        self.tabla.clearContents()
        self.tabla.setRowCount(len(frecuencias))
        for i, caracter in enumerate(frecuencias.keys()):
            self.tabla.setItem(i, 0, self.nuevo_item(caracter))
            self.tabla.setItem(i, 1, self.nuevo_item(codigos.get(caracter)))
            self.tabla.setItem(i, 2, self.nuevo_item(str(frecuencias.get(caracter)), True))
            self.tabla.setItem(i, 3, self.nuevo_item(str(probabilidades.get(caracter))))
            self.tabla.setItem(i, 4, self.nuevo_item(str(logaritmos.get(caracter))))

    def nuevo_item(self, valor, editable=False):
        item = QTableWidgetItem(valor)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        if not editable:    
            item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        return item

    def editar_frecuencia(self, fila, columna):
        if columna == 2:
            item = self.tabla.item(fila, 2)
            self.tabla.editItem(item)

    def actualizar_frecuencia(self, fila, columna):
        global frecuencia_editada, frecuencias
        if not frecuencia_editada:
            return
        frecuencia_editada = False
        item_caracter = self.tabla.item(fila, 0)
        item_frecuencia = self.tabla.item(fila, 2)
        frecuencia_nueva = int(item_frecuencia.data(Qt.ItemDataRole.EditRole))
        caracter = item_caracter.data(Qt.ItemDataRole.EditRole)
        frecuencia = frecuencias.get(caracter)
        if frecuencia_nueva == frecuencia:
            return
        diferencia = abs(frecuencia - frecuencia_nueva)
        texto = self.textedit.toPlainText()
        if frecuencia_nueva < frecuencia:
            nuevo_texto = texto.replace(caracter, "", diferencia)
        else:
            nuevo_texto = texto + (caracter * diferencia)
        self.textedit.setText(nuevo_texto)

class DelegadoNumerico(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            regex = QRegularExpression("[0-9]+")
            validador = QRegularExpressionValidator(regex)
            editor.setValidator(validador)
        return editor
    
    def setModelData(self, editor, model, index):
        global frecuencia_editada
        frecuencia_editada = True
        super().setModelData(editor, model, index)

def calcular(texto):
    global frecuencias, codigos, probabilidades, logaritmos, entropia, longitud_media
    if not texto:
        return
    tuplas = collections.Counter(texto).items()
    codigos = huffman.codebook(tuplas)
    frecuencias = dict(tuplas)
    probabilidades = dict(map(lambda x: (x[0], x[1] / total_caracteres), frecuencias.items()))
    logaritmos = dict(map(lambda x: (x[0], math.log2(total_caracteres / x[1])), frecuencias.items()))

    entropia = 0
    longitud_media = 0
    for caracter in frecuencias.keys():
        entropia += probabilidades[caracter] * logaritmos[caracter]
        longitud_media += probabilidades[caracter] * len(codigos[caracter])

def handler(tipo, contexto, cadena):
    pass

def main():
    qInstallMessageHandler(handler)
    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()