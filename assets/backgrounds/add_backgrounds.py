#!/usr/bin/env python3
"""Добавить свои фоны в галерею редактора (панель «Слайд» → «Картинка фона»).

    python3 add_backgrounds.py <папка или файлы…> [--group "Мои фоны"]

Каждая картинка ужимается до 1080 px по короткой стороне (JPEG q82) и кладётся в эту папку backgrounds/,
а в backgrounds.js добавляется строка { src, label, group, color } — подпись из имени файла, color — средний цвет
(он ставится цветом слайда под картинкой, по нему же редактор решает, белым или чёрным будет текст).
Повторный запуск с тем же файлом обновляет его строку, а не дублирует. Папку backgrounds/ копируют рядом с колодой.
"""
import json, re, sys
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
args, group = [], "Мои фоны"
it = iter(sys.argv[1:])
for a in it:
    if a == "--group":
        group = next(it)
    else:
        args.append(Path(a))
if not args:
    sys.exit(__doc__)
files = [f for a in args for f in (sorted(a.iterdir()) if a.is_dir() else [a])
         if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")]
js = HERE / "backgrounds.js"
items = []
if js.exists():
    m = re.search(r"window\.BACKGROUNDS\s*=\s*(\[.*\]);", js.read_text(encoding="utf-8"), re.S)
    items = json.loads(m.group(1)) if m else []
for f in files:
    im = Image.open(f).convert("RGB")
    k = 1080 / min(im.size)
    if k < 1:
        im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    name = re.sub(r"[^\w-]+", "-", f.stem.lower()).strip("-") + ".jpg"
    im.save(HERE / name, quality=82, optimize=True, progressive=True)
    r, g, b = im.resize((1, 1), Image.LANCZOS).getpixel((0, 0))
    entry = {"src": f"backgrounds/{name}", "label": f.stem.replace("-", " ").replace("_", " "),
             "group": group + (" 16:9" if im.width > im.height * 1.3 else ""), "color": f"#{r:02x}{g:02x}{b:02x}"}
    items = [x for x in items if x["src"] != entry["src"]] + [entry]
    print("+", name, entry["color"])
js.write_text("// Готовые фоны для панели «Слайд» редактора. Добавить свои: python3 add_backgrounds.py <папка>.\n"
              "// color — средний цвет: ставится цветом слайда под картинкой.\n"
              "window.BACKGROUNDS = " + json.dumps(items, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
print(len(items), "фонов в галерее")
