import sys
import numpy as np
import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QMessageBox,
                             QGroupBox, QFormLayout, QDoubleSpinBox, QComboBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from astropy.io import fits
from typing import Dict, Union

plt.style.use('dark_background')

# Настройка цветовой схемы
COLORS = {
    'white': '#FFFFFF',
    'blue': '#00009A',
    'dark_blue': '#000034',
    'mid_blue': '#000015',
    'darker_blue': '#001E34',
    'gray': '#9E9E9E',
    'green': '#0DA678',
    'light_blue': '#0367B0'
}

def calculate_mass(m_k: float, delta: float, r: float) -> float:
    """Расчет массы кометы по формуле Хакатона 2025"""
    C1 = -0.4 * (-13.78)
    DENOMINATOR = 1.37e-38 * 0.031
    exponent = -0.4 * m_k + C1
    numerator = math.pow(10, exponent) * math.pow(delta, 2) * math.pow(r, 2)
    return numerator / DENOMINATOR

def calculate_diameter(H: Union[float, np.ndarray], 
                      p: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    if np.any(p <= 0) or np.any(p > 1):
        raise ValueError("Альбедо должно быть в диапазоне (0, 1]")
    return 1329 / np.sqrt(p) * 10**(-0.2 * H)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Астрофизический хакатон 2025")
        self.setMinimumSize(1000, 700)
        
        # Настройка шрифтов
        self.font = QFont("Gotman Pro", 12)
        self.title_font = QFont("Gotman Pro", 14, QFont.Medium)
        self.setFont(self.font)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный лэйаут
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Заголовок с логотипом
        header_layout = QHBoxLayout()
        self.title_label = QLabel("Астрофизический хакатон 2025")
        self.title_label.setFont(QFont("Gotman Pro", 18, QFont.Medium))
        self.title_label.setStyleSheet(f"color: {COLORS['white']};")
        header_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        main_layout.addLayout(header_layout)
        
        # Вкладки
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background: {COLORS['dark_blue']};
                border-radius: 12px;
            }}
            QTabBar::tab {{
                background: {COLORS['dark_blue']};
                color: {COLORS['white']};
                padding: 12px 24px;
                border: none;
                border-top-left-radius: 16px;
                border-top-right-radius: 16px;
                font-family: "Gotman Pro";
                font-weight: medium;
            }}
            QTabBar::tab:selected {{
                background: {COLORS['blue']};
                color: {COLORS['white']};
            }}
        """)
        
        self.tab1 = SublimationTab()
        self.tab2 = GraphsTab()
        self.tab3 = MassTab()
        self.tab4 = SizeTab()
        
        self.tabs.addTab(self.tab1, "Сублимация")
        self.tabs.addTab(self.tab2, "Графики")
        self.tabs.addTab(self.tab3, "Масса кометы")
        self.tabs.addTab(self.tab4, "Размер ядра")
        
        main_layout.addWidget(self.tabs)
        
        # Панель статуса
        self.status_bar = self.statusBar()
        self.status_bar.setFont(self.font)
        self.status_bar.setStyleSheet(f"color: {COLORS['white']};")
        
        # Кнопки управления
        control_layout = QHBoxLayout()
        control_layout.setSpacing(15)
        
        self.help_btn = QPushButton("Справка")
        self.help_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['blue']};
                color: {COLORS['white']};
                border: none;
                padding: 10px 20px;
                border-radius: 12px;
                font-family: "Gotman Pro";
                font-weight: medium;
            }}
            QPushButton:hover {{
                background-color: {COLORS['light_blue']};
            }}
        """)
        self.help_btn.clicked.connect(self.show_help)
        control_layout.addWidget(self.help_btn)
        
        self.load_btn = QPushButton("Загрузить данные")
        self.load_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['green']};
                color: {COLORS['white']};
                border: none;
                padding: 10px 20px;
                border-radius: 12px;
                font-family: "Gotman Pro";
                font-weight: medium;
            }}
            QPushButton:hover {{
                background-color: {COLORS['light_blue']};
            }}
        """)
        self.load_btn.clicked.connect(self.load_data)
        control_layout.addWidget(self.load_btn)
        
        main_layout.addLayout(control_layout)
        
        # Применение стилей
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['mid_blue']};
            }}
            QLabel {{
                color: {COLORS['white']};
                font-family: "Gotman Pro";
            }}
            QGroupBox {{
                color: {COLORS['white']};
                font-family: "Gotman Pro";
                font-weight: medium;
                border: 1px solid {COLORS['blue']};
                border-radius: 12px;
                margin-top: 10px;
                padding-top: 15px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }}
            QTextEdit, QLineEdit, QDoubleSpinBox, QComboBox {{
                background-color: {COLORS['darker_blue']};
                color: {COLORS['white']};
                border: 1px solid {COLORS['blue']};
                padding: 8px;
                border-radius: 8px;
                font-family: "Gotman Pro";
            }}
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
                width: 20px;
                border-left: 1px solid {COLORS['blue']};
            }}
            QComboBox::drop-down {{
                border-left: 1px solid {COLORS['blue']};
            }}
        """)
        
    def show_help(self):
        help_text = """
        <span style="font-family: 'Gotman Pro'; font-size: 12pt;">
        <b>Инструкция по использованию приложения:</b><br><br>
        
        1. <b>Сублимация химических элементов:</b><br>
        - Введите температуру, расстояние от Земли и Солнца<br>
        - Нажмите "Рассчитать" для получения результатов<br><br>
        
        2. <b>Интерактивные графики:</b><br>
        - Выберите тип графика из выпадающего списка<br>
        - Используйте кнопки для управления масштабом<br><br>
        
        3. <b>Расчет массы кометы:</b><br>
        - Введите видимую звездную величину, расстояние и радиус<br>
        - Результат будет отображен в соответствующем поле<br><br>
        
        4. <b>Расчет размеров ядра кометы:</b><br>
        - Введите звездную величину, альбедо и угловой размер<br>
        - Результат будет отображен с визуализацией<br><br>
        
        Для загрузки данных из файла используйте кнопку "Загрузить данные"
        </span>
        """
        msg = QMessageBox()
        msg.setWindowTitle("Справка")
        msg.setTextFormat(Qt.RichText)
        msg.setText(help_text)
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {COLORS['dark_blue']};
                font-family: "Gotman Pro";
            }}
            QLabel {{
                color: {COLORS['white']};
            }}
            QPushButton {{
                background-color: {COLORS['blue']};
                color: {COLORS['white']};
                border: none;
                padding: 5px 15px;
                border-radius: 8px;
                font-family: "Gotman Pro";
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['light_blue']};
            }}
        """)
        msg.exec_()
        
    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Открыть файл", 
            "", 
            "FITS Files (*.fits);;Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                if file_path.endswith('.fits'):
                    data = self.read_fits(file_path)
                    if 'H' in data and 'p' in data:
                        self.tab4.set_data(data['H'], data['p'])
                        self.tabs.setCurrentIndex(3)
                        self.status_bar.showMessage(f"Данные успешно загружены из файла: {file_path}", 5000)
            except Exception as e:
                self.show_error(f"Ошибка при загрузке файла: {str(e)}")
                
    def read_fits(self, file_path: str) -> Dict[str, float]:
        try:
            with fits.open(file_path) as hdul:
                header = hdul[0].header
                return {
                    'H': header['H_MAG'],
                    'p': header['ALBEDO']
                }
        except Exception as e:
            raise Exception(f"Ошибка чтения FITS файла: {str(e)}")
                
    def show_error(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle("Ошибка")
        error_box.setText(message)
        error_box.setStyleSheet(f"""
            QMessageBox {{
                background-color: {COLORS['dark_blue']};
                font-family: "Gotman Pro";
            }}
            QLabel {{
                color: {COLORS['white']};
            }}
            QPushButton {{
                background-color: {COLORS['blue']};
                color: {COLORS['white']};
                border: none;
                padding: 5px 15px;
                border-radius: 8px;
                font-family: "Gotman Pro";
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['light_blue']};
            }}
        """)
        error_box.exec_()

class SublimationTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Группа ввода параметров
        input_group = QGroupBox("Параметры сублимации")
        input_layout = QFormLayout()
        input_layout.setLabelAlignment(Qt.AlignRight)
        
        self.temp_input = QDoubleSpinBox()
        self.temp_input.setRange(0, 10000)
        self.temp_input.setValue(300)
        self.temp_input.setSuffix(" K")
        input_layout.addRow(QLabel("Температура:"), self.temp_input)
        
        self.earth_dist_input = QDoubleSpinBox()
        self.earth_dist_input.setRange(0.1, 100)
        self.earth_dist_input.setValue(1.0)
        self.earth_dist_input.setSuffix(" а.е.")
        input_layout.addRow(QLabel("Расстояние от Земли:"), self.earth_dist_input)
        
        self.sun_dist_input = QDoubleSpinBox()
        self.sun_dist_input.setRange(0.1, 100)
        self.sun_dist_input.setValue(1.0)
        self.sun_dist_input.setSuffix(" а.е.")
        input_layout.addRow(QLabel("Расстояние от Солнца:"), self.sun_dist_input)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Кнопка расчета
        self.calc_btn = QPushButton("Рассчитать сублимацию")
        self.calc_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['light_blue']};
                color: {COLORS['white']};
                border: none;
                padding: 12px 24px;
                border-radius: 12px;
                font-family: "Gotman Pro";
                font-weight: medium;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['blue']};
            }}
        """)
        self.calc_btn.clicked.connect(self.calculate_sublimation)
        layout.addWidget(self.calc_btn, alignment=Qt.AlignCenter)
        
        # Результаты
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS['darker_blue']};
                color: {COLORS['white']};
                border: 1px solid {COLORS['blue']};
                border-radius: 12px;
                padding: 12px;
            }}
        """)
        layout.addWidget(QLabel("Результаты:"))
        layout.addWidget(self.result_text)
        
        # График
        self.figure = Figure(facecolor=COLORS['dark_blue'])
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet(f"background-color: {COLORS['dark_blue']}; border-radius: 12px;")
        layout.addWidget(self.canvas)
        
    def calculate_sublimation(self):
        try:
            temp = self.temp_input.value()
            earth_dist = self.earth_dist_input.value()
            sun_dist = self.sun_dist_input.value()
            
            # Здесь должна быть логика расчета сублимации
            results = {
                "Вода": "Газ",
                "Углекислый газ": "Газ",
                "Аммиак": "Твердое",
                "Метан": "Газ"
            }
            
            result_text = "Состояние элементов при заданных условиях:\n\n"
            for element, state in results.items():
                result_text += f"{element}: {state}\n"
                
            self.result_text.setText(result_text)
            self.update_plot(temp)
            
        except Exception as e:
            self.parent().show_error(f"Ошибка расчета: {str(e)}")
            
    def update_plot(self, temp):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor(COLORS['dark_blue'])
        
        temps = np.linspace(100, 1000, 50)
        sublimation = np.exp(-5000/temps) * 100
        
        ax.plot(temps, sublimation, color=COLORS['light_blue'], linewidth=2)
        ax.axvline(x=temp, color=COLORS['green'], linestyle='--')
        ax.set_xlabel('Температура (K)', color=COLORS['white'])
        ax.set_ylabel('Скорость сублимации (%)', color=COLORS['white'])
        ax.set_title('Зависимость сублимации от температуры', color=COLORS['white'])
        ax.tick_params(colors=COLORS['white'])
        ax.grid(True, color=COLORS['blue'], alpha=0.3)
        
        self.canvas.draw()

class GraphsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Выбор типа графика
        self.graph_type = QComboBox()
        self.graph_type.addItems([
            "Afρ от расстояния", 
            "Звёздная величина от даты",
            "Спектральная характеристика"
        ])
        layout.addWidget(QLabel("Тип графика:"))
        layout.addWidget(self.graph_type)
        
        # График
        self.figure = Figure(facecolor=COLORS['dark_blue'])
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet(f"background-color: {COLORS['dark_blue']}; border-radius: 12px;")
        layout.addWidget(self.canvas)
        
        # Кнопки управления
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.zoom_in_btn = QPushButton("Приблизить")
        self.zoom_out_btn = QPushButton("Отдалить")
        self.reset_btn = QPushButton("Сброс")
        
        for btn in [self.zoom_in_btn, self.zoom_out_btn, self.reset_btn]:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['light_blue']};
                    color: {COLORS['white']};
                    border: none;
                    padding: 8px 16px;
                    border-radius: 12px;
                    font-family: "Gotman Pro";
                    font-weight: medium;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['blue']};
                }}
            """)
        
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        self.reset_btn.clicked.connect(self.reset_view)
        
        btn_layout.addWidget(self.zoom_in_btn)
        btn_layout.addWidget(self.zoom_out_btn)
        btn_layout.addWidget(self.reset_btn)
        
        layout.addLayout(btn_layout)
        self.update_graph()
        
    def update_graph(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor(COLORS['dark_blue'])
        
        graph_type = self.graph_type.currentText()
        
        if graph_type == "Afρ от расстояния":
            x = np.linspace(1, 10, 50)
            y = 100 * np.exp(-0.2 * x)
            ax.plot(x, y, color=COLORS['light_blue'])
            ax.set_xlabel('Расстояние (а.е.)', color=COLORS['white'])
            ax.set_ylabel('Afρ', color=COLORS['white'])
            ax.set_title('Зависимость Afρ от расстояния', color=COLORS['white'])
        elif graph_type == "Звёздная величина от даты":
            x = np.arange(30)
            y = 10 + 0.1 * x + np.random.normal(0, 0.5, 30)
            ax.plot(x, y, color=COLORS['green'], marker='o')
            ax.set_xlabel('Дни', color=COLORS['white'])
            ax.set_ylabel('Звёздная величина', color=COLORS['white'])
            ax.set_title('Изменение звёздной величины со временем', color=COLORS['white'])
        else:
            x = np.linspace(3000, 8000, 100)
            y = np.exp(-(x-5000)**2/(2*500**2))
            ax.plot(x, y, color=COLORS['blue'])
            ax.set_xlabel('Длина волны (Å)', color=COLORS['white'])
            ax.set_ylabel('Интенсивность', color=COLORS['white'])
            ax.set_title('Спектральная характеристика', color=COLORS['white'])
            
        ax.tick_params(colors=COLORS['white'])
        ax.grid(True, color=COLORS['blue'], alpha=0.3)
        self.canvas.draw()
        
    def zoom_in(self):
        ax = self.figure.gca()
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        ax.set_xlim(xlim[0]*0.9, xlim[1]*0.9)
        ax.set_ylim(ylim[0]*0.9, ylim[1]*0.9)
        self.canvas.draw()
        
    def zoom_out(self):
        ax = self.figure.gca()
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        ax.set_xlim(xlim[0]*1.1, xlim[1]*1.1)
        ax.set_ylim(ylim[0]*1.1, ylim[1]*1.1)
        self.canvas.draw()
        
    def reset_view(self):
        self.update_graph()

class MassTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Группа ввода параметров
        input_group = QGroupBox("Параметры кометы")
        input_layout = QFormLayout()
        input_layout.setLabelAlignment(Qt.AlignRight)
        
        self.mag_input = QDoubleSpinBox()
        self.mag_input.setRange(-30, 30)
        self.mag_input.setValue(10.0)
        input_layout.addRow(QLabel("Видимая звёздная величина (mₖ):"), self.mag_input)
        
        self.delta_input = QDoubleSpinBox()
        self.delta_input.setRange(0.1, 100)
        self.delta_input.setValue(1.0)
        self.delta_input.setSuffix(" а.е.")
        input_layout.addRow(QLabel("Расстояние (Δ):"), self.delta_input)
        
        self.r_input = QDoubleSpinBox()
        self.r_input.setRange(0.1, 100)
        self.r_input.setValue(1.0)
        self.r_input.setSuffix(" а.е.")
        input_layout.addRow(QLabel("Радиус (r):"), self.r_input)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Кнопка расчета
        self.calc_btn = QPushButton("Рассчитать массу")
        self.calc_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['light_blue']};
                color: {COLORS['white']};
                border: none;
                padding: 12px 24px;
                border-radius: 12px;
                font-family: "Gotman Pro";
                font-weight: medium;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['blue']};
            }}
        """)
        self.calc_btn.clicked.connect(self.calculate_mass)
        layout.addWidget(self.calc_btn, alignment=Qt.AlignCenter)
        
        # Результат
        self.result_label = QLabel("Масса кометы: ")
        self.result_label.setStyleSheet(f"""
            font-family: "Gotman Pro";
            font-weight: medium;
            font-size: 16px;
            color: {COLORS['white']};
        """)
        layout.addWidget(self.result_label, alignment=Qt.AlignCenter)
        
        # Подсказки
        tips = QLabel("""
        <small>Подсказки:<br>
        - Видимая звёздная величина: обычно от -1 (очень яркие) до +20 (очень тусклые)<br>
        - Расстояние и радиус: в астрономических единицах (1 а.е. = 149.6 млн км)
        </small>
        """)
        tips.setStyleSheet(f"color: {COLORS['gray']}; font-family: 'Gotman Pro';")
        layout.addWidget(tips)
        
    def calculate_mass(self):
        try:
            m_k = self.mag_input.value()
            delta = self.delta_input.value()
            r = self.r_input.value()
            
            mass = calculate_mass(m_k, delta, r)
            
            if mass >= 1e20:
                formatted_mass = f"{mass/1e21:.2f} × 10²¹ кг"
            elif mass >= 1e17:
                formatted_mass = f"{mass/1e18:.2f} × 10¹⁸ кг"
            else:
                formatted_mass = f"{mass:.2e} кг"
                
            self.result_label.setText(f"Полная масса кометы: {formatted_mass}")
            
        except Exception as e:
            self.parent().show_error(f"Ошибка расчета массы: {str(e)}")

class SizeTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Группа ввода параметров
        input_group = QGroupBox("Параметры ядра кометы")
        input_layout = QFormLayout()
        input_layout.setLabelAlignment(Qt.AlignRight)
        
        self.H_input = QDoubleSpinBox()
        self.H_input.setRange(-10, 30)
        self.H_input.setValue(15.0)
        input_layout.addRow(QLabel("Абсолютная звёздная величина (H):"), self.H_input)
        
        self.p_input = QDoubleSpinBox()
        self.p_input.setRange(0.01, 1.0)
        self.p_input.setValue(0.04)
        self.p_input.setSingleStep(0.01)
        input_layout.addRow(QLabel("Альбедо (p):"), self.p_input)
        
        self.angular_input = QDoubleSpinBox()
        self.angular_input.setRange(0.1, 100)
        self.angular_input.setValue(10.0)
        self.angular_input.setSuffix(" угл. сек.")
        input_layout.addRow(QLabel("Угловой размер:"), self.angular_input)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Кнопки
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.calc_btn = QPushButton("Рассчитать размер")
        self.calc_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['light_blue']};
                color: {COLORS['white']};
                border: none;
                padding: 12px 24px;
                border-radius: 12px;
                font-family: "Gotman Pro";
                font-weight: medium;
            }}
            QPushButton:hover {{
                background-color: {COLORS['blue']};
            }}
        """)
        self.calc_btn.clicked.connect(self.calculate_size)
        btn_layout.addWidget(self.calc_btn)
        
        self.load_btn = QPushButton("Загрузить из FITS")
        self.load_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['green']};
                color: {COLORS['white']};
                border: none;
                padding: 12px 24px;
                border-radius: 12px;
                font-family: "Gotman Pro";
                font-weight: medium;
            }}
            QPushButton:hover {{
                background-color: {COLORS['light_blue']};
            }}
        """)
        self.load_btn.clicked.connect(self.load_from_fits)
        btn_layout.addWidget(self.load_btn)
        
        layout.addLayout(btn_layout)
        
        # Результаты
        self.result_label = QLabel("Диаметр ядра: ")
        self.result_label.setStyleSheet(f"""
            font-family: "Gotman Pro";
            font-weight: medium;
            font-size: 16px;
            color: {COLORS['white']};
        """)
        layout.addWidget(self.result_label, alignment=Qt.AlignCenter)
        
        # Визуализация
        self.figure = Figure(facecolor=COLORS['dark_blue'])
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet(f"background-color: {COLORS['dark_blue']}; border-radius: 12px;")
        layout.addWidget(self.canvas)
        
    def calculate_size(self):
        try:
            H = self.H_input.value()
            p = self.p_input.value()
            angular_size = self.angular_input.value()
            
            if p <= 0 or p > 1:
                raise ValueError("Альбедо должно быть в диапазоне (0, 1]")
                
            diameter = calculate_diameter(H, p)
            self.result_label.setText(f"Диаметр ядра: {diameter:.2f} км")
            self.update_visualization(diameter, angular_size)
            
        except Exception as e:
            self.parent().show_error(f"Ошибка расчета размера: {str(e)}")
            
    def update_visualization(self, diameter, angular_size):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor(COLORS['dark_blue'])
        
        # Рисуем схематичное изображение кометы
        nucleus = plt.Circle((0.5, 0.5), 0.2, color=COLORS['gray'])
        ax.add_patch(nucleus)
        
        # Хвост
        ax.plot([0.5, 0.9], [0.5, 0.5], color=COLORS['light_blue'], linewidth=2, alpha=0.5)
        ax.plot([0.5, 0.9], [0.45, 0.4], color=COLORS['light_blue'], linewidth=1, alpha=0.3)
        ax.plot([0.5, 0.9], [0.55, 0.6], color=COLORS['light_blue'], linewidth=1, alpha=0.3)
        
        # Подписи
        ax.text(0.5, 0.25, f"Диаметр: {diameter:.1f} км", 
                ha='center', color=COLORS['white'], fontfamily='Gotman Pro')
        ax.text(0.5, 0.2, f"Угловой размер: {angular_size}''", 
                ha='center', color=COLORS['white'], fontfamily='Gotman Pro')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Схематичное изображение кометы', 
                    color=COLORS['white'], fontfamily='Gotman Pro')
        
        self.canvas.draw()
        
    def load_from_fits(self):
        self.parent().load_data()
        
    def set_data(self, H, p):
        self.H_input.setValue(H)
        self.p_input.setValue(p)
        self.calculate_size()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Установка шрифта по умолчанию
    font = QFont("Gotman Pro", 12)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())