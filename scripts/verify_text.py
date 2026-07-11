#!/usr/bin/env python3
"""Посимвольная сверка текста слайдов stories.html с исходником поста.

Использование:
    python3 verify_text.py <stories.html> <post.md>

Печатает все расхождения (difflib opcodes) между текстом источника и текстом
слайдов. Ожидаемые расхождения: пробельные артефакты вокруг <b>/<i>/<br>,
маркеры буллетов и сознательно исправленные опечатки. Любая другая замена,
вставка или пропуск — баг раскладки: чинить.
"""
import difflib
import re
import sys


def slides_text(html: str) -> str:
    m = re.search(r'<!-- SLIDE 1.*?</div>\s*\n\s*\n</div>', html, re.S)
    if not m:
        sys.exit("Не найден блок слайдов (<!-- SLIDE 1 ... -->)")
    texts = re.findall(
        r'<(?:div|ul) class="story-(?:title|text|text-sm|quote|bullets)[^"]*"'
        r' contenteditable="true"[^>]*>(.*?)</(?:div|ul)>',
        m.group(0), re.S)
    joined = ' '.join(texts)
    joined = re.sub(r'<li>', ' • ', joined)
    joined = re.sub(r'<[^>]+>', ' ', joined)
    return normalize(joined)


def normalize(s: str) -> str:
    s = re.sub(r'\*\*|\*|_', '', s)
    s = s.replace('•', ' ')
    return re.sub(r'\s+', ' ', s).strip()


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    html = open(sys.argv[1], encoding='utf-8').read()
    source = normalize(open(sys.argv[2], encoding='utf-8').read())
    slides = slides_text(html)

    diffs = 0
    sm = difflib.SequenceMatcher(None, source, slides)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        diffs += 1
        print(f"{tag}: SRC[{source[max(0, i1 - 25):i2 + 25]!r}] -> "
              f"SLIDES[{slides[max(0, j1 - 25):j2 + 25]!r}]")
    print(f"--- {diffs} расхождений "
          f"(допустимы только пробельные артефакты и исправленные опечатки) ---")


if __name__ == '__main__':
    main()
