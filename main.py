from PyQt6.QtWidgets import QApplication

from libs.main_window import MainWindow

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
