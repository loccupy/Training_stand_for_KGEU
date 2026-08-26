from PyQt6.QtWidgets import QWidget, QPushButton, QTextEdit, QComboBox
from PyQt6.uic import loadUi
from serial.tools import list_ports as serial_list_ports

from libs.running import DebugWorker

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
            ports.append(f"{port.device}")
    except Exception as e:
        print(f"Ошибка поиска портов: {e}")
        ports.extend(["COM1", "COM2", "COM3", "COM4"])
    return ports


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        loadUi("libs/maket_training_stand.ui", self)

        self.start_button = None
        self.field_log = None
        self.com_drop_down = None
        self.com_refresh = None
        self.debug_thread = None
        self.init_ui()

    def init_ui(self):
        self.start_button = self.findChild(QPushButton, "start_button")
        self.start_button.clicked.connect(self.on_start_clicked)

        self.field_log = self.findChild(QTextEdit, "logs")
        self.field_log.setReadOnly(True)

        self.com_drop_down = self.findChild(QComboBox, "com_drop_down")
        self.com_drop_down.addItems(get_available_ports())

        self.com_refresh = self.findChild(QPushButton, "com_refresh")
        self.com_refresh.setText("↻")
        self.com_refresh.clicked.connect(self.on_refresh_port_combo)

        self.setStyleSheet(dark_style)

    def on_refresh_port_combo(self):
        """Обновить список портов комбо-бокса."""
        self.com_drop_down.clear()
        self.com_drop_down.addItems(get_available_ports())
        self.com_drop_down.setCurrentIndex(0)
        self.log("Обновлен список портов")

    def log(self, message):
        """Добавляет сообщение в поле логов."""
        from datetime import datetime
        field_log = self.findChild(QTextEdit, "logs")
        timestamp = datetime.now().strftime("%H:%M:%S")
        field_log.append(f"[{timestamp}] {message}")

    def on_start_clicked(self):
        """Обработчик нажатия кнопки запуска/остановки."""
        if self.debug_thread is not None and self.debug_thread.isRunning():
            self.log("Остановка потока...")
            self.debug_thread.stop()
            self.debug_thread.wait()
            self.debug_thread = None
            self.start_button.setEnabled(True)
            self.com_drop_down.setEnabled(True)
            self.com_refresh.setEnabled(True)
            return

        selected = self.com_drop_down.currentText()
        if selected == "Не выбран" or not selected:
            self.log("Ошибка: не выбран COM-порт")
            return

        port_num = selected.replace("COM", "")
        if not port_num.isdigit():
            self.log(f"Ошибка: некорректный порт '{selected}'")
            return

        self.start_button.setEnabled(False)
        self.com_drop_down.setEnabled(False)
        self.com_refresh.setEnabled(False)

        port_num = int(port_num)

        self.debug_thread = DebugWorker(port_num, interval=10)
        self.debug_thread.log_signal.connect(self.log)
        self.debug_thread.error_signal.connect(self.log)
        self.debug_thread.finished_signal.connect(self.on_debug_finished)
        self.debug_thread.start()

    def on_debug_finished(self):
        """Обработчик завершения фонового потока."""
        self.debug_thread = None
        self.start_button.setEnabled(True)
        self.com_drop_down.setEnabled(True)
        self.com_refresh.setEnabled(True)


        