import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QMessageBox, QDesktopWidget
)
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QSize


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение с полупрозрачным фоном")
        self.setGeometry(100, 100, 600, 400)

        # Центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Основной layout
        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)

        # Надпись
        self.label = QLabel("Надпись")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; color: white; background: transparent;")
        main_layout.addWidget(self.label)

        # Layout для кнопок
        buttons_layout = QHBoxLayout()
        main_layout.addLayout(buttons_layout)

        # Кнопка 1
        self.button1 = QPushButton("Кнопка1")
        self.button1.clicked.connect(self.change_label_text)
        buttons_layout.addWidget(self.button1)

        # Кнопка 2
        self.button2 = QPushButton("Кнопка2")
        self.button2.clicked.connect(self.load_transparent_image)
        buttons_layout.addWidget(self.button2)

        # Хранение изображения
        self.background_pixmap = None

        # Устанавливаем прозрачный фон
        self.central_widget.setAttribute(Qt.WA_TranslucentBackground)
        self.central_widget.setAutoFillBackground(False)

        # Переопределяем paintEvent для рисования фона
        self.central_widget.paintEvent = self.paint_background

    def paint_background(self, event):
        """Рисует полупрозрачный фон поверх всего окна"""
        if self.background_pixmap:
            painter = QPainter(self.central_widget)
            painter.setRenderHint(QPainter.Antialiasing)

            # Масштабируем изображение под размер центрального виджета
            scaled_pixmap = self.background_pixmap.scaled(
                self.central_widget.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )

            # Рисуем с полупрозрачностью
            painter.setOpacity(0.7)
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()
        else:
            # Стандартный фон, если нет изображения
            painter = QPainter(self.central_widget)
            painter.fillRect(self.central_widget.rect(), QColor(240, 240, 240))
            painter.end()

    def change_label_text(self):
        """Изменяет текст надписи при нажатии кнопки 1"""
        current_text = self.label.text()
        if current_text == "Надпись":
            self.label.setText("Текст изменён!")
        else:
            self.label.setText("Надпись")

    def load_transparent_image(self):
        """Загружает PNG-изображение и подгоняет окно под его размер или максимизирует"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите PNG файл",
            "",
            "PNG Files (*.png);;All Files (*)"
        )

        if not file_path:
            return

        try:
            pixmap = QPixmap(file_path)
            if pixmap.isNull():
                QMessageBox.critical(self, "Ошибка", "Не удалось загрузить изображение.")
                return

            # Сохраняем изображение
            self.background_pixmap = pixmap

            # Получаем размер изображения
            img_width = pixmap.width()
            img_height = pixmap.height()

            # Получаем размер экрана
            screen = QDesktopWidget().screenGeometry()
            screen_width = screen.width()
            screen_height = screen.height()

            # Если изображение больше экрана — максимизируем окно
            if img_width > screen_width or img_height > screen_height:
                self.showMaximized()
            else:
                # Иначе — устанавливаем точный размер окна под изображение
                self.resize(img_width, img_height)

            # Обновляем фон
            self.central_widget.update()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Убираем стандартный фон окна
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())