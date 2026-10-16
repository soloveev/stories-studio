#!/usr/bin/env python3
"""Пересадить сохранённую колоду в свежий редактор: слайды и стили колоды — из старого файла, код редактора — из template.html.

    python3 tools/upgrade_deck.py <старый.html> <новый.html> [шаблон=assets/template.html скилла]

Зачем: редактор живёт внутри каждого файла колоды. Когда в template.html появляются новые функции или чинятся баги,
сохранённая автором колода остаётся со старым кодом. Скрипт берёт из старого файла всё, что сделал автор
и сборка колоды, и вставляет в новый шаблон:
  • слайды — всё содержимое <div class="viewport"> (картинки data-URL, тексты, выделения, сдвиги, состояние картинок);
  • CSS колоды — от «/* ===== Колода 4:5 (deck4x5.py) =====» до «.story-white» (если есть);
  • ссылки на шрифты и стили после </style> (например fonts/fonts-v3.css);
  • <title>, класс <body> (формат), формат по умолчанию и префикс имён экспорта.
Старый файл не меняется. Новый проверяется: число слайдов и картинок совпадает.
"""
import re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
old_p, new_p = Path(sys.argv[1]), Path(sys.argv[2])
tpl_p = Path(sys.argv[3]) if len(sys.argv) > 3 else HERE.parent / "assets" / "template.html"
if old_p.resolve() == new_p.resolve():
    sys.exit("новый файл должен отличаться от старого — старый остаётся как резерв")
old, tpl = old_p.read_text(encoding="utf-8"), tpl_p.read_text(encoding="utf-8")


def segment(text, start, end, what):
    i = text.find(start)
    j = text.find(end, i + 1)
    if i < 0 or j < 0:
        sys.exit(f"не найден {what}: «{start[:40]}» … «{end[:40]}»")
    return i, j


# 1. слайды: содержимое .viewport (до панелей редактора — у старых шаблонов «Image Editor Panel», у новых — спрайт иконок)
END_OLD = "<!-- Image Editor Panel -->" if "<!-- Image Editor Panel -->" in old else "<!-- Иконки интерфейса"
END_NEW = "<!-- Иконки интерфейса" if "<!-- Иконки интерфейса" in tpl else "<!-- Image Editor Panel -->"
i, j = segment(old, '<div class="viewport">', END_OLD, "блок слайдов в старом файле")
slides = old[i:j]
a, b = segment(tpl, '<div class="viewport">', END_NEW, "блок слайдов в шаблоне")
out = tpl[:a] + slides + tpl[b:]

# 2. CSS колоды
MARK = "  /* ===== Колода 4:5 (deck4x5.py) ===== */"
if MARK in old:
    i = old.index(MARK)
    j = old.index("  .story-white { background: #fff; }", i)
    deck_css = old[i:j]
    anchor = "  .story-white { background: #fff; }"
    assert out.count(anchor) == 1, "в шаблоне не найдено правило .story-white"
    out = out.replace(anchor, deck_css + anchor, 1)

# 3. ссылки после </style> (шрифты колоды)
m = re.search(r"</style>\s*(.*?)</head>", old, re.S)
extra = m.group(1).strip() if m else ""
if extra:
    out = out.replace("</style>\n</head>", "</style>\n" + extra + "\n</head>", 1)

# 4. title, класс body, формат, префикс экспорта
t = re.search(r"<title>.*?</title>", old, re.S)
out = re.sub(r"<title>.*?</title>", lambda _: t.group(0), out, count=1)
body = re.search(r"<body[^>]*>", old).group(0)
out = re.sub(r"<body[^>]*>", lambda _: body, out, count=1)
fmt = re.search(r"let currentFormat = FORMATS\.(\w+);", old)
if fmt:
    out = re.sub(r"let currentFormat = FORMATS\.\w+;", f"let currentFormat = FORMATS.{fmt.group(1)};", out, count=1)
    for k in ("story", "post", "wide"):
        out = re.sub(rf'class="fmt-btn(?: active)?" data-fmt="{k}"',
                     f'class="fmt-btn{" active" if k == fmt.group(1) else ""}" data-fmt="{k}"', out, count=1)
pre = re.search(r"dl\(data, `([^`$]*)\$\{", old)
if pre:
    out = out.replace("dl(data, `story-", "dl(data, `" + pre.group(1))

# 5. проверка
n_old, n_new = old.count('class="story-wrap'), out.count('class="story-wrap')
img_old, img_new = len(re.findall(r"<img\b", slides)), len(re.findall(r"<img\b", out[out.index('<div class="viewport">'):]))
if n_old != n_new or img_old > img_new:
    sys.exit(f"сверка не сошлась: слайдов {n_old} → {n_new}, картинок {img_old} → {img_new}")
new_p.write_text(out, encoding="utf-8")
print(f"{new_p.name}: {n_new} слайдов, {img_old} картинок, редактор из {tpl_p.name}")
