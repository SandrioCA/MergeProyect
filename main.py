import os
import re
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QFileDialog, QMessageBox
)


def process_file(file_path, file_name, compiled_data):
    with open(file_path, "r", errors="replace") as f:
        for line in f:
            pattern = r"^([0-9A-Za-z]+)\s+(.+?)\s+([A-Z]{3})\s+(\d+)\s+(\d+)\s+(\d+)(?:\s+(999))?\s+(\d{8})$"
            m = re.match(pattern, line.strip())

            if m:
                id_, nombre, cod, c1, c2, c3, c999, fecha = m.groups()
                c999 = c999 or ""

                fields = [id_, nombre, cod, c1, c2, c3, c999, fecha]
                linea_csv = ",".join(fields)
                compiled_data.write(f"{file_name},{linea_csv.rstrip()}\n")


class Ventana(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Merger Python")
        self.setGeometry(300, 300, 550, 200)

        layout = QVBoxLayout()

        # Etiqueta
        label = QLabel("Seleccione carpeta con archivos TXT:")
        label.setStyleSheet("font-size: 20px;")
        layout.addWidget(label)

        # Caja + botón para seleccionar carpeta
        hbox = QHBoxLayout()
        self.entry = QLineEdit()
        hbox.addWidget(self.entry)

        btn_folder = QPushButton("Buscar carpeta")
        btn_folder.clicked.connect(self.seleccionar_carpeta)
        hbox.addWidget(btn_folder)

        layout.addLayout(hbox)

        # Botón procesar
        btn_procesar = QPushButton("Generar CSV")
        btn_procesar.setStyleSheet("background-color: #4CAF50; color: white; font-size: 15px;")
        btn_procesar.clicked.connect(self.procesar)
        layout.addWidget(btn_procesar)

        self.setLayout(layout)

    def seleccionar_carpeta(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta")
        if carpeta:
            self.entry.setText(carpeta)

    def procesar(self):
        directory = self.entry.text().strip()
        if not directory or not os.path.isdir(directory):
            QMessageBox.critical(self, "Error", "Seleccione una carpeta válida.")
            return

        output_file = os.path.join(directory, "compiled_data.csv")

        try:
            with open(output_file, "w") as compiled_data:
                compiled_data.write("Nombre del archivo,Contenido\n")

                for file_name in os.listdir(directory):
                    file_path = os.path.join(directory, file_name)
                    if os.path.isfile(file_path):
                        process_file(file_path, file_name, compiled_data)

            QMessageBox.information(self, "Éxito", f"Archivo creado:\n{output_file}")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec_())