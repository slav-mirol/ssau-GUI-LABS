import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QTabWidget, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QTableWidget,
    QTableWidgetItem, QMessageBox, QFileDialog
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt SQL App")
        self.setGeometry(100, 100, 800, 600)

        # Инициализация базы данных
        self.db = None
        self.current_table = None  # Текущая таблица для запросов

        # Центральный виджет и макет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Меню
        menu_bar = self.menuBar()
        db_menu = menu_bar.addMenu("Menu")

        set_conn_action = QAction("Set connection", self)
        set_conn_action.triggered.connect(self.set_connection)
        db_menu.addAction(set_conn_action)

        close_conn_action = QAction("Close connection", self)
        close_conn_action.triggered.connect(self.close_connection)
        db_menu.addAction(close_conn_action)

        # Виджет вкладок
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Создаем вкладки
        self.create_tabs()

        # Панель управления (кнопки и комбобокс)
        control_layout = QHBoxLayout()
        self.b1_btn = QPushButton("b1 'SELECT Column'")
        self.b1_btn.clicked.connect(self.execute_b1_query)
        control_layout.addWidget(self.b1_btn)

        self.columns_combo = QComboBox()
        self.columns_combo.addItem("Выберите колонку...")
        self.columns_combo.currentIndexChanged.connect(self.on_column_selected)
        control_layout.addWidget(self.columns_combo)

        self.b2_btn = QPushButton("b2 'Query2'")
        self.b2_btn.clicked.connect(self.execute_b2_query)
        control_layout.addWidget(self.b2_btn)

        self.b3_btn = QPushButton("b3 'Query3'")
        self.b3_btn.clicked.connect(self.execute_b3_query)
        control_layout.addWidget(self.b3_btn)

        main_layout.addLayout(control_layout)

        # Устанавливаем начальную вкладку (Tab1) пустой
        self.setup_tab1()

    def create_tabs(self):
        """Создание 5 вкладок"""
        self.tabs = []
        for i in range(1, 6):
            tab = QWidget()
            layout = QVBoxLayout(tab)
            table = QTableWidget()
            table.setColumnCount(0)
            table.setRowCount(0)
            layout.addWidget(table)
            self.tabs.append(table)
            self.tab_widget.addTab(tab, f"Tab{i}")

    def setup_tab1(self):
        """Загрузка данных в Tab1 по умолчанию"""
        if not self.db or not self.db.isOpen():
            return
        query = QSqlQuery("SELECT * FROM sqlite_master")
        self.display_query_results(query, self.tabs[0])

    def set_connection(self):
        """Установить соединение с БД"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть базу данных", "", "SQLite Files (*.db *.sqlite)"
        )
        if not file_path:
            return

        # Закрываем предыдущее соединение
        if self.db and self.db.isOpen():
            self.db.close()

        # Подключение к новой БД
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(file_path)
        if not self.db.open():
            QMessageBox.critical(self, "Ошибка", f"Не удалось подключиться: {self.db.lastError().text()}")
            self.db = None
            return

        QMessageBox.information(self, "Успех", "Подключение установлено!")
        self.setup_tab1()
        self.load_columns_list()

    def close_connection(self):
        """Закрыть соединение"""
        if self.db and self.db.isOpen():
            self.db.close()
            self.db = None
            QMessageBox.information(self, "Информация", "Соединение закрыто.")
            # Очистка всех таблиц
            for tab in self.tabs:
                tab.setRowCount(0)
                tab.setColumnCount(0)
            self.columns_combo.clear()
            self.columns_combo.addItem("Выберите колонку...")

    def load_columns_list(self):
        """Загружает список колонок из первой таблицы для комбобокса"""
        if not self.db or not self.db.isOpen():
            return

        query = QSqlQuery("SELECT name FROM sqlite_master WHERE type='table'")
        tables = []
        while query.next():
            tables.append(query.value(0))

        if tables:
            self.current_table = tables[0]
            query = QSqlQuery(f"PRAGMA table_info({self.current_table})")
            columns = []
            while query.next():
                col_name = query.value(1)  # имя столбца
                if col_name:  # Проверяем, что имя не пустое
                    columns.append(col_name)

            self.columns_combo.clear()
            self.columns_combo.addItem("Выберите колонку...")
            self.columns_combo.addItems(columns)

    def execute_b1_query(self):
        """Выполнить запрос SELECT name FROM sqlite_master -> Tab2"""
        if not self.db or not self.db.isOpen():
            QMessageBox.warning(self, "Предупреждение", "Сначала установите соединение!")
            return

        query = QSqlQuery("SELECT name FROM sqlite_master")
        self.display_query_results(query, self.tabs[1])  # Tab2

    def on_column_selected(self):
        """При выборе колонки в комбобоксе — выполнить запрос для неё -> Tab3"""
        selected_col = self.columns_combo.currentText()
        if selected_col == "Выберите колонку..." or not self.db or not self.db.isOpen() or not selected_col.strip():
            return

        if not hasattr(self, 'current_table') or not self.current_table:
            QMessageBox.warning(self, "Предупреждение", "Не выбрана таблица для запроса.")
            return

        query_str = f"SELECT {selected_col} FROM {self.current_table} LIMIT 10"
        query = QSqlQuery(query_str)
        self.display_query_results(query, self.tabs[2])  # Tab3

    def execute_b2_query(self):
        """Запрос для b2 -> Tab4"""
        if not self.db or not self.db.isOpen():
            QMessageBox.warning(self, "Предупреждение", "Сначала установите соединение!")
            return

        query = QSqlQuery("SELECT * FROM sqlite_master WHERE type='table' LIMIT 5")
        self.display_query_results(query, self.tabs[3])  # Tab4

    def execute_b3_query(self):
        """Запрос для b3 -> Tab5"""
        if not self.db or not self.db.isOpen():
            QMessageBox.warning(self, "Предупреждение", "Сначала установите соединение!")
            return

        query = QSqlQuery("SELECT sql FROM sqlite_master WHERE type='table' LIMIT 3")
        self.display_query_results(query, self.tabs[4])  # Tab5

    def display_query_results(self, query, table_widget):
        """Отображает результаты запроса в указанной таблице (с отладкой)"""
        print(f"[DEBUG] Запрос: {query.lastQuery()}")

        if not query.exec_():
            error_msg = query.lastError().text()
            QMessageBox.critical(self, "Ошибка выполнения запроса", f"Не удалось выполнить запрос:\n{error_msg}")
            print(f"[ERROR] Запрос не выполнился: {error_msg}")
            return

        # Проверяем, есть ли столбцы
        record = query.record()
        col_count = record.count()
        print(f"[DEBUG] Количество столбцов: {col_count}")

        if col_count == 0:
            QMessageBox.warning(self, "Предупреждение", "Запрос не вернул столбцов.")
            table_widget.setColumnCount(0)
            table_widget.setRowCount(0)
            return

        # Получаем названия столбцов
        headers = []
        for i in range(col_count):
            field_name = record.fieldName(i)
            if field_name is None or field_name == "":
                field_name = f"Column_{i + 1}"
            headers.append(field_name)
            print(f"[DEBUG] Столбец {i}: {field_name}")

        # Устанавливаем заголовки
        table_widget.setColumnCount(col_count)
        table_widget.setHorizontalHeaderLabels(headers)

        # Очищаем таблицу
        table_widget.setRowCount(0)

        # Считаем строки
        row_index = 0
        while query.next():
            print(f"[DEBUG] Обработка строки {row_index + 1}")
            table_widget.insertRow(row_index)
            for col in range(col_count):
                value = query.value(col)
                if value is None:
                    value = "NULL"
                else:
                    value = str(value)
                item = QTableWidgetItem(value)
                table_widget.setItem(row_index, col, item)
            row_index += 1

        # Если данных нет — показываем сообщение
        if row_index == 0:
            print("[DEBUG] Нет данных в результате")
            table_widget.setRowCount(1)
            item = QTableWidgetItem("Нет данных")
            item.setTextAlignment(Qt.AlignCenter)
            table_widget.setItem(0, 0, item)
            for col in range(1, col_count):
                table_widget.setItem(0, col, QTableWidgetItem(""))

        table_widget.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
