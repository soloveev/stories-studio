# slide-templates.md — копипастные шаблоны слайдов

Готовые HTML-снипеты для каждого паттерна. Бери отсюда — не пиши руками.

Подставляй:
- `{N0}` → номер `data-slide` (0-indexed): `0`, `1`, `2`, …
- `{N1}` → номер слайда (1-indexed): `1`, `2`, `3`, …
- `{TOTAL}` → общее число слайдов
- `{IMG_HINT}` → описание идеи картинки для комментария
- `{TEXT}` / `{TITLE}` / `{QUOTE}` → собственно содержимое
- `{BG}` — класс фона: `story-white`, `story-gray`, `story-black` (для цветного фона убери класс и поставь `style="background:#e9d5ff;"`)

---

## Быстрый старт нового поста

```bash
SKILL="<путь до скилла>/assets"     # каталог assets внутри stories-studio
DST="<папка поста>"                  # куда разворачиваем колоду

mkdir -p "$DST/images"
cp "$SKILL/template.html"    "$DST/stories.html"
cp "$SKILL/server.py"        "$DST/server.py"
cp "$SKILL/placeholder.svg"  "$DST/images/placeholder.svg"

cd "$DST" && python3 server.py 8089 &
open http://localhost:8089/stories.html
```

После этого:
1. Удали 4 демо-слайда из `stories.html` (это блоки `<!-- SLIDE N — ... -->` внутри `<div class="viewport">`).
2. Вместо них вставь нужное количество слайдов из шаблонов ниже.
3. Поправь `<title>` в `<head>`; префикс файлов экспорта по умолчанию `story-NN` менять не обязательно.

---

## Шаблон 1 — TITLE (первый слайд)

```html
<!-- SLIDE {N1} — TITLE: заголовок + первый абзац -->
<!-- IMG: {IMG_HINT} -->
<div class="story-wrap active" data-slide="{N0}">
  <span class="story-label">{N1} / {TOTAL}</span>
  <div class="story {BG}" id="story-{N1}">
    <div class="block">
      <div class="block-controls"><div class="move-btn" onclick="nudge(this,-1)">&#9650;</div><div class="drag-handle">&#10303;</div><div class="move-btn" onclick="nudge(this,1)">&#9660;</div></div>
      <div class="story-image-block small"><img src="images/placeholder.svg" alt=""></div>
    </div>
    <div class="block">
      <div class="block-controls"><div class="move-btn" onclick="nudge(this,-1)">&#9650;</div><div class="drag-handle">&#10303;</div><div class="move-btn" onclick="nudge(this,1)">&#9660;</div></div>
      <div class="story-title" contenteditable="true">{TITLE_LINE1}<br>{TITLE_LINE2}</div>
    </div>
    <div class="block">
      <div class="block-controls"><div class="move-btn" onclick="nudge(this,-1)">&#9650;</div><div class="drag-handle">&#10303;</div><div class="move-btn" onclick="nudge(this,1)">&#9660;</div></div>
      <div class="story-text" contenteditable="true">{FIRST_PARAGRAPH}</div>
    </div>
    <div class="spacer"></div>
    <div class="story-footer" contenteditable="true"><span class="footer-sig"></span></div>
  </div>
</div>
```

⚠️ Только у слайда 1 класс `story-wrap active` (он стартует видимым). У остальных — просто `story-wrap`.

---

## Шаблон 2 — BODY (рабочая лошадь, 60-70 % слайдов)

```html
<!-- SLIDE {N1} — BODY: {WHAT_ABOUT} -->
<!-- IMG: {IMG_HINT} -->
<div class="story-wrap" data-slide="{N0}">
  <span class="story-label">{N1} / {TOTAL}</span>
  <div class="story {BG}" id="story-{N1}">
    <div class="block">
      <div class="block-controls"><div class="move-btn" onclick="nudge(this,-1)">&#9650;</div><div class="drag-handle">&#10303;</div><div class="move-btn" onclick="nudge(this,1)">&#9660;</div></div>
      <div class="story-image-block small"><img src="images/placeholder.svg" alt=""></div>
    </div>
    <div class="block">
      <div class="block-controls"><div class="move-btn" onclick="nudge(this,-1)">&#9650;</div><div class="drag-handle">&#10303;</div><div class="move-btn" onclick="nudge(this,1)">&#9660;</div></div>
      <div class="story-text" contenteditable="true">{TEXT}</div>
    </div>
    <div class="spacer"></div>
    <div class="story-footer" contenteditable="true"><span class="footer-sig"></span></div>
  </div>
</div>
```

Если нужно два абзаца — продублируй `.block` с `.story-text`, между ними CSS даст 28 px отступ.

---

## Шаблон 3 — QUOTE (центральный тезис)

Для цитаты обычно полезно: маленькая картинка сверху, потом `spacer`, потом крупный текст по центру вертикально.

```html
<!-- SLIDE {N1} — QUOTE: {WHAT_ABOUT} -->
<!-- IMG: {IMG_HINT} -->
<div class="story-wrap" data-slide="{N0}">
  <span class="story-label">{N1} / {TOTAL}</span>
  <div class="story {BG}" id="story-{N1}">
    <div class="block">
      <div class="block-controls"><div class="move-btn" onclick="nudge(this,-1)">&#9650;</div><div class="drag-handle">&#10303;</div><div class="move-btn" onclick="nudge(this,1)">&#9660;</div></div>
      <div class="story-image-block small"><img src="images/placeholder.svg" alt=""></div>
    </div>
    <div class="spacer"></div>
    <div class="block">
      <div class="block-controls"><div class="move-btn" onclick="nudge(this,-1)">&#9650;</div><div class="drag-handle">&#10303;</div><div class="move-btn" onclick="nudge(this,1)">&#9660;</div></div>
      <div class="story-quote" contenteditable="true">{QUOTE}</div>
    </div>
    <div class="spacer"></div>
    <div class="story-footer" contenteditable="true"><span class="footer-sig"></span></div>
  </div>
</div>
```

Для акцентного цветного фона (лаванда / коралл / мята) **убери** класс `{BG}` и добавь `style="background:#e9d5ff;"` (или другой цвет) к `.story`.

Для чёрного фона — поставь `story-black` в `{BG}`.

---

## Шаблон 4 — QUOTE + tail (цитата + короткая приписка)

```html
<!-- SLIDE {N1} — QUOTE+TAIL: {WHAT_ABOUT} -->
<!-- IMG: {IMG_HINT} -->
<div class="story-wrap" data-slide="{N0}">
  <span class="story-label">{N1} / {TOTAL}</span>
  <div class="story {BG}" id="story-{N1}">
    <div class="block">
      <div class="block-controls"><div class="move-btn" onclick="nudge(this,-1)">&#9650;</div><div class="drag-handle">&#10303;</div><div class="move-btn" onclick="nudge(this,1)">&#9660;</div></div>
      <div class="story-image-block small"><img src="images/placeholder.svg" alt=""></div>
    </div>
    <div class="spacer"></div>
    <div class="block">
      <div class="block-controls"><div class="move-btn" onclick="nudge(this,-1)">&#9650;</div><div class="drag-handle">&#10303;</div><div class="move-btn" onclick="nudge(this,1)">&#9660;</div></div>
      <div class="story-quote" contenteditable="true">{QUOTE}</div>
    </div>
    <div class="block">
      <div class="block-controls"><div class="move-btn" onclick="nudge(this,-1)">&#9650;</div><div class="drag-handle">&#10303;</div><div class="move-btn" onclick="nudge(this,1)">&#9660;</div></div>
      <div class="story-text-sm" contenteditable="true">{TAIL_TEXT}</div>
    </div>
    <div class="spacer"></div>
    <div class="story-footer" contenteditable="true"><span class="footer-sig"></span></div>
  </div>
</div>
```

---

## Шаблон 5 — BULLETS (перечисление)

```html
<!-- SLIDE {N1} — BULLETS: {WHAT_ABOUT} -->
<!-- IMG: {IMG_HINT} -->
<div class="story-wrap" data-slide="{N0}">
  <span class="story-label">{N1} / {TOTAL}</span>
  <div class="story {BG}" id="story-{N1}">
    <div class="block">
      <div class="block-controls"><div class="move-btn" onclick="nudge(this,-1)">&#9650;</div><div class="drag-handle">&#10303;</div><div class="move-btn" onclick="nudge(this,1)">&#9660;</div></div>
      <div class="story-image-block small"><img src="images/placeholder.svg" alt=""></div>
    </div>
    <div class="block">
      <div class="block-controls"><div class="move-btn" onclick="nudge(this,-1)">&#9650;</div><div class="drag-handle">&#10303;</div><div class="move-btn" onclick="nudge(this,1)">&#9660;</div></div>
      <ul class="story-bullets" contenteditable="true">
        <li>{ITEM_1}</li>
        <li>{ITEM_2}</li>
        <li>{ITEM_3}</li>
      </ul>
    </div>
    <div class="spacer"></div>
    <div class="story-footer" contenteditable="true"><span class="footer-sig"></span></div>
  </div>
</div>
```

---

## Шаблон 6 — CLOSING (финальный слайд)

```html
<!-- SLIDE {N1} — CLOSING: {WHAT_ABOUT} -->
<!-- IMG: {IMG_HINT} -->
<div class="story-wrap" data-slide="{N0}">
  <span class="story-label">{N1} / {TOTAL}</span>
  <div class="story {BG}" id="story-{N1}">
    <div class="block">
      <div class="block-controls"><div class="move-btn" onclick="nudge(this,-1)">&#9650;</div><div class="drag-handle">&#10303;</div><div class="move-btn" onclick="nudge(this,1)">&#9660;</div></div>
      <div class="story-image-block small"><img src="images/placeholder.svg" alt=""></div>
    </div>
    <div class="block">
      <div class="block-controls"><div class="move-btn" onclick="nudge(this,-1)">&#9650;</div><div class="drag-handle">&#10303;</div><div class="move-btn" onclick="nudge(this,1)">&#9660;</div></div>
      <div class="story-text-sm" contenteditable="true">{CONCLUSION_LINE_1}</div>
    </div>
    <div class="block">
      <div class="block-controls"><div class="move-btn" onclick="nudge(this,-1)">&#9650;</div><div class="drag-handle">&#10303;</div><div class="move-btn" onclick="nudge(this,1)">&#9660;</div></div>
      <div class="story-text-sm" contenteditable="true">{CONCLUSION_LINE_2}</div>
    </div>
    <div class="spacer"></div>
    <div class="story-footer" contenteditable="true"><span class="footer-sig"></span></div>
  </div>
</div>
```

---

## Чек-лист сборки

После того как все слайды собраны:

- [ ] У слайда 1 класс `story-wrap active`, у остальных — просто `story-wrap`.
- [ ] `data-slide` идёт от `0`, `id="story-N"` — от `1`.
- [ ] `<span class="story-label">N1 / TOTAL</span>` — правильный для каждого слайда.
- [ ] Футер на каждом слайде — `<span class="footer-sig"></span>`, пустой (редактор сам подставит подпись из настройки). Без терма и без номера слайда.
- [ ] Под каждым слайдом — комментарий `<!-- IMG: … -->` с идеей картинки.
- [ ] **Текст совпадает с `source.md` посимвольно** (см. § Правило ноль в composition-rules.md).
- [ ] В `<head>` обновлён `<title>`.
- [ ] Сервер запущен на `localhost:8089`, страница открывается, навигация стрелками работает.

---

## Минимальный «скелет stories.html»

Если нужно собрать руками без копирования template.html (редко, но бывает) — структура такая:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <title>{POST_NAME} — Stories</title>
  <!-- CSS + JS (берётся из template.html, ~800 строк, не править) -->
</head>
<body>
  <div class="toolbar">…</div>                  <!-- из template.html -->
  <div class="viewport">
    <div class="nav-arrow left" onclick="go(-1)">&#8592;</div>
    <div class="nav-arrow right" onclick="go(1)">&#8594;</div>

    <!-- сюда вставить N слайдов из шаблонов выше -->

  </div>
  <div class="image-editor" id="image-editor">…</div>       <!-- из template.html -->
  <div class="text-size-editor" id="text-size-editor">…</div>  <!-- из template.html -->
  <div class="slide-counter" id="slide-counter"></div>
  <script>…</script>                                           <!-- из template.html -->
</body>
</html>
```

В 99 % случаев правильный путь — копировать `template.html` целиком и заменить только блок слайдов внутри `.viewport`.
