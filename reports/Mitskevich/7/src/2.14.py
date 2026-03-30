import sys
import numpy as np
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QLabel,
    QLineEdit,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter


class NewtonFractal:
    """Класс для вычисления математической логики фрактала Ньютона."""

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def generate(self, degree, alpha, iterations):
        """
        Генерирует массив пикселей фрактала.
        :param degree: Степень уравнения z^n - 1 = 0
        :param alpha: Коэффициент расслабления метода Ньютона
        :param iterations: Количество итераций
        :return: Массив NumPy (RGB)
        """
        # Создаем координатную сетку
        x_coords = np.linspace(-2, 2, self.width)
        y_coords = np.linspace(-2, 2, self.height)
        x_grid, y_grid = np.meshgrid(x_coords, y_coords)
        z_plane = x_grid + 1j * y_grid

        # Массив для фиксации скорости сходимости
        convergence = np.zeros(z_plane.shape, dtype=float)

        for _ in range(iterations):
            z_old = z_plane.copy()
            # Формула Ньютона: z = z - a * (z^n - 1) / (n * z^(n-1))
            f_z = z_plane**degree - 1
            df_z = degree * z_plane ** (degree - 1)

            # Защита от деления на 0
            df_z[np.abs(df_z) < 1e-6] = 1e-6
            z_plane -= alpha * f_z / df_z

            # Считаем близость к корню для визуализации яркости
            convergence += np.exp(-np.abs(z_plane - z_old))

        # Определяем корень через угол комплексного числа
        roots = np.angle(z_plane)

        # Подготовка каналов цвета
        hue = ((roots + np.pi) / (2 * np.pi) * 255).astype(np.uint8)
        brightness = ((convergence / iterations) * 255).astype(np.uint8)

        # Формируем итоговый RGB массив
        img_array = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        img_array[..., 0] = hue  # Красный канал
        img_array[..., 1] = brightness  # Зеленый канал
        img_array[..., 2] = 150  # Синий канал

        return img_array


class FractalCanvas(QWidget):
    """Виджет для отрисовки фрактала на экране."""

    def __init__(self):
        super().__init__()
        self.fractal_engine = NewtonFractal(600, 600)
        self.degree = 3.0
        self.alpha = 1.0
        self.max_iters = 30
        self.image = QImage()
        self.render_fractal()

    def render_fractal(self):
        """Запускает расчет фрактала и обновляет изображение."""
        raw_data = self.fractal_engine.generate(self.degree, self.alpha, self.max_iters)
        height, width, _ = raw_data.shape
        # Сохраняем ссылку на данные, чтобы Python не удалил их из памяти
        self.image = QImage(
            raw_data.data, width, height, width * 3, QImage.Format_RGB888
        )
        # Принудительно копируем изображение, чтобы избежать проблем с памятью данных NumPy
        self.image = self.image.copy()
        self.update()

    def paintEvent(self, _event):
        """Метод отрисовки виджета."""
        if not self.image.isNull():
            painter = QPainter(self)
            painter.drawImage(self.rect(), self.image)


class MainWindow(QMainWindow):
    """Главное окно приложения с элементами управления."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Построение Бассейнов Ньютона")

        self.canvas = FractalCanvas()

        # Создание интерфейса
        self.n_input = QLineEdit("3")
        self.alpha_slider = QSlider(Qt.Horizontal)
        self.iter_slider = QSlider(Qt.Horizontal)
        self.btn_refresh = QPushButton("Обновить график")

        self._setup_ui()

    def _setup_ui(self):
        """Настройка расположения элементов управления."""
        controls = QVBoxLayout()

        # Поле ввода степени
        controls.addWidget(QLabel("Степень уравнения (n):"))
        self.n_input.setPlaceholderText("Введите число...")
        self.n_input.editingFinished.connect(self.apply_params)
        controls.addWidget(self.n_input)

        # Слайдер коэффициента а
        controls.addWidget(QLabel("Коэффициент расслабления (a):"))
        self.alpha_slider.setRange(1, 20)
        self.alpha_slider.setValue(10)
        self.alpha_slider.valueChanged.connect(self.apply_params)
        controls.addWidget(self.alpha_slider)

        # Слайдер итераций
        controls.addWidget(QLabel("Глубина прорисовки:"))
        self.iter_slider.setRange(5, 60)
        self.iter_slider.setValue(30)
        self.iter_slider.valueChanged.connect(self.apply_params)
        controls.addWidget(self.iter_slider)

        # Кнопка
        self.btn_refresh.clicked.connect(self.apply_params)
        controls.addWidget(self.btn_refresh)

        # Основная компоновка
        layout = QHBoxLayout()
        layout.addWidget(self.canvas, stretch=4)
        layout.addLayout(controls, stretch=1)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def apply_params(self):
        """Считывает параметры из UI и инициирует перерисовку."""
        try:
            val_n = float(self.n_input.text())
            # Защита от деления на 0 при степени 0
            self.canvas.degree = val_n if val_n != 0 else 0.1
        except ValueError:
            pass  # Игнорируем некорректный ввод

        self.canvas.alpha = self.alpha_slider.value() / 10.0
        self.canvas.max_iters = self.iter_slider.value()
        self.canvas.render_fractal()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(900, 650)
    window.show()
    sys.exit(app.exec())
