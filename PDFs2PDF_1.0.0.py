from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QFileDialog, \
    QLabel, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyPDF2 import PdfMerger
import ntpath
import sys
import os


class PDFMerger:
    def __init__(self):
        self.file_paths = []
        self.merger = PdfMerger()

    def add_file(self, file_path):
        self.file_paths.append(file_path)
        self.merger.append(file_path)

    def remove_file(self, index):
        self.file_paths.pop(index)

    def move_file(self, index, new_index):
        self.file_paths.insert(new_index, self.file_paths.pop(index))

    def merge_files(self, output_path):
        if output_path:
            self.merger.write(output_path)
            self.merger.close()


class PDFMergerApp(QWidget):
    def __init__(self):
        super(PDFMergerApp, self).__init__()
        self.pdf_merger = PDFMerger()
        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("PDF Merger")
        self.setGeometry(500, 400, 400, 400)

        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Buttons
        self.init_buttons(layout)

        # List Widget
        self.listwidget = QListWidget()
        layout.addWidget(self.listwidget)

        # Status Label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

    def init_buttons(self, layout):
        select_button = QPushButton("Vali failid")
        select_button.clicked.connect(self.select_files)
        layout.addWidget(select_button)

        up_button = QPushButton("↑ Üles")
        up_button.clicked.connect(self.move_up)
        layout.addWidget(up_button)

        down_button = QPushButton("↓ Alla")
        down_button.clicked.connect(self.move_down)
        layout.addWidget(down_button)

        remove_button = QPushButton("X Eemalda")
        remove_button.clicked.connect(self.remove_file)
        layout.addWidget(remove_button)

        merge_button = QPushButton("Ühenda failid")
        merge_button.clicked.connect(self.merge_files)
        layout.addWidget(merge_button)

    def select_files(self):
        default_location = os.path.join(os.path.expanduser("~"), "Desktop")
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Vali failid", default_location, "PDF Files (*.pdf)")
        for file_path in file_paths:
            self.pdf_merger.add_file(file_path)
        self.refresh_listbox()

    def move_up(self):
        current_row = self.listwidget.currentRow()
        if current_row >= 1:
            self.pdf_merger.move_file(current_row, current_row - 1)
            self.refresh_listbox()

    def move_down(self):
        current_row = self.listwidget.currentRow()
        if current_row < self.listwidget.count() - 1:
            self.pdf_merger.move_file(current_row, current_row + 1)
            self.refresh_listbox()

    def remove_file(self):
        current_row = self.listwidget.currentRow()
        if self.listwidget.count() > 0 and current_row != -1:
            self.pdf_merger.remove_file(current_row)
            self.refresh_listbox()

    def merge_files(self):
        # Check if no files or only one file is selected
        if len(self.pdf_merger.file_paths) == 0:
            reply = QMessageBox.question(self, 'Kinnitus',
                                         "Olete kindel, et soovite salvestada tühja faili?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.No:
                return
        elif len(self.pdf_merger.file_paths) == 1:
            reply = QMessageBox.question(self, 'Kinnitus',
                                         "Olete kindel, et soovite salvestada ainult ühte PDF faili?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.No:
                return

        default_location = os.path.join(os.path.expanduser("~"), "Desktop")
        default_file_name = "merged.pdf"
        output_path, _ = QFileDialog.getSaveFileName(self, "Salvesta fail",
                                                     os.path.join(default_location, default_file_name),
                                                     "PDF Files (*.pdf)")

        if output_path:
            self.pdf_merger.merge_files(output_path)
            self.status_label.setText("PDF-id on ühendatud ja salvestatud!")
            self.status_label.setStyleSheet("color: green; font-weight: bold")
            QTimer.singleShot(3000, self.status_label.clear)
        else:
            self.status_label.setText("Ühendamine tühistati")
            self.status_label.setStyleSheet("color: red")
            QTimer.singleShot(3000, self.status_label.clear)

    def refresh_listbox(self):
        self.listwidget.clear()
        for file_path in self.pdf_merger.file_paths:
            file_name = ntpath.basename(file_path)
            self.listwidget.addItem(QListWidgetItem(file_name))


def main():
    App = QApplication(sys.argv)
    window = PDFMergerApp()
    window.show()
    sys.exit(App.exec())


if __name__ == '__main__':
    main()
