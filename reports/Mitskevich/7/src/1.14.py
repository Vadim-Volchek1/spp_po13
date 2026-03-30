import sys
import random
import math
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QLabel,
)
from PySide6.QtCore import QTimer, Qt, QPointF
from PySide6.QtGui import QPainter, QColor, QPen


class Point:
    """Класс, представляющий движущуюся точку."""

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        # Вектор движения (скорость по осям)
        self.vel_x = random.uniform(-1, 1)
        self.vel_y = random.uniform(-1, 1)

    def move(self, width, height, speed):
        """Обновляет координаты точки с учетом скорости и границ окна."""
        self.pos_x += self.vel_x * speed
        self.pos_y += self.vel_y * speed

        # Отскок от левой и правой границ
        if self.pos_x <= 0 or self.pos_x >= width:
            self.vel_x *= -1
        # Отскок от верхней и нижней границ
        if self.pos_y <= 0 or self.pos_y >= height:
            self.vel_y *= -1


class Line:
    """Класс, представляющий прямую линию, заданную двумя точками."""

    def __init__(self, point_start: QPointF, point_end: QPointF):
        self.point_start = point_start
        self.point_end = point_end

    def get_distance(self, target_point: Point):
        """Вычисляет расстояние от точки до прямой по формуле перпендикуляра."""
        x_1, y_1 = self.point_start.x(), self.point_start.y()
        x_2, y_2 = self.point_end.x(), self.point_end.y()

        # Числитель формулы: |(y2-y1)x0 - (x2-x1)y0 + x2y1 - y2x1|
        numerator = abs(
            (y_2 - y_1) * target_point.pos_x
            - (x_2 - x_1) * target_point.pos_y
            + x_2 * y_1
            - y_2 * x_1
        )
        # Знаменатель: sqrt((y2-y1)^2 + (x2-x1)^2)
        denominator = math.sqrt((y_2 - y_1) ** 2 + (x_2 - x_1) ** 2)

        # Возвращаем расстояние с защитой от деления на ноль
        return numerator / (denominator + 1e-6)


class Canvas(QWidget):
    """Виджет для визуализации движения точек и отрисовки прямой."""

    def __init__(self):
        super().__init__()
        self.points = []
        self.line = Line(QPointF(50, 50), QPointF(550, 350))
        self.speed = 1.0
        self.is_paused = False
        self.furthest_point = None
        self.setMinimumSize(600, 400)

    def update_points_count(self, count):
        """Создает новый список из заданного количества случайных точек."""
        self.points = [
            Point(random.randint(10, 550), random.randint(10, 350))
            for _ in range(count)
        ]
        self.update()

    def find_furthest(self):
        """Находит точку, наиболее удаленную от линии."""
        if not self.points:
            return
        # передаем метод напрямую
        self.furthest_point = max(self.points, key=self.line.get_distance)

    def paintEvent(self, _event):
        """Метод отрисовки всех графических примитивов."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Рисуем линию (зеленая)
        pen_line = QPen(Qt.green, 3)
        painter.setPen(pen_line)
        painter.drawLine(self.line.point_start, self.line.point_end)

        # Рисуем точки
        self.find_furthest()
        for point in self.points:
            if point == self.furthest_point:
                # Дальняя точка: красная с белой обводкой и линией-связью
                painter.setBrush(QColor("red"))
                painter.setPen(QPen(Qt.white, 1))
                painter.drawLine(
                    QPointF(point.pos_x, point.pos_y), self.line.point_start
                )
            else:
                # Обычные точки: розовые
                painter.setBrush(QColor("pink"))
                painter.setPen(QPen(Qt.gray, 1))

            painter.drawEllipse(QPointF(point.pos_x, point.pos_y), 5, 5)

    def step(self):
        """Шаг анимации: движение точек и перерисовка."""
        if not self.is_paused:
            for point in self.points:
                point.move(self.width(), self.height(), self.speed)
            self.update()


class MainWindow(QMainWindow):
    """Главное окно приложения с панелью управления."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная 7: Поиск удаленной точки")

        self.canvas = Canvas()
        self.canvas.update_points_count(10)

        # Элементы интерфейса
        self.speed_slider = QSlider(Qt.Horizontal)
        self.count_slider = QSlider(Qt.Horizontal)
        self.btn_pause = QPushButton("Пауза")
        self.timer = QTimer()

        self._setup_ui()

    def _setup_ui(self):
        """Инициализация и компоновка интерфейса."""
        controls = QVBoxLayout()

        # Настройка слайдера скорости
        controls.addWidget(QLabel("Скорость движения:"))
        self.speed_slider.setRange(0, 10)
        self.speed_slider.setValue(2)
        self.speed_slider.valueChanged.connect(self.change_speed)
        controls.addWidget(self.speed_slider)

        # Настройка слайдера количества точек
        controls.addWidget(QLabel("Количество точек (n):"))
        self.count_slider.setRange(2, 100)
        self.count_slider.setValue(10)
        self.count_slider.valueChanged.connect(self.change_count)
        controls.addWidget(self.count_slider)

        # Кнопка паузы
        self.btn_pause.clicked.connect(self.toggle_pause)
        controls.addWidget(self.btn_pause)

        # Основная компоновка
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.canvas, stretch=4)
        main_layout.addLayout(controls, stretch=1)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Таймер
        self.timer.timeout.connect(self.canvas.step)
        self.timer.start(20)

    def change_speed(self, value):
        """Слот для изменения скорости движения."""
        self.canvas.speed = value

    def change_count(self, value):
        """Слот для изменения количества точек."""
        self.canvas.update_points_count(value)

    def toggle_pause(self):
        """Слот для включения/выключения паузы."""
        self.canvas.is_paused = not self.canvas.is_paused
        self.btn_pause.setText("Продолжить" if self.canvas.is_paused else "Пауза")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1000, 600)
    window.show()
    sys.exit(app.exec())
