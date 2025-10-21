from PyQt5.QtCore import QObject, pyqtSignal

class UsdSignals(QObject):
    usd_changed = pyqtSignal(float)