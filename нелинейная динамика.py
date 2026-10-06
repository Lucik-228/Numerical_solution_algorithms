import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 1. Начальные параметры системы
init_a = 4.0
init_b = 0.98
init_x0 = 0.65  # Начальное состояние x_0
num_steps = 100  # Количество шагов (итераций) во времени


# 2. Функция итерационного расчета (временного ряда)
def generate_trajectory(a, b, x0, steps):
    trajectory = np.zeros(steps)
    trajectory[0] = x0

    for t in range(1, steps):
        prev_x = trajectory[t - 1]
        # Проверяем на отрицательные значения, чтобы корень (**0.5) не выдал ошибку
        if prev_x < 0:
            prev_x = 0

        # Уравнение, где текущее значение зависит от предыдущего
        trajectory[t] = a * (prev_x ** 0.5) * (1 - b * (prev_x ** 0.5))

    return trajectory


# Генерируем массив шагов времени [0, 1, 2, ..., steps]
time_steps = np.arange(num_steps)
y_values = generate_trajectory(init_a, init_b, init_x0, num_steps)

# 3. Настройка окна отображения
fig, ax = plt.subplots(figsize=(9, 6))
plt.subplots_adjust(bottom=0.3)  # Место для ползунков снизу

# Строим график динамики (траектории во времени)
line, = ax.plot(time_steps, y_values, lw=2, color='crimson', marker='.', label='Траектория $x_t$')
ax.set_xlabel('Шаг времени ($t$)')
ax.set_ylabel('Значение ($x_t$)')
ax.set_title('Динамика системы: $x_t = a\sqrt{x_{t-1}}(1 - b\sqrt{x_{t-1}})$')
ax.grid(True)
ax.legend()

# 4. Создаем оси для ползунков
ax_a = plt.axes([0.15, 0.16, 0.65, 0.03])
ax_b = plt.axes([0.15, 0.10, 0.65, 0.03])
ax_x0 = plt.axes([0.15, 0.04, 0.65, 0.03])

# Создаем ползунки (добавили ползунок для начального значения x0)
slider_a = Slider(ax_a, 'Параметр a', 0.1, 4.0, valinit=init_a, valfmt='%.2f')
slider_b = Slider(ax_b, 'Параметр b', 0.01, 2.0, valinit=init_b, valfmt='%.2f')
slider_x0 = Slider(ax_x0, 'Старт (x0)', 0.0, 2.0, valinit=init_x0, valfmt='%.3f')


# 5. Функция обновления при движении ползунков
def update(val):
    a = slider_a.val
    b = slider_b.val
    x0 = slider_x0.val

    # Пересчитываем всю цепочку значений заново с новыми коэффициентами
    new_y = generate_trajectory(a, b, x0, num_steps)
    line.set_ydata(new_y)

    # Корректируем масштаб сетки под новые значения
    ax.relim()
    ax.autoscale_view(scalex=False, scaley=True)

    fig.canvas.draw_idle()


# Связываем ползунки с обработчиком
slider_a.on_changed(update)
slider_b.on_changed(update)
slider_x0.on_changed(update)

plt.show()
