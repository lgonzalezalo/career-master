#!/usr/bin/env python3
"""Render a CV or letter written in Markdown to an A4 PDF.

Usage:
    python render.py input.md output.pdf [--css cv.css] [--title "Name - CV"]

Pipeline: Markdown -> HTML -> PDF (Chromium via Playwright).

Markdown conversion: pandoc if installed, else python-markdown, else a small built-in converter
that covers the CV template (so the printable-HTML fallback always works).

Exit codes:
    0  PDF written (prints the absolute path and the page count)
    1  input or conversion error (details printed)
    2  no PDF engine available: an HTML file is left next to the output so the
       user can open it in a browser and print it to PDF (A4)

Notes:
- pandoc runs with subscript, superscript and citation syntax disabled so that
  approximations such as "~12%" and handles such as "@name" are kept literally.
- HTML hooks (<p class="headline">, <span class="date">...) must contain plain text,
  not Markdown, so both pandoc and the python-markdown fallback render them the same.
"""
import argparse
import html as html_lib
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
PANDOC_FORMAT = "markdown-subscript-superscript-citations"


def builtin_md_to_html(text: str) -> str:
    """Minimal converter for the CV template: headings, '- ' lists, **bold**, [links](url),
    paragraphs and raw HTML lines. Used when neither pandoc nor python-markdown is available."""
    def inline(s: str) -> str:
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)

    out, para, in_list = [], [], False

    def flush():
        nonlocal para
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para = []

    for raw in text.splitlines():
        line = raw.rstrip()
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if not line.strip() or m or line.lstrip().startswith("<") or line.startswith("- "):
            flush()
        if in_list and not line.startswith("- "):
            out.append("</ul>")
            in_list = False
        if not line.strip():
            continue
        if m:
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
        elif line.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(line[2:])}</li>")
        elif line.lstrip().startswith("<"):
            out.append(line)
        else:
            para.append(line.strip())
    flush()
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def md_to_html(md_path: pathlib.Path) -> tuple[str, str]:
    """Return (html, engine)."""
    text = md_path.read_text(encoding="utf-8")
    force_builtin = os.environ.get("RENDER_FORCE_BUILTIN") == "1"
    if shutil.which("pandoc") and not force_builtin:
        try:
            return subprocess.run(
                ["pandoc", str(md_path), "-f", PANDOC_FORMAT, "-t", "html"],
                check=True, capture_output=True, text=True,
            ).stdout, "pandoc"
        except subprocess.CalledProcessError as e:
            sys.stderr.write(f"pandoc failed:\n{e.stderr}\n")
            sys.exit(1)
    if not force_builtin:
        try:
            import markdown  # type: ignore
            return markdown.markdown(text, extensions=["extra"]), "python-markdown"
        except ImportError:
            pass
    return builtin_md_to_html(text), "builtin"


def count_pages(pdf_path: pathlib.Path) -> int:
    try:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            from pypdf import PdfReader  # type: ignore
            return len(PdfReader(str(pdf_path)).pages)
    except Exception:
        data = pdf_path.read_bytes()
        return len(re.findall(rb"/Type\s*/Page(?!s)", data))


def fallback(html_doc: str, out_pdf: pathlib.Path, reason: str) -> None:
    html_out = out_pdf.with_name(out_pdf.stem + ".print.html")
    html_out.write_text(html_doc, encoding="utf-8")
    sys.stderr.write(
        f"No PDF created ({reason}).\n"
        f"Open {html_out.resolve()} in a browser and print it to PDF (A4, default margins).\n"
    )
    sys.exit(2)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--css", default=str(HERE / "cv.css"))
    ap.add_argument("--title", default=None)
    args = ap.parse_args()

    md_path = pathlib.Path(args.input)
    out_pdf = pathlib.Path(args.output)
    if not md_path.is_file():
        sys.stderr.write(f"Input not found: {md_path}\n")
        sys.exit(1)
    if out_pdf.suffix.lower() != ".pdf":
        sys.stderr.write("The output file must end in .pdf\n")
        sys.exit(1)
    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    css = pathlib.Path(args.css).read_text(encoding="utf-8")
    body, _engine = md_to_html(md_path)
    title = html_lib.escape(args.title or md_path.stem)
    html_doc = (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<title>{title}</title><style>{css}</style></head><body>{body}</body></html>"
    )

    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except ImportError:
        fallback(html_doc, out_pdf, "Playwright is not installed")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_html = pathlib.Path(tmp) / "render.html"
        tmp_html.write_text(html_doc, encoding="utf-8")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                try:
                    page = browser.new_page()
                    page.goto(tmp_html.as_uri())
                    page.pdf(path=str(out_pdf), format="A4", print_background=True,
                             prefer_css_page_size=True)
                finally:
                    browser.close()
        except Exception as e:  # browser missing, sandbox errors, etc.
            fallback(html_doc, out_pdf, f"Chromium could not run: {e.__class__.__name__}")

    pages = count_pages(out_pdf)
    print(f"PDF written to {out_pdf.resolve()} ({pages} page{'s' if pages != 1 else ''})")


if __name__ == "__main__":
    main()
