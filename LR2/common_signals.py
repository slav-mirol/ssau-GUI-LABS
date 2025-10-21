from PyQt5.QtCore import QObject, pyqtSignal

class CommonSignals(QObject):
    clear_all = pyqtSignal()
    rates_updated = pyqtSignal(dict)