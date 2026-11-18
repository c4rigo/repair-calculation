# -*- coding: utf-8 -*-
"""
Калькулятор материалов для ремонта (учебный проект на Streamlit).

Как запустить:
    1. Установите библиотеку:  pip install streamlit
    2. Запустите приложение:   streamlit run app.py
"""

import math

import streamlit as st

# Настройки страницы (должны вызываться первой командой Streamlit)
st.set_page_config(page_title="Калькулятор материалов для ремонта", page_icon="🧱")

# ---------------------------------------------------------------------------
# Константы: стандартные размеры проёмов, м (используются как значения по умолчанию)
# ---------------------------------------------------------------------------
DOOR_W, DOOR_H = 0.9, 2.0        # дверь: 0.9 × 2.0 м
WINDOW_W, WINDOW_H = 1.4, 1.4    # окно: 1.4 × 1.4 м

# ---------------------------------------------------------------------------
# Заголовок и описание
# ---------------------------------------------------------------------------
st.title("🧱 Калькулятор материалов для ремонта")
st.write(
    "Введите параметры комнаты, и приложение подскажет, сколько нужно купить "
    "краски, обоев, плитки и линолеума. Рядом с полями есть значок «?» с подсказкой."
)

# ---------------------------------------------------------------------------
# Входные данные
# ---------------------------------------------------------------------------
st.header("Параметры комнаты")

col1, col2, col3 = st.columns(3)
with col1:
    length = st.number_input("Длина комнаты, м", min_value=0.1, value=4.0, step=0.1)
with col2:
    width = st.number_input("Ширина комнаты, м", min_value=0.1, value=3.0, step=0.1)
with col3:
    height = st.number_input("Высота стен, м", min_value=0.1, value=2.7, step=0.1)

col4, col5 = st.columns(2)
with col4:
    doors = st.number_input("Количество дверей", min_value=0, max_value=10, value=1, step=1)
with col5:
    windows = st.number_input("Количество окон", min_value=0, max_value=10, value=1, step=1)

# Списки размеров: для каждой двери и каждого окна свои (ширина, высота)
door_sizes = []
window_sizes = []

with st.expander("Изменить размеры дверей и окон (по умолчанию стандартные)"):
    st.caption(
        "Если окна или двери нестандартные, впишите их размеры. "
        "У каждой двери и каждого окна размеры можно задать свои."
    )
    # Цикл по дверям: для каждой создаём два поля (ширина и высота)
    for i in range(doors):
        st.markdown(f"**Дверь {i + 1}**")
        cw, ch = st.columns(2)
        with cw:
            dw = st.number_input(
                f"Ширина двери {i + 1}, м", min_value=0.1, value=DOOR_W, step=0.05,
                key=f"door_w_{i}",
            )
        with ch:
            dh = st.number_input(
                f"Высота двери {i + 1}, м", min_value=0.1, value=DOOR_H, step=0.05,
                key=f"door_h_{i}",
            )
        door_sizes.append((dw, dh))
    # Цикл по окнам
    for i in range(windows):
        st.markdown(f"**Окно {i + 1}**")
        cw, ch = st.columns(2)
        with cw:
            ww = st.number_input(
                f"Ширина окна {i + 1}, м", min_value=0.1, value=WINDOW_W, step=0.05,
                key=f"window_w_{i}",
            )
        with ch:
            wh = st.number_input(
                f"Высота окна {i + 1}, м", min_value=0.1, value=WINDOW_H, step=0.05,
                key=f"window_h_{i}",
            )
        window_sizes.append((ww, wh))

# ---------------------------------------------------------------------------
# 1. Общие площади
# ---------------------------------------------------------------------------
st.divider()
st.header("1. Общие площади")

# Периметр комнаты:        P = 2 × (длина + ширина)
perimeter = 2 * (length + width)
# Площадь стен с проёмами: S_стен_брутто = P × высота
walls_gross = perimeter * height
# Площадь дверей:          сумма (ширина × высота) по всем дверям
doors_area = sum(w * h for w, h in door_sizes)
# Площадь окон:            сумма (ширина × высота) по всем окнам
windows_area = sum(w * h for w, h in window_sizes)
# Площадь проёмов:         S_проёмов = S_дверей + S_окон
openings_area = doors_area + windows_area
# Площадь стен без проёмов: S_стен = S_стен_брутто − S_проёмов
walls_area = walls_gross - openings_area
# Площадь пола:            S_пола = длина × ширина
floor_area = length * width

# Проверка: площадь стен должна быть положительной
if walls_area <= 0:
    st.error(
        "Площадь стен получилась ≤ 0. Проверьте размеры комнаты, "
        "дверей и окон."
    )
    st.stop()

st.success(
    f"Площадь стен без проёмов: **{walls_area:.2f} м²**  \n"
    f"Площадь пола: **{floor_area:.2f} м²**  \n"
    f"Периметр: **{perimeter:.2f} м**"
)

with st.expander("Как считали"):
    st.latex(r"P = 2 \cdot (a + b)")
    st.latex(r"S_{\text{проёмов}} = \sum S_{\text{дверей}} + \sum S_{\text{окон}}")
    st.latex(r"S_{\text{стен}} = P \cdot h - S_{\text{проёмов}}")
    st.latex(r"S_{\text{пола}} = a \cdot b")
    st.write(f"Периметр: 2 × ({length} + {width}) = {perimeter:.2f} м")
    st.write(f"Стены с проёмами: {perimeter:.2f} × {height} = {walls_gross:.2f} м²")
    st.write(
        f"Проёмы: двери {doors_area:.2f} м² + окна {windows_area:.2f} м² = "
        f"{openings_area:.2f} м²"
    )
    st.write(f"Стены без проёмов: {walls_gross:.2f} − {openings_area:.2f} = {walls_area:.2f} м²")
    st.write(f"Пол: {length} × {width} = {floor_area:.2f} м²")

# ---------------------------------------------------------------------------
# 2. Краска
# ---------------------------------------------------------------------------
st.divider()
st.header("2. Краска")

c1, c2 = st.columns(2)
with c1:
    consumption = st.number_input(
        "Расход краски, м²/л (за один слой)", min_value=0.1, value=10.0, step=0.5,
        help=(
            "Сколько квадратных метров стены покрывает 1 литр краски за один слой. "
            "Эта цифра написана на банке (ищите слово «расход»). Чаще всего "
            "8–12 м² на литр. Если краску ещё не выбрали, оставьте 10."
        ),
    )
with c2:
    layers = st.number_input(
        "Количество слоёв", min_value=1, value=2, step=1,
        help="Обычно красят в 2 слоя. Если красите тёмную стену в светлый цвет, может понадобиться 3.",
    )

# Литры = площадь стен × слои ÷ расход, округляем ВВЕРХ до 0.1 л
# (round(..., 6) убирает мелкие ошибки float, чтобы 3.0000000001 не стало 3.1)
paint_raw = walls_area * layers / consumption
paint_liters = math.ceil(round(paint_raw * 10, 6)) / 10

st.success(f"Нужно краски: **{paint_liters:.1f} л**")

with st.expander("Как считали"):
    st.latex(r"V = \frac{S_{\text{стен}} \cdot n}{r}")
    st.write("где n — количество слоёв, r — расход краски (м²/л).")
    st.write(f"V = {walls_area:.2f} × {layers} ÷ {consumption} = {paint_raw:.2f} л")
    st.write(f"Округляем вверх до 0.1 л: **{paint_liters:.1f} л**")

# ---------------------------------------------------------------------------
# 3. Обои
# ---------------------------------------------------------------------------
st.divider()
st.header("3. Обои")

c1, c2 = st.columns(2)
with c1:
    wp_width = st.number_input(
        "Ширина рулона обоев, м", min_value=0.1, value=0.53, step=0.01, format="%.2f",
        key="wp_width",
        help="Размеры рулона написаны на этикетке. Самые частые: 0.53 × 10 м и 1.06 × 10 м.",
    )
with c2:
    wp_length = st.number_input(
        "Длина рулона обоев, м", min_value=0.5, value=10.0, step=0.5, key="wp_length",
        help="Длина рулона написана на этикетке, обычно около 10 м.",
    )

# Периметр без проёмов = периметр − ширина всех дверей − ширина всех окон
# (упрощение: вычитаем только ширину проёмов)
doors_width_total = sum(w for w, h in door_sizes)
windows_width_total = sum(w for w, h in window_sizes)
wp_perimeter = max(perimeter - doors_width_total - windows_width_total, 0)
# Полос с одного рулона = ⌊длина рулона ÷ высота комнаты⌋
strips_per_roll = math.floor(round(wp_length / height, 6))

if height > wp_length or strips_per_roll == 0:
    st.error(
        "Высота комнаты больше длины рулона: из одного рулона нельзя "
        "получить ни одной полосы. Выберите рулон длиннее."
    )
else:
    # Полос нужно = ⌈периметр без проёмов ÷ ширина рулона⌉
    strips_needed = math.ceil(round(wp_perimeter / wp_width, 6))
    # Рулонов = ⌈полос нужно ÷ полос с рулона⌉
    rolls = math.ceil(strips_needed / strips_per_roll)

    st.success(f"Нужно рулонов обоев: **{rolls} шт.**")

    with st.expander("Как считали"):
        st.latex(r"N_{\text{полос}} = \left\lceil \frac{P'}{w} \right\rceil")
        st.latex(r"k = \left\lfloor \frac{L}{h} \right\rfloor")
        st.latex(r"N_{\text{рулонов}} = \left\lceil \frac{N_{\text{полос}}}{k} \right\rceil")
        st.write("где P' — периметр без проёмов, w — ширина рулона, L — длина рулона, h — высота комнаты.")
        st.write(
            f"Периметр без проёмов: {perimeter:.2f} − {doors_width_total:.2f} (двери) − "
            f"{windows_width_total:.2f} (окна) = {wp_perimeter:.2f} м"
        )
        st.write(f"Полос нужно: ⌈{wp_perimeter:.2f} ÷ {wp_width}⌉ = {strips_needed}")
        st.write(f"Полос с рулона: ⌊{wp_length} ÷ {height}⌋ = {strips_per_roll}")
        st.write(f"Рулонов: ⌈{strips_needed} ÷ {strips_per_roll}⌉ = **{rolls}**")

# ---------------------------------------------------------------------------
# 4. Плитка на пол
# ---------------------------------------------------------------------------
st.divider()
st.header("4. Плитка на пол")

c1, c2 = st.columns(2)
with c1:
    tile_l = st.number_input(
        "Длина плитки, см", min_value=1.0, value=30.0, step=1.0,
        help="Размер плитки написан на коробке. Частые размеры: 30×30, 40×40, 60×60 см.",
    )
with c2:
    tile_w = st.number_input("Ширина плитки, см", min_value=1.0, value=30.0, step=1.0)
tile_reserve = st.slider(
    "Запас на подрезку, %", min_value=0, max_value=20, value=10,
    help=(
        "Часть плиток придётся резать у стен, и некоторые могут разбиться. "
        "При укладке ровными рядами хватает 5–10%, при укладке по диагонали "
        "лучше 10–15%."
    ),
)

# Площадь одной плитки (м²) = (длина_см ÷ 100) × (ширина_см ÷ 100)
tile_area = (tile_l / 100) * (tile_w / 100)
# Количество = площадь пола ÷ площадь плитки × (1 + запас), округляем ВВЕРХ до целого
tiles_raw = floor_area / tile_area * (1 + tile_reserve / 100)
tiles_count = math.ceil(round(tiles_raw, 6))

st.success(f"Нужно плиток: **{tiles_count} шт.**")

with st.expander("Как считали"):
    st.latex(r"N = \frac{S_{\text{пола}}}{S_{\text{плитки}}} \cdot \left(1 + \frac{k}{100}\right)")
    st.write("где k — запас на подрезку (%).")
    st.write(f"Площадь одной плитки: {tile_l / 100} × {tile_w / 100} = {tile_area:.4f} м²")
    st.write(
        f"N = {floor_area:.2f} ÷ {tile_area:.4f} × (1 + {tile_reserve}/100) = {tiles_raw:.2f}"
    )
    st.write(f"Округляем вверх до целого: **{tiles_count} шт.**")

# ---------------------------------------------------------------------------
# 5. Линолеум
# ---------------------------------------------------------------------------
st.divider()
st.header("5. Линолеум")

c1, c2 = st.columns(2)
with c1:
    roll_width = st.selectbox(
        "Ширина рулона линолеума, м", [1.5, 2.0, 2.5, 3.0, 3.5, 4.0], index=3,
        help=(
            "Линолеум продаётся рулонами разной ширины. Чем шире рулон, тем меньше "
            "стыков. Лучше выбрать рулон, который не меньше короткой стороны комнаты."
        ),
    )
with c2:
    lino_reserve = st.slider(
        "Запас линолеума, %", min_value=0, max_value=15, value=5,
        help=(
            "Лишний материал на подрезку по краям, неровные стены и подгонку рисунка. "
            "Для обычной комнаты хватает 5%. Если комната сложной формы или рисунок "
            "на линолеуме крупный, берите 10–15%."
        ),
    )

short_side = min(length, width)   # короткая сторона комнаты
long_side = max(length, width)    # длинная сторона комнаты

if roll_width < short_side:
    # Рулон уже комнаты: нужен стык из двух полотен, длина удваивается
    # (упрощённо: берём два полотна; при очень узком рулоне их может понадобиться больше)
    st.warning(
        "Ширина рулона меньше короткой стороны комнаты: потребуется стык "
        "из двух полотен. Длина отреза посчитана как двойная."
    )
    has_seam = True
    # Длина = длинная сторона × (1 + запас) × 2
    lino_length_raw = long_side * (1 + lino_reserve / 100) * 2
else:
    has_seam = False
    # Длина = длинная сторона × (1 + запас)
    lino_length_raw = long_side * (1 + lino_reserve / 100)

# Округляем длину отреза ВВЕРХ до 0.1 м
lino_length = math.ceil(round(lino_length_raw * 10, 6)) / 10
# Площадь купленного отреза = длина × ширина рулона
lino_area = lino_length * roll_width

st.success(
    f"Длина отреза: **{lino_length:.1f} пог. м**  \n"
    f"Площадь отреза: **{lino_area:.2f} м²**"
)

with st.expander("Как считали"):
    if has_seam:
        st.latex(r"L = 2 \cdot b_{\text{длинная}} \cdot \left(1 + \frac{k}{100}\right)")
        st.write(
            f"L = 2 × {long_side} × (1 + {lino_reserve}/100) = {lino_length_raw:.2f} м"
        )
    else:
        st.latex(r"L = b_{\text{длинная}} \cdot \left(1 + \frac{k}{100}\right)")
        st.write(f"L = {long_side} × (1 + {lino_reserve}/100) = {lino_length_raw:.2f} м")
    st.write(f"Округляем вверх до 0.1 м: **{lino_length:.1f} м**")
    st.latex(r"S = L \cdot W_{\text{рулона}}")
    st.write(f"S = {lino_length:.1f} × {roll_width} = {lino_area:.2f} м²")

# ---------------------------------------------------------------------------
# Примечание
# ---------------------------------------------------------------------------
st.divider()
st.caption(
    "Примечание: все расчёты приблизительные. Перед покупкой материалов "
    "уточните размеры на месте и проконсультируйтесь с продавцом."
)

# ---------------------------------------------------------------------------
# Как запустить: в терминале, в папке с файлом, выполните
#     streamlit run app.py
# ---------------------------------------------------------------------------
