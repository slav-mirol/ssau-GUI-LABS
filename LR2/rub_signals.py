from PyQt5.QtCore import QObject, pyqtSignal

class RubSignals(QObject):
    rub_changed = pyqtSignal(float)