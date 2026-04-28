"""
EPUB generator for the NovelDownloader web backend.
Produces well-structured EPUB 3 files with embedded CSS styling.
"""

from __future__ import annotations

import logging
import uuid
from typing import Optional

from ebooklib import epub

logger = logging.getLogger(__name__)

# ─── Embedded CSS for the EPUB ────────────────────────────────────────────────

EPUB_CSS = """
@charset "UTF-8";

body {
    font-family: "Georgia", "Times New Roman", serif;
    line-height: 1.8;
    color: #1a1a2e;
    margin: 1em;
}

h1 {
    font-size: 2em;
    text-align: center;
    color: #4a3728;
    margin: 1.5em 0 0.5em;
    border-bottom: 2px solid #c4a882;
    padding-bottom: 0.4em;
}

h2 {
    font-size: 1.4em;
    text-align: center;
    color: #4a3728;
    margin: 1em 0 0.8em;
}

h3 {
    font-size: 1.1em;
    color: #6b5b4e;
    margin: 0.8em 0 0.4em;
}

p {
    text-align: justify;
    text-indent: 1.5em;
    margin: 0.3em 0;
}

p.first {
    text-indent: 0;
}

p.meta {
    text-align: center;
    text-indent: 0;
    color: #6b5b4e;
    font-style: italic;
    margin: 0.2em 0;
}

p.synopsis {
    text-indent: 0;
    font-style: italic;
    margin: 0.5em 2em;
    color: #333;
}

.genre-list {
    text-align: center;
    margin: 0.6em 0;
}

.genre {
    display: inline-block;
    background: #f0ebe3;
    color: #4a3728;
    padding: 0.15em 0.6em;
    border-radius: 0.3em;
    margin: 0.15em 0.2em;
    font-size: 0.85em;
}

hr {
    border: none;
    border-top: 1px solid #c4a882;
    margin: 1.5em 2em;
}

.chapter-number {
    text-align: center;
    font-size: 0.85em;
    color: #c4a882;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.2em;
}
"""


def generate_epub(
    output_path: str,
    novel_title: str,
    author: str,
    description: str,
    genres: list[str],
    chapters: list,
    cover_url: Optional[str] = None,
    progress_callback=None,
) -> str:
    """Generate an EPUB file from novel content.

    Parameters match ``generate_pdf`` so the two generators are
    interchangeable from the caller's perspective.
    """

    def log(message: str):
        logger.info(message)
        if progress_callback:
            progress_callback(message)

    book = epub.EpubBook()

    uid = uuid.uuid4().hex
    book.set_identifier(f"noveldownloader-{uid}")
    book.set_title(novel_title)
    book.set_language("en")
    book.add_author(author or "Unknown")

    css_item = epub.EpubItem(
        uid="style",
        file_name="style/default.css",
        media_type="text/css",
        content=EPUB_CSS.encode("utf-8"),
    )
    book.add_item(css_item)

    title_html = _build_title_page(novel_title, author, description, genres)
    title_chapter = epub.EpubHtml(
        title="Portada",
        file_name="title.xhtml",
        lang="en",
    )
    title_chapter.content = title_html.encode("utf-8")
    title_chapter.add_item(css_item)
    book.add_item(title_chapter)

    epub_chapters: list[epub.EpubHtml] = [title_chapter]
    toc_entries: list[epub.EpubHtml] = []

    total = len(chapters)
    for index, chapter in enumerate(chapters, start=1):
        log(f"Generando capítulo EPUB {index}/{total}")

        safe_name = f"chapter_{index:04d}.xhtml"
        epub_ch = epub.EpubHtml(
            title=chapter.title,
            file_name=safe_name,
            lang="en",
        )

        body_html = _build_chapter_html(chapter, index)
        epub_ch.content = body_html.encode("utf-8")
        epub_ch.add_item(css_item)
        book.add_item(epub_ch)
        epub_chapters.append(epub_ch)
        toc_entries.append(epub_ch)

    book.toc = toc_entries
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav"] + epub_chapters

    log("Escribiendo archivo EPUB...")
    epub.write_epub(output_path, book, {})
    log(f"EPUB generado: {output_path}")
    return output_path


# ─── HTML builders ────────────────────────────────────────────────────────────

def _esc(text: str) -> str:
    """Minimal HTML escaping."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _build_title_page(
    title: str, author: str, description: str, genres: list[str]
) -> str:
    parts = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<html xmlns="http://www.w3.org/1999/xhtml">',
        "<head><title>Portada</title></head>",
        "<body>",
        f"<h1>{_esc(title)}</h1>",
    ]

    if author:
        parts.append(f'<p class="meta">Autor: {_esc(author)}</p>')

    if genres:
        chips = "".join(f'<span class="genre">{_esc(g)}</span>' for g in genres)
        parts.append(f'<div class="genre-list">{chips}</div>')

    if description:
        parts.append("<hr/>")
        parts.append('<h3 style="text-align:center;">Sinopsis</h3>')
        for line in description.split("\n"):
            line = line.strip()
            if line:
                parts.append(f'<p class="synopsis">{_esc(line)}</p>')

    parts.extend(["</body>", "</html>"])
    return "\n".join(parts)


def _build_chapter_html(chapter, index: int) -> str:
    parts = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<html xmlns="http://www.w3.org/1999/xhtml">',
        f"<head><title>{_esc(chapter.title)}</title></head>",
        "<body>",
        f'<div class="chapter-number">Capítulo {index}</div>',
        f"<h2>{_esc(chapter.title)}</h2>",
    ]

    for i, paragraph in enumerate(chapter.paragraphs):
        css_class = ' class="first"' if i == 0 else ""
        parts.append(f"<p{css_class}>{_esc(paragraph)}</p>")

    parts.extend(["</body>", "</html>"])
    return "\n".join(parts)
