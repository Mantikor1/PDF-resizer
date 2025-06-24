import os
import subprocess
import sys
from pypdf import PdfReader, PdfWriter
from PySide6 import QtCore, QtWidgets
from PySide6.QtPrintSupport import QPrinter, QPrintPreviewDialog, QPrintDialog


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.inputPath = ""
        self.outputPath = ""

        self.selectButton = QtWidgets.QPushButton("Datei...")
        self.saveButton = QtWidgets.QPushButton("Speichern unter...")
        self.printButton = QtWidgets.QPushButton("Drucken")
        self.fileName = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.selectButton)
        self.layout.addWidget(self.saveButton)
        self.layout.addWidget(self.printButton)
        self.layout.addWidget(self.fileName)

        self.selectButton.clicked.connect(self.selectInputFile)
        self.saveButton.clicked.connect(self.saveUnder)
        self.printButton.clicked.connect(self.print)

    @QtCore.Slot()
    def selectInputFile(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open File", "", self.tr("PDF Files (*.pdf)")
        )
        filePath = fileName[0]
        self.inputPath = filePath
        self.fileName.setText(filePath)

    def selectOutputPath(self):
        outputPath, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", "", self.tr("PDF Files (*.pdf)")
        )

        if len(outputPath) < 4:
            print("Path is too short")
            return

        # Check for file type existance
        if outputPath[-4:] != ".pdf":
            outputPath += ".pdf"

        return outputPath

    @QtCore.Slot()
    def saveUnder(self):

        self.outputPath = self.selectOutputPath()

        if self.inputPath == "":
            print("No file selected")
            return

        resizePDF(self.inputPath, self.outputPath)

    def print(self):

        if sys.platform == "win32":
            os.startfile(self.outputPath)
        elif sys.platform == "darwin":
            subprocess.run(["open", "-a", "Preview", self.outputPath])
        else:
            subprocess.run(["lpr", self.outputPath])


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
