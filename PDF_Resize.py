import sys
from pypdf import PdfReader, PdfWriter
from PySide6 import QtCore, QtWidgets


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.inputPath = ""

        self.selectButton = QtWidgets.QPushButton("Datei...")
        self.saveButton = QtWidgets.QPushButton("Speichern unter...")
        self.fileName = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.selectButton)
        self.layout.addWidget(self.saveButton)
        self.layout.addWidget(self.fileName)

        self.selectButton.clicked.connect(self.magic)
        self.saveButton.clicked.connect(self.saveUnder)

    @QtCore.Slot()
    def magic(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open File", "", self.tr("PDF Files (*.pdf)")
        )
        filePath = fileName[0]
        self.inputPath = filePath
        self.fileName.setText(filePath)

    @QtCore.Slot()
    def saveUnder(self):
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", "", self.tr("PDF Files (*.pdf)")
        )

        if len(fileName) < 4:
            return

        # Check for file type existance
        if fileName[-4:] != ".pdf":
            fileName += ".pdf"

        if self.inputPath == "":
            return

        resizePDF(self.inputPath, fileName)


def resizePDF(inputFile, outputFile):
    reader = PdfReader(inputFile)
    writer = PdfWriter()

    page = reader.pages[0]
    page.mediabox.lower_right = (
        page.mediabox.right,
        page.mediabox.top / 2,
    )

    page.rotate(90)

    writer.add_page(page)

    with open(outputFile, "wb") as f:
        writer.write(f)


def main():
    # file = sys.argv[1]
    # resizePDF(file)
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
