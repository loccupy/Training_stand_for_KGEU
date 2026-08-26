from PyQt6.QtWidgets import QWidget, QPushButton, QTextEdit, QComboBox, QStyle
from PyQt6.uic import loadUi
from serial.tools import list_ports as serial_list_ports

dark_style = """
    QWidget {
        background-color: #282828;
        color: #dddddd;
        border-radius: 8px;
    }
    QPushButton {
        background-color: #3c3c44;
        color: #dddddd;
        padding: 6px;
        border: 1px solid #444;
        border-radius: 8px;
    }
    QPushButton:hover {
        background-color: #484855;
    }
    QComboBox {
        background-color: #333;
        color: #ddd;
        border: 1px solid #555;
        border-radius: 8px;
        padding-left: 20px;
    }
    QComboBox::drop-down {
        width: 20px;
        border-left: 1px solid #555;
    }
    QComboBox QAbstractItemView {
        background-color: #333;
        border: 1px solid #555;
        border-radius: 8px; /* Скругляем углы списка */
        padding-left: 30px;
    }
    QTextEdit {
        background-color: #1e1e1e;       /* Тёмно-серый фон */
        color: #e0e0e0;                  /* Светлый текст */
        border: 1px solid #333;          /* Тонкая рамка */
        border-radius: 8px;              /* Скругление углов */
        padding: 8px;                    /* Отступы внутри */
    }
    QTextEdit:focus {
        border: 1px solid #5a7fa5;       /* Цвет рамки при фокусе */
    }
    QScrollBar:vertical {
        background: #333;
        width: 12px;
    }
    QScrollBar::handle:vertical {
        background: #555;
        min-height: 20px;
    }
    """


def get_available_ports() -> list:
    ports = ["Не выбран"]
    try:
        available = serial_list_ports.comports()
        for port in available:
            # Форматируем красиво: "COM3 (USB Serial Device)"
            ports.append(f"{port.device}")
    except Exception as e:
        print(f"Ошибка поиска портов: {e}")
        ports.extend(["COM1", "COM2", "COM3", "COM4"])
    return ports


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        # Загружаем дизайн прямо из файла
        loadUi("libs/maket_training_stand.ui", self)
        self.init_ui()

    def init_ui(self):
        start_button = self.findChild(QPushButton, "start_button")
        start_button.clicked.connect(self.debug_meth)

        field_log = self.findChild(QTextEdit, "logs")
        field_log.setReadOnly(True)

        com_drop_down = self.findChild(QComboBox, "com_drop_down")
        com_drop_down.addItems(get_available_ports())

        com_refresh = self.findChild(QPushButton, "com_refresh")
        com_refresh.setText("↻")
        com_refresh.clicked.connect(self.on_refresh_port_combo)

        self.setStyleSheet(dark_style)

    def on_refresh_port_combo(self):
        """Обновить список портов комбо-бокса."""
        self.com_drop_down.clear()
        self.com_drop_down.addItems(get_available_ports())
        self.com_drop_down.setCurrentIndex(0)

    def debug_meth(self):
        print("debug")