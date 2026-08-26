from PyQt6.QtCore import QThread, pyqtSignal
from gurux_dlms.objects import GXDLMSData

from gurux_connect.connect_meter import get_reader, init_connect, close_reader


class DebugWorker(QThread):
    """Рабочий поток для выполнения подключения в фоновом режиме."""

    log_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, port_num: int, interval: int = 300, max_errors: int = 2):
        super().__init__()
        self.port_num = port_num
        self.interval = interval  # интервал в секундах (по умолчанию 5 минут)
        self.max_errors = max_errors
        self._stop_event = False
        self._connection_errors = 0

    def stop(self):
        """Запрос на остановку потока."""
        self._stop_event = True

    def run(self):
        while not self._stop_event:
            max_attempts = self.max_errors
            serial_number_list = [5654, 1, 2]

            for serial_num in serial_number_list:
                success = False
                attempt = 0
                while not self._stop_event and attempt < max_attempts:
                    reader = None
                    attempt += 1
                    try:
                        reader, settings = get_reader(
                            com=self.port_num,
                            password="1234567898765432",
                            serial_number=serial_num,
                            authentication="High",
                            clientAddress=48
                        )

                        init_connect(reader, settings)
                        self.log_signal.emit("Соединение успешно установлено")
                        serial_number = reader.read(GXDLMSData("0.0.96.1.0.255"), 2).decode("utf-8")
                        self.log_signal.emit(f"Считан серийный номер {serial_number}")
                        if str(serial_num) != str(serial_number)[-4:].lstrip("0"):
                            self.log_signal.emit(f"Серийный номер {serial_num} не соответствует"
                                                 f" {str(serial_number)[-4:].lstrip("0")}!")
                        self._connection_errors = 0  # Сброс счётчика при успешном подключении
                        self.log_signal.emit("Отправить сигнал на овен - ВКЛЮЧИТЬ лампочку.\n")
                        success = True
                        break

                    except Exception as e:
                        self.error_signal.emit(f"Ошибка подключения (попытка {attempt}/{max_attempts}): {e}")

                    finally:
                        if reader is not None:
                            close_reader(reader)

                    # Ждать 3 секунды перед следующей попыткой
                    if not self._stop_event and attempt < max_attempts:
                        self.sleep(3)

                if not self._stop_event and not success:
                    self.log_signal.emit(f"Отправить сигнал на овен - ВЫКЛЮЧИТЬ лампочку для счетчика №{serial_num}.\n")

            if not self._stop_event:
                self.sleep(self.interval)

        self.finished_signal.emit()