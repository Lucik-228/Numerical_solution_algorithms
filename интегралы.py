import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.special import sici


# Подынтегральная функция
def f(x):
    return np.sin(x) / x


# Точное значение интеграла через интегральный синус
exact_val = sici(2)[0] - sici(1)[0]


# Функции численного интегрирования
def left_rectangles(n):
    h = 1.0 / n
    x = np.linspace(1, 2, n, endpoint=False)
    return h * np.sum(f(x))


def right_rectangles(n):
    h = 1.0 / n
    x = np.linspace(1 + h, 2, n, endpoint=True)
    return h * np.sum(f(x))


def midpoint_rectangles(n):
    h = 1.0 / n
    x = np.linspace(1 + h / 2, 2 - h / 2, n)
    return h * np.sum(f(x))


def trapezoidal(n):
    h = 1.0 / n
    x = np.linspace(1, 2, n + 1)
    y = f(x)
    return h * (0.5 * y[0] + np.sum(y[1:-1]) + 0.5 * y[-1])


def simpson_13(n):
    if n % 2 != 0:
        return None
    h = 1.0 / n
    x = np.linspace(1, 2, n + 1)
    y = f(x)
    return h / 3 * (y[0] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-1:2]) + y[-1])


def simpson_38(n):
    if n % 3 != 0:
        return None
    h = 1.0 / n
    x = np.linspace(1, 2, n + 1)
    y = f(x)
    s = y[0] + y[-1]
    for i in range(1, n):
        if i % 3 == 0:
            s += 2 * y[i]
        else:
            s += 3 * y[i]
    return (3 * h / 8) * s


# Настройка интерактивного окна Matplotlib
fig, ax = plt.subplots(figsize=(13, 6))
plt.subplots_adjust(left=0.08, bottom=0.25, right=0.55)

x_plot = np.linspace(0.8, 2.2, 400)
ax.plot(x_plot, f(x_plot), 'r', lw=2, label='f(x) = sin(x)/x')
ax.set_xlim(0.9, 2.1)
ax.set_ylim(0.4, 0.9)
ax.grid(True)
ax.set_title("Численное интегрирование sin(x)/x от 1 до 2")

# Подняли координату Y до 0.40, чтобы длинный текст не обрезался снизу
text_box = fig.text(0.58, 0.40, '', fontsize=10, fontfamily='monospace',
                    verticalalignment='top',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='whitesmoke', alpha=0.9, edgecolor='gray'))

# Слайдер для изменения n
ax_n = plt.axes([0.08, 0.1, 0.43, 0.03])
slider_n = Slider(ax_n, 'Шаги (n)', 1, 60, valinit=6, valstep=1)


def update(val):
    n = int(slider_n.val)

    for coll in list(ax.collections):
        coll.remove()

    x_steps = np.linspace(1, 2, n + 1)
    ax.vlines(x_steps, 0, f(x_steps), colors='gray', linestyles='dashed', alpha=0.3)
    ax.fill_between(x_steps, 0, f(x_steps), facecolor='blue', alpha=0.07)

    i_left = left_rectangles(n)
    i_right = right_rectangles(n)
    i_mid = midpoint_rectangles(n)
    i_trap = trapezoidal(n)
    i_simp = simpson_13(n)
    i_38 = simpson_38(n)

    # Структура: (Название, Значение, Доступность)
    methods_data = [
        ("Левые прямоуг. ", i_left, True),
        ("Правые прямоуг.", i_right, True),
        ("Средн прямоуг.", i_mid, True),
        ("Трапеции       ", i_trap, True),
        ("Симпсон (1/3)  ", i_simp, i_simp is not None),
        ("Правило 3/8    ", i_38, i_38 is not None)
    ]

    available_methods = []
    unavailable_methods = []

    for name, val_m, is_avail in methods_data:
        if is_avail:
            abs_err = val_m - exact_val
            # Расчет относительной погрешности в процентах
            rel_err = abs(abs_err / exact_val) * 100
            available_methods.append((name, val_m, abs_err, rel_err))
        else:
            unavailable_methods.append((name, None, None, None))

    # Сортировка по абсолютной (или относительной, они пропорциональны) погрешности
    available_methods.sort(key=lambda item: abs(item[2]))

    # Формирование таблицы результатов
    res_text = f"Шагов разбиения (n): {n}\n"
    res_text += f"Точное значение: {exact_val:.6f}\n"
    res_text += "—" * 60 + "\n"
    res_text += "Метод (от лучшего) |  Знач.  | Абс.погр | Отн.погр (%)\n"
    res_text += "—" * 60 + "\n"

    for name, val_m, abs_e, rel_e in available_methods:
        # Если относительная погрешность меньше 0.0001%, пишем её в экспоненциальном виде
        if rel_e < 1e-4 and rel_e > 0:
            rel_str = f"{rel_e:.2e}%"
        elif rel_e == 0:
            rel_str = "0.000000%"
        else:
            rel_str = f"{rel_e:.6f}%"

        res_text += f"{name}: {val_m:.6f} ({abs_e:+.6f}) | {rel_str}\n"

    if unavailable_methods:
        res_text += "—" * 60 + "\n"
        for name, _, _, _ in unavailable_methods:
            if "Симпсон" in name:
                res_text += f"{name}: (n должно быть четным)\n"
            else:
                res_text += f"{name}: (n должно быть кратно 3)\n"

    text_box.set_text(res_text)
    fig.canvas.draw_idle()


slider_n.on_changed(update)
update(6)

plt.show()
