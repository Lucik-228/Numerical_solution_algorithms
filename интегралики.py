import math


# --- 1. ОПРЕДЕЛЕНИЕ ФУНКЦИЙ ---


def f_sin(x):
    """y = sin(x)"""
    return math.sin(x)


def f_abs(x):
    """y = |x - 1|"""
    return abs(x - 1)


def f_sqrt(x):
    """y = sqrt(x)"""
    return math.sqrt(x)


# --- 2. МЕТОДЫ ИНТЕГРИРОВАНИЯ ---


def trapezoidal_rule(func, a, b, n):
    """Метод трапеций"""
    h = (b - a) / n
    total_sum = 0.5 * (func(a) + func(b))
    for i in range(1, n):
        total_sum += func(a + i * h)
    return total_sum * h


def simpson_rule(func, a, b, n):
    """Метод Симпсона (парабол)"""
    h = (b - a) / n
    total_sum = func(a) + func(b)

    for i in range(1, n):
        x = a + i * h
        if i % 2 == 0:
            total_sum += 2 * func(x)  # Четные индексы
        else:
            total_sum += 4 * func(x)  # Нечетные индексы

    return total_sum * (h / 3)


# --- 3. РАСЧЕТ ПОКАЗАТЕЛЯ РУНГЕ ---


def calculate_runge_p(I1, I2, I3):
    """Оценка порядка точности p по формуле Рунге"""
    numerator = I2 - I1
    denominator = I3 - I2

    if abs(denominator) < 1e-15:
        return float("nan")

    ratio = abs(numerator / denominator)
    return math.log2(ratio)


# --- 4. ОСНОВНОЙ БЛОК ВЫЧИСЛЕНИЙ С ПАРАЛЛЕЛЬНЫМ ВЫВОДОМ ---


def process_function(name, func, a, b, n1):
    """Вычисляет оба метода параллельно и выводит результаты в таблицу рядом"""
    n2 = n1 * 2
    n3 = n2 * 2

    # Расчет методом трапеций
    I1_t = trapezoidal_rule(func, a, b, n1)
    I2_t = trapezoidal_rule(func, a, b, n2)
    I3_t = trapezoidal_rule(func, a, b, n3)
    p_t = calculate_runge_p(I1_t, I2_t, I3_t)

    # Расчет методом Симпсона
    I1_s = simpson_rule(func, a, b, n1)
    I2_s = simpson_rule(func, a, b, n2)
    I3_s = simpson_rule(func, a, b, n3)
    p_s = calculate_runge_p(I1_s, I2_s, I3_s)

    # Вывод красивой таблицы в консоль
    print("=" * 72)
    print(f" ФУНКЦИЯ: {name:15} Отрезок: [{a}, {b}]")
    print("=" * 72)
    print(f" {'Параметр сетки':<18} | {'Метод трапеций':<22} | {'Метод Симпсона':<22}")
    print("-" * 72)
    print(f"  I1 (n = {n1:<3})        |  {I1_t:<20.8f} |  {I1_s:<20.8f}")
    print(f"  I2 (n = {n2:<3})        |  {I2_t:<20.8f} |  {I2_s:<20.8f}")
    print(f"  I3 (n = {n3:<3})        |  {I3_t:<20.8f} |  {I3_s:<20.8f}")
    print("-" * 72)

    # Форматирование вывода Рунге p (чтобы не упало, если вдруг NaN)
    p_t_str = f"{p_t:.4f}" if not math.isnan(p_t) else "NaN"
    p_s_str = f"{p_s:.4f}" if not math.isnan(p_s) else "NaN"

    print(f"  Показатель Рунге p |  {p_t_str:<20} |  {p_s_str:<20}")
    print("=" * 72)
    print("\n")


# --- НАСТРОЙКА И ЗАПУСК ---

# Начальное количество разбиений
initial_n = 10

# Запуск расчетов для всех трех функций
process_function("y = sin(x)", f_sin, 0, math.pi, initial_n)
process_function("y = |x - 1|", f_abs, 0, 2, initial_n)
process_function("y = sqrt(x)", f_sqrt, 0, 1, initial_n)
