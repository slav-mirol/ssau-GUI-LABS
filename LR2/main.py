import sys
from PyQt5.QtWidgets import QApplication

# Импортируем все сигналы в main.py
from usd_signals import UsdSignals
from eur_signals import EurSignals
from rub_signals import RubSignals
from common_signals import CommonSignals
from currency_converter import CurrencyConverterWidget


def main():
    app = QApplication(sys.argv)

    # Создаём экземпляры сигналов
    usd_signals = UsdSignals()
    eur_signals = EurSignals()
    rub_signals = RubSignals()
    common_signals = CommonSignals()

    # Создаём виджет и передаём ему все сигналы
    converter = CurrencyConverterWidget(usd_signals, eur_signals, rub_signals, common_signals)

    converter.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()