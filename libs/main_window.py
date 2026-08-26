from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        # Загружаем дизайн прямо из файла
        loadUi("libs/maket_training_stand.ui", self)