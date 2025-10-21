from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl
import json


class CurrencyConverterWidget(QWidget):
    def __init__(self, usd_signals, eur_signals, rub_signals, common_signals):
        super().__init__()
        self.usd_signals = usd_signals
        self.eur_signals = eur_signals
        self.rub_signals = rub_signals
        self.common_signals = common_signals
        self.rates = {}
        self.updating = False
        self.network_manager = QNetworkAccessManager()
        self.initUI()
        self.setupSignals()
        self.updateRatesFromAPI()  # Автоматическая загрузка при запуске

    def initUI(self):
        self.setWindowTitle('Конвертер валют')

        layout = QVBoxLayout()

        self.usd_label = QLabel('Доллары (USD):')
        self.usd_input = QLineEdit()

        self.eur_label = QLabel('Евро (EUR):')
        self.eur_input = QLineEdit()

        self.rub_label = QLabel('Рубли (RUB):')
        self.rub_input = QLineEdit()

        self.clear_button = QPushButton('Очистить все поля')

        layout.addWidget(self.usd_label)
        layout.addWidget(self.usd_input)
        layout.addWidget(self.eur_label)
        layout.addWidget(self.eur_input)
        layout.addWidget(self.rub_label)
        layout.addWidget(self.rub_input)
        layout.addWidget(self.clear_button)

        self.setLayout(layout)

    def setupSignals(self):
        self.usd_signals.usd_changed.connect(self.updateEurRub)
        self.eur_signals.eur_changed.connect(self.updateUsdRub)
        self.rub_signals.rub_changed.connect(self.updateUsdEur)
        self.common_signals.clear_all.connect(self.onClearAll)
        self.common_signals.rates_updated.connect(self.onRatesUpdated)

        self.usd_input.textChanged.connect(self.onUsdChanged)
        self.eur_input.textChanged.connect(self.onEurChanged)
        self.rub_input.textChanged.connect(self.onRubChanged)

        self.clear_button.clicked.connect(self.onClearClicked)

    def updateRatesFromAPI(self):
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        request = QNetworkRequest(QUrl(url))
        self.network_manager.get(request)
        self.network_manager.finished.connect(self.onAPIResponse)

    def onAPIResponse(self, reply):
        error = reply.error()
        if error == reply.NoError:
            data = json.loads(reply.readAll().data())
            rates = data.get('rates', {})

            # База — USD, курсы к нему
            usd_to_eur = rates.get('EUR', 0)
            usd_to_rub = rates.get('RUB', 0)

            # Обратные курсы
            eur_to_usd = 1 / usd_to_eur if usd_to_eur else 0
            rub_to_usd = 1 / usd_to_rub if usd_to_rub else 0

            # Курсы "евро к рублю" и "рубль к евро"
            eur_to_rub = usd_to_rub / usd_to_eur if usd_to_eur else 0
            rub_to_eur = 1 / eur_to_rub if eur_to_rub else 0

            self.rates = {
                'usd_to_eur': usd_to_eur,
                'usd_to_rub': usd_to_rub,
                'eur_to_usd': eur_to_usd,
                'eur_to_rub': eur_to_rub,
                'rub_to_usd': rub_to_usd,
                'rub_to_eur': rub_to_eur
            }
            self.common_signals.rates_updated.emit(self.rates)
        else:
            print("Ошибка при загрузке курсов:", reply.errorString())

    def onRatesUpdated(self, new_rates):
        self.rates = new_rates

    def onUsdChanged(self, text):
        if self.updating or not self.rates:
            return
        try:
            value = float(text)
        except ValueError:
            return
        self.usd_signals.usd_changed.emit(value)

    def onEurChanged(self, text):
        if self.updating or not self.rates:
            return
        try:
            value = float(text)
        except ValueError:
            return
        self.eur_signals.eur_changed.emit(value)

    def onRubChanged(self, text):
        if self.updating or not self.rates:
            return
        try:
            value = float(text)
        except ValueError:
            return
        self.rub_signals.rub_changed.emit(value)

    def updateEurRub(self, usd_value):
        if self.updating or not self.rates:
            return
        self.updating = True
        eur = usd_value * self.rates['usd_to_eur']
        rub = usd_value * self.rates['usd_to_rub']
        self.eur_input.setText(f"{eur:.2f}")
        self.rub_input.setText(f"{rub:.2f}")
        self.updating = False

    def updateUsdRub(self, eur_value):
        if self.updating or not self.rates:
            return
        self.updating = True
        usd = eur_value * self.rates['eur_to_usd']
        rub = eur_value * self.rates['eur_to_rub']
        self.usd_input.setText(f"{usd:.2f}")
        self.rub_input.setText(f"{rub:.2f}")
        self.updating = False

    def updateUsdEur(self, rub_value):
        if self.updating or not self.rates:
            return
        self.updating = True
        usd = rub_value * self.rates['rub_to_usd']
        eur = rub_value * self.rates['rub_to_eur']
        self.usd_input.setText(f"{usd:.2f}")
        self.eur_input.setText(f"{eur:.2f}")
        self.updating = False

    def onClearAll(self):
        self.updating = True
        self.usd_input.clear()
        self.eur_input.clear()
        self.rub_input.clear()
        self.updating = False

    def onClearClicked(self):
        self.common_signals.clear_all.emit()