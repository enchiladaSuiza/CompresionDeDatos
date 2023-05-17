import sys, math
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

diccionario = dict()
codigos = dict()
total_caracteres = 0
entropia = 0
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
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Carácter", "Frecuencia", "F. Relativa", "Logaritmo"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setItemDelegateForColumn(1, DelegadoNumerico())
        self.tabla.cellActivated.connect(self.editar_frecuencia)
        self.tabla.cellChanged.connect(self.actualizar_frecuencia)

        self.label_entropia = QLabel("Entropía: ")
        self.label_entropia.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(boton_archivo)
        layout.addWidget(self.textedit)
        layout.addWidget(self.label_total)
        layout.addWidget(self.tabla)
        layout.addWidget(self.label_entropia)

        self.entrada_actualizada()

    def seleccionar_archivo(self):
        nombre_archivo, _ = QFileDialog.getOpenFileName(self, "Seleccione un archivo.", "./")
        if nombre_archivo:
            texto = open(nombre_archivo, "r").read()
            self.textedit.setText(texto)

    def entrada_actualizada(self):
        global total_caracteres
        global entropia
        global codigos
        texto = self.textedit.toPlainText()
        total_caracteres = len(texto)
        self.label_total.setText(f"Total de carácteres: {total_caracteres}")
        actualizar_diccionario(texto)
        self.actualizar_tabla()
        calcular_entropia()
        self.label_entropia.setText(f"Entropía: {entropia}")

    def actualizar_tabla(self):
        global diccionario
        global codigos
        self.tabla.clearContents()
        self.tabla.setRowCount(0)
        for caracter, valores in diccionario.items():
            fila = self.tabla.rowCount()
            self.tabla.insertRow(fila)
            self.tabla.setItem(fila, 0, self.nuevo_item(caracter))
            self.tabla.setItem(fila, 1, self.nuevo_item(str(valores[0]), True))
            self.tabla.setItem(fila, 2, self.nuevo_item(str(valores[1])))
            self.tabla.setItem(fila, 3, self.nuevo_item(str(valores[2])))
    
    def nuevo_item(self, valor, editable=False):
        item = QTableWidgetItem(valor)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        if not editable:    
            item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        return item
    
    def editar_frecuencia(self, fila, columna):
        if columna == 1:
            item = self.tabla.item(fila, 1)
            self.tabla.editItem(item)

    def actualizar_frecuencia(self, fila, columna):
        global frecuencia_editada
        global diccionario
        if frecuencia_editada:
            frecuencia_editada = False
            item_frecuencia = self.tabla.item(fila, 1)
            item_caracter = self.tabla.item(fila, 0)
            frecuencia_nueva = int(item_frecuencia.data(Qt.ItemDataRole.EditRole))
            caracter = item_caracter.data(Qt.ItemDataRole.EditRole)
            frecuencia = diccionario[caracter][0]
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

def actualizar_diccionario(texto):
    diccionario.clear()
    for caracter in texto:
        if diccionario.get(caracter) == None:
            relativa = 1 / total_caracteres
            logaritmo = math.log2(total_caracteres)
            diccionario[caracter] = [1, relativa, logaritmo]
        else:
            frecuencia = diccionario[caracter][0] + 1
            relativa = frecuencia / total_caracteres
            logaritmo = math.log2(total_caracteres / frecuencia)
            diccionario[caracter] = [frecuencia, relativa, logaritmo]

def calcular_entropia():
    global entropia
    entropia = 0
    for valores in diccionario.values():
        entropia += valores[1] * valores[2]

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