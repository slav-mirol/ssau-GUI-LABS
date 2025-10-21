from PyQt5.QtCore import QObject, pyqtSignal

class EurSignals(QObject):
    eur_changed = pyqtSignal(float)