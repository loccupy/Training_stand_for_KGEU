from gurux_connect.GXDLMSReader import GXDLMSReader
from gurux_connect.GXSettings import GXSettings


def get_reader(com, password, serial_number, authentication, clientAddress):
    settings = GXSettings()
    settings.getParameters("COM", f"COM{com}", password=password,
                           authentication=authentication, serverAddress=serial_number + 16,
                           logicalAddress=1, clientAddress=clientAddress, baudRate=9600)
    reader = GXDLMSReader(settings.client, settings.media,
                          settings.trace, settings.invocationCounter)

    return reader, settings


def init_connect(reader, settings):
    try:
        if not settings.media.isOpen():
            settings.media.open()

        reader.initializeConnection()
    except Exception as e:
        settings.media.close()
        print(f"Ошибка при открытии соединения: {e}")
        raise


def close_reader(reader):
    try:
        reader.close()
    except Exception as e:
        # print(f"Ошибка при закрытии соединения: {e}")
        raise