"""Генерирует чёрно-белый скетч «Ёж за ноутбуком» -> images/hedgehog.svg

Запуск:  python tools/generate_hedgehog.py
Меняйте SEED, чтобы получить другой рисунок иголок.
"""
import math
import random
from pathlib import Path

SEED = 7
random.seed(SEED)

W, H = 640, 480
INK = "#1a1a1a"

# Тело ежа — эллипс, голова смотрит вправо (к ноутбуку)
CX, CY, RX, RY = 210, 330, 140, 108
T_START, T_END = math.radians(44), math.radians(214)


def ell(t, r=1.0):
    return CX + RX * r * math.cos(t), CY - RY * r * math.sin(t)


def f(x, y):
    return f"{x:.1f},{y:.1f}"


def j(v=1.0):
    return random.uniform(-v, v)


parts = []
add = parts.append

# ---------- Иголки: внутренние штрихи (штриховка-объём) ----------
spines = []
for _ in range(900):
    t = random.uniform(T_START, T_END)
    # больше штрихов в «теневой» (нижне-левой) части
    if t < math.radians(120) and random.random() < 0.35:
        continue
    r = math.sqrt(random.uniform(0.02, 0.9))
    x0, y0 = ell(t, r)
    if y0 > 404:
        continue
    length = random.uniform(16, 30) * (0.7 + 0.4 * r)
    a = t + math.radians(random.uniform(18, 34))  # иголки зачёсаны назад
    dx, dy = math.cos(a) * length, -math.sin(a) * length
    # направление «наружу» от центра тела + стрела назад
    ox, oy = math.cos(t), -math.sin(t)
    x1 = x0 + 0.55 * dx + 0.45 * ox * length
    y1 = y0 + 0.55 * dy + 0.45 * oy * length
    w = random.uniform(0.6, 1.5)
    op = random.uniform(0.45, 0.95)
    spines.append(
        f'<path d="M{f(x0, y0)} L{f(x1, y1)}" stroke-width="{w:.2f}" opacity="{op:.2f}"/>'
    )
add('<g id="spines-inner" stroke="%s" stroke-linecap="round" fill="none">' % INK)
parts.extend(spines)
add("</g>")

# ---------- Иголки: зубчатый контур (2 прохода для эффекта карандаша) ----------
for pass_no, (sw, op, jit) in enumerate([(1.9, 0.95, 1.2), (1.0, 0.6, 2.4)]):
    pts = []
    n = 40
    step = (T_END - T_START) / n
    for i in range(n + 1):
        t = T_START + i * step
        pts.append(ell(t + j(0.01), 0.95 + j(0.015)))
        if i < n:
            tip_r = random.uniform(1.16, 1.28)
            pts.append(ell(t + step * 0.85 + j(0.02), tip_r))
    d = "M" + " L".join(f(x + j(jit), y + j(jit)) for x, y in pts)
    add(
        f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{sw}" '
        f'stroke-linejoin="round" stroke-linecap="round" opacity="{op}"/>'
    )

# ---------- Мордочка и грудка (белая заливка поверх иголок) ----------
face = (
    "M300,250 C330,258 350,284 362,304 C370,316 382,320 385,328 "
    "C386,338 371,342 357,344 C341,346 327,353 319,363 "
    "C312,373 311,388 313,404 L250,404 "
    "C255,370 262,330 270,300 C278,276 288,258 300,250 Z"
)
add(f'<path d="{face}" fill="#fff" stroke="none"/>')
face_outline = (
    "M300,250 C330,258 350,284 362,304 C370,316 382,320 385,328 "
    "C386,338 371,342 357,344 C341,346 327,353 319,363 "
    "C312,373 311,388 313,402"
)
add(
    f'<path d="{face_outline}" fill="none" stroke="{INK}" stroke-width="2.3" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
)
add(
    f'<path d="{face_outline}" fill="none" stroke="{INK}" stroke-width="0.9" '
    'stroke-linecap="round" opacity="0.5" transform="translate(1.2,-1)"/>'
)

# мех на границе мордочки и иголок
fur = []
for i in range(16):
    k = i / 15
    # точка на внутренней границе (приблизительно по кривой)
    x = 300 - 50 * k + 6 * math.sin(k * math.pi) * -1
    y = 252 + 150 * k
    x += -8 * math.sin(k * math.pi)
    L = random.uniform(7, 13)
    a = math.radians(random.uniform(150, 200))
    fur.append(
        f'<path d="M{f(x + 4, y)} L{f(x + 4 + math.cos(a) * L, y - math.sin(a) * L)}" '
        f'stroke-width="{random.uniform(0.8, 1.4):.2f}"/>'
    )
add('<g stroke="%s" stroke-linecap="round" opacity="0.85">' % INK)
parts.extend(fur)
add("</g>")

# ухо
add(
    f'<path d="M286,266 C282,250 300,242 309,256" fill="#fff" stroke="{INK}" '
    'stroke-width="2" stroke-linecap="round"/>'
)
add(f'<path d="M292,262 C292,254 300,251 304,257" fill="none" stroke="{INK}" stroke-width="0.9"/>')

# глаз
add(f'<ellipse cx="338" cy="298" rx="5.6" ry="7" fill="{INK}"/>')
add('<circle cx="340" cy="295" r="1.9" fill="#fff"/>')
add(f'<path d="M329,286 C334,282 341,282 346,285" fill="none" stroke="{INK}" '
    'stroke-width="1.4" stroke-linecap="round"/>')

# нос
add(f'<ellipse cx="385" cy="329" rx="7" ry="6" fill="{INK}"/>')
add('<ellipse cx="383" cy="326.5" rx="2.2" ry="1.4" fill="#fff"/>')

# рот и щёчка
add(f'<path d="M378,337 C376,344 369,347 362,345" fill="none" stroke="{INK}" '
    'stroke-width="1.5" stroke-linecap="round"/>')
blush = []
for i in range(4):
    x = 340 + i * 4
    blush.append(f'<path d="M{x},{326 + i * 0.5} l5,-6" stroke-width="0.9"/>')
add('<g stroke="%s" stroke-linecap="round" opacity="0.6">' % INK)
parts.extend(blush)
add("</g>")

# усы
add('<g stroke="%s" stroke-width="0.8" stroke-linecap="round" fill="none" opacity="0.75">' % INK)
add('<path d="M372,322 C385,312 396,309 408,309"/>')
add('<path d="M374,326 C388,320 400,320 410,322"/>')
add("</g>")

# штриховка грудки
add('<g stroke="%s" stroke-width="0.8" stroke-linecap="round" fill="none" opacity="0.45">' % INK)
for i in range(6):
    y = 366 + i * 6
    add(f'<path d="M{296 + i},{y} C{302 + i},{y - 3} {306 + i},{y - 2} {309},{y + 1}"/>')
add("</g>")

# ---------- Ноутбук ----------
# крышка (вид сзади-сбоку, экран повёрнут к ежу)
lid = "M452,398 L490,388 L528,242 L486,252 Z"
add(f'<path d="{lid}" fill="#fff" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>')
add(f'<path d="{lid}" fill="none" stroke="{INK}" stroke-width="0.9" opacity="0.5" '
    'transform="translate(-1.2,1)"/>')
# толщина крышки
add(f'<path d="M486,252 L481,255 L447,399 L452,398" fill="none" stroke="{INK}" stroke-width="1.6" '
    'stroke-linejoin="round"/>')
# штриховка на крышке
add('<clipPath id="lidclip"><path d="%s"/></clipPath>' % lid)
add('<g clip-path="url(#lidclip)" stroke="%s" stroke-width="0.8" opacity="0.4">' % INK)
for i in range(-10, 30):
    x = 440 + i * 4.5
    add(f'<path d="M{x},400 L{x + 70},240"/>')
add("</g>")
# логотип — сердечко
add(f'<path d="M496,318 c-3,-6 -11,-3 -8,3 c1.5,3 8,8 8,8 c0,0 6.5,-5 8,-8 c3,-6 -5,-9 -8,-3 z" '
    f'fill="#fff" stroke="{INK}" stroke-width="1.4"/>')

# основание / клавиатура
add(f'<path d="M336,401 L454,401 L490,390 L366,390 Z" fill="#fff" stroke="{INK}" '
    'stroke-width="2" stroke-linejoin="round"/>')
add(f'<path d="M336,401 L336,404 L454,404 L490,393 L490,390" fill="none" stroke="{INK}" stroke-width="1.4"/>')
# клавиши
add('<g stroke="%s" stroke-width="0.7" opacity="0.55">' % INK)
for i in range(9):
    x = 372 + i * 11
    add(f'<path d="M{x},392.5 l-4,6"/>')
add('<path d="M362,395.5 L470,395.5"/>')
add("</g>")

# свет от экрана
add('<g stroke="%s" stroke-width="1" stroke-linecap="round" stroke-dasharray="2 6" opacity="0.5">' % INK)
add('<path d="M470,290 L410,292"/>')
add('<path d="M466,310 L414,322"/>')
add('<path d="M475,268 L420,262"/>')
add("</g>")

# ---------- Лапки ----------
arm = "M309,357 C327,363 343,373 356,386"
arm2 = "M312,378 C324,384 335,390 344,395"
add(f'<path d="M309,357 C327,363 343,373 356,386 L344,395 C335,390 324,384 312,378 Z" fill="#fff"/>')
for d in (arm, arm2):
    add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>')
# лапка на клавиатуре
add(f'<path d="M343,394 C346,385 358,382 364,389 C366,393 362,395 356,395" fill="#fff" '
    f'stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>')
add('<g stroke="%s" stroke-width="1" stroke-linecap="round">' % INK)
add('<path d="M352,393 l1,-3"/><path d="M357,393 l1.5,-3"/>')
add("</g>")
# вторая (дальняя) лапка
add(f'<path d="M370,391 C372,385 381,384 384,389" fill="#fff" stroke="{INK}" '
    'stroke-width="1.5" stroke-linecap="round"/>')

# ---------- Кружка с паром ----------
add(f'<path d="M548,356 L548,394 C548,400 580,400 580,394 L580,356" fill="#fff" stroke="{INK}" '
    'stroke-width="2" stroke-linejoin="round"/>')
add(f'<ellipse cx="564" cy="356" rx="16" ry="4" fill="#fff" stroke="{INK}" stroke-width="1.8"/>')
add(f'<path d="M580,364 C594,362 594,384 580,384" fill="none" stroke="{INK}" stroke-width="2"/>')
add('<g stroke="%s" stroke-width="0.8" opacity="0.45">' % INK)
for i in range(7):
    x = 551 + i * 4
    add(f'<path d="M{x},372 l6,-12"/>' if x < 575 else "")
add("</g>")
add('<g fill="none" stroke="%s" stroke-width="1.4" stroke-linecap="round" opacity="0.7">' % INK)
add('<path d="M558,346 c-6,-8 6,-12 0,-22"/>')
add('<path d="M570,344 c-6,-8 6,-12 0,-22"/>')
add("</g>")

# ---------- Стол ----------
add(f'<rect x="20" y="403" width="600" height="77" fill="#fff"/>')
add(f'<path d="M24,403 L616,402" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>')
add(f'<path d="M30,405 L612,405.5" stroke="{INK}" stroke-width="0.9" opacity="0.5"/>')
add(f'<path d="M26,420 L614,419" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>')
add(f'<path d="M24,403 L26,420 M616,402 L614,419" stroke="{INK}" stroke-width="1.6"/>')
add('<g stroke="%s" stroke-width="0.8" opacity="0.35">' % INK)
for i in range(60):
    x = 30 + i * 9.8
    add(f'<path d="M{x:.1f},418 l8,-12"/>')
add("</g>")
# тени на столе
add('<g stroke="%s" stroke-width="0.9" stroke-linecap="round" opacity="0.5">' % INK)
add('<path d="M70,409 L330,409"/><path d="M110,413 L300,413"/>')
add('<path d="M340,409 L470,409"/><path d="M546,409 L586,409"/>')
add("</g>")

# ---------- Сборка ----------
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="10 170 620 260" role="img" aria-labelledby="t">
  <title id="t">Ёж за ноутбуком — карандашный скетч</title>
  <defs>
    <filter id="pencil" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="{SEED}" result="noise"/>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="2.6" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
  </defs>
  <g filter="url(#pencil)">
    {chr(10).join("    " + p for p in parts if p).strip()}
  </g>
</svg>
"""

out = Path(__file__).resolve().parent.parent / "images" / "hedgehog.svg"
out.write_text(svg, encoding="utf-8")
print(f"saved {out}")
