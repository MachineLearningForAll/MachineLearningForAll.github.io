#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import subprocess
from pathlib import Path
from datetime import date
from typing import Union, Dict, Tuple, Iterator

# Optional imports (keep if you use them elsewhere)
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import tempfile
from pdf2image import convert_from_path

PathLike = Union[str, Path]

# --- LaTeX + Markdown safety wrappers ---
RAW_OPEN  = "{% raw %}"
RAW_CLOSE = "{% endraw %}"

# Match fenced code blocks ```...``` (any language) and existing raw blocks.
FENCE_OR_RAW_RE = re.compile(r"(```.*?```|{% raw %}.*?{% endraw %})", flags=re.DOTALL)

# Display math: $$...$$ (can be multiline)
DISPLAY_MATH_RE = re.compile(r"\$\$(.+?)\$\$", flags=re.DOTALL)

# Inline math: $...$ (but not $$...$$)
INLINE_MATH_RE = re.compile(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", flags=re.DOTALL)

BASE_IMAGE_URL = "https://AaltoDictionaryofML.github.io/images/"


def _wrap_math_segment(segment: str) -> str:
    """
    Wrap only math tokens ($...$ or $$...$$) that contain {{ or }} using {% raw %}...{% endraw %}.
    No extra whitespace/newlines are inserted; we wrap ONLY the math token itself.
    """

    def wrap_if_liquid(match: re.Match) -> str:
        full  = match.group(0)  # full $...$ or $$...$$ token
        inner = match.group(1)  # inside delimiters
        if "{{" in inner or "}}" in inner:
            return f"{RAW_OPEN}{full}{RAW_CLOSE}"
        return full

    segment = DISPLAY_MATH_RE.sub(wrap_if_liquid, segment)
    segment = INLINE_MATH_RE.sub(wrap_if_liquid, segment)
    return segment


def fix_latex_in_text(md_text: str) -> str:
    """
    Process a Markdown string so that ONLY LaTeX math tokens containing '{{' or '}}'
    are wrapped with {% raw %}...{% endraw %}.
    - Idempotent for code fences and existing raw blocks.
    - No extra line breaks introduced.
    """
    parts = FENCE_OR_RAW_RE.split(md_text)  # keep delimiters as separate parts
    fixed_parts = []
    for part in parts:
        if FENCE_OR_RAW_RE.fullmatch(part or ""):
            fixed_parts.append(part)  # leave fences/raw unchanged
        else:
            fixed_parts.append(_wrap_math_segment(part))
    return "".join(fixed_parts)


def extract_tikz_from_entry(entry_text: str) -> str | None:
    """
    Try to extract a TikZ picture from the entry text.
    Returns TikZ code if found, otherwise None.
    """
    match = re.search(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', entry_text, re.DOTALL)
    if match:
        return match.group(0)

    # Fallback for custom {tikzpicture} ... {tikzpicture} style
    match = re.search(r'\{tikzpicture\}.*?\{tikzpicture\}', entry_text, re.DOTALL)
    if match:
        tikz_inner = match.group(0)[13:-13].strip()
        return f"\\begin{{tikzpicture}}\n{tikz_inner}\n\\end{{tikzpicture}}"

    return None


def replace_tikz_with_includegraphics(description: str, image_path: str) -> str:
    """
    Replace the TikZ block in the description with a single \includegraphics command.
    """
    include_cmd = fr"\\includegraphics[width=0.8\\linewidth]{{{image_path}}}"
    return re.sub(
        r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',
        include_cmd,
        description,
        count=1,
        flags=re.DOTALL
    )


def compile_tikz_to_png(tikz_code: str, filename: str = "tikz_figure", output_dir: str = "../images") -> None:
    """
    Compile TikZ -> PDF via pdflatex, then convert PDF -> PNG via ImageMagick 'convert'.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_png_path = os.path.join(output_dir, f"{filename}.png")

    latex_code = f"""
\\documentclass[tikz]{{standalone}}
\\usepackage{{tikz}}
\\usetikzlibrary{{fit}}
\\usepackage[dvipsnames]{{xcolor}}
\\usetikzlibrary{{positioning, arrows.meta, calc, decorations.pathreplacing}}
\\definecolor{{lightblue}}{{RGB}}{{173, 216, 230}}
\\begin{{document}}
{tikz_code}
\\end{{document}}
""".strip() + "\n"

    tex_path = "figure.tex"
    pdf_path = "figure.pdf"

    Path(tex_path).write_text(latex_code, encoding="utf-8")

    subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_path], check=False)

    subprocess.run(
        ["convert", "-density", "300", pdf_path, "-quality", "90", output_png_path],
        check=False
    )

    print(f"✅ Saved PNG to: {output_png_path}")


def generate_texfile_with_image(term: str, description: str, image_path: str | None = None, output_dir: str = "../") -> None:
    """
    Generate a LaTeX file containing the full glossary description.
    If image_path is provided, replace the TikZ block with \\includegraphics.
    """
    tex_output_path = Path(output_dir) / f"{term}.tex"
    os.makedirs(tex_output_path.parent, exist_ok=True)

    description_processed = replace_tikz_with_includegraphics(description, image_path) if image_path else description

    tex_code = f"""\\documentclass{{article}}
\\usepackage{{graphicx}}
\\usepackage{{caption}}
\\usepackage{{amsmath, amssymb}}
\\usepackage[margin=2.5cm]{{geometry}}

\\begin{{document}}

\\section*{{{term.capitalize()}}}

{description_processed}

\\end{{document}}
"""

    tex_output_path.write_text(tex_code, encoding="utf-8")
    print(f"✅ LaTeX file written to: {tex_output_path}")


def convert_pandoc_figures_to_html(md_text: str) -> str:
    """
    Converts Pandoc-style image+caption blocks to HTML <figure> with <figcaption>,
    preserving inline LaTeX and width attributes.
    """
    figure_pattern = re.compile(r'!\[([^\]]+)\]\(([^)]+)\)\{([^}]*)\}', flags=re.DOTALL)

    def repl(match: re.Match) -> str:
        caption = match.group(1).strip()
        img_path = match.group(2).strip()
        attr_string = match.group(3).strip()

        width_match = re.search(r'width\s*=\s*["\']?([\d.]+%)["\']?', attr_string)
        width_attr = f' width="{width_match.group(1)}"' if width_match else ''

        id_match = re.search(r'#([a-zA-Z0-9\-_]+)', attr_string)
        id_attr = f' id="{id_match.group(1)}"' if id_match else ''

        alt_attr = caption.replace('"', '')

        return (
            f'<figure{id_attr}>\n'
            f'  <img src="{img_path}" alt="{alt_attr}"{width_attr}>\n'
            f'  <figcaption>\n'
            f'    {caption}\n'
            f'  </figcaption>\n'
            f'</figure>'
        )

    return figure_pattern.sub(repl, md_text)


def generate_blog_post(
    tex_file: PathLike,
    bib_file: PathLike,
    output_dir: PathLike = "../",
    title: str = "Dictionary of ML – Geometric Median",
    seo_title: str = "Geometric Median – A Robust Alternative to the Mean in Machine Learning",
    seo_description: str = "Understand the geometric median, a key concept in robust statistics and machine learning.",
    post_slug: str = "geometric-median",
    post_date: str | None = None
) -> Path | None:
    """
    Converts a LaTeX file to Markdown using Pandoc and adds Jekyll front matter.
    Writes *raw* md file (suffix _raw.md) and returns that Path.
    """
    post_date = post_date or date.today().isoformat()
    filename = f"{post_date}-{post_slug}_raw.md"
    output_path = Path(output_dir) / filename
    os.makedirs(output_path.parent, exist_ok=True)

    temp_md_path = Path("temp_pandoc_output.md")

    command = [
        "pandoc",
        str(tex_file),
        "-o", str(temp_md_path),
        "--from=latex",
        "--to=markdown",
        "--standalone",
        "--citeproc",
        f"--bibliography={bib_file}"
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("❌ Pandoc conversion failed:", e)
        return None

    markdown_body = temp_md_path.read_text(encoding="utf-8")
    markdown_body = convert_pandoc_figures_to_html(markdown_body)

    front_matter = f"""---
layout: post
title: "{title}"
date: {post_date}
seo_title: "{seo_title}"
seo_description: "{seo_description}"
markdown: kramdown
---

"""

    output_path.write_text(front_matter + markdown_body, encoding="utf-8")
    temp_md_path.unlink(missing_ok=True)

    print(f"✅ Blog post written to: {output_path}")
    return output_path


# ---------- NEW: robust parsing from ADictML*expanded.tex files ----------

NEW_ENTRY_RE = re.compile(r"\\newglossaryentry\{([^}]+)\}\s*\{", re.DOTALL)

def extract_balanced_braces(s: str, start_brace_idx: int) -> Tuple[str, int]:
    """
    Given s[start_brace_idx] == '{', return (content_inside, index_after_closing_brace).
    Handles nested braces.
    """
    if start_brace_idx < 0 or start_brace_idx >= len(s) or s[start_brace_idx] != "{":
        raise ValueError("extract_balanced_braces: start index must point to '{'.")

    depth = 0
    for i in range(start_brace_idx, len(s)):
        ch = s[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return s[start_brace_idx + 1 : i], i + 1
    raise ValueError("Unbalanced braces while parsing.")

def iter_newglossaryentry_blocks(tex: str) -> Iterator[Tuple[str, str]]:
    """
    Yield (key, body_text) for each \\newglossaryentry{key}{body}.
    """
    pos = 0
    while True:
        m = NEW_ENTRY_RE.search(tex, pos)
        if not m:
            break
        key = m.group(1).strip()
        body_open_brace_idx = m.end() - 1  # points to '{' starting the body
        body, next_pos = extract_balanced_braces(tex, body_open_brace_idx)
        yield key, body
        pos = next_pos

def parse_glossary(tex: str) -> Dict[str, str]:
    """
    Return dict: key -> description text (value of description={...})
    """
    glossary: Dict[str, str] = {}

    for key, body in iter_newglossaryentry_blocks(tex):
        body_cleaned = re.sub(r"(?m)^%.*$", "", body)  # remove full-line comments

        desc_idx = body_cleaned.find("description=")
        if desc_idx == -1:
            continue

        brace_idx = body_cleaned.find("{", desc_idx)
        if brace_idx == -1:
            continue

        try:
            desc_text, _ = extract_balanced_braces(body_cleaned, brace_idx)
        except ValueError:
            continue

        glossary[key] = desc_text.strip()

    return glossary

def load_expanded_glossary_sources(source: PathLike) -> str:
    """
    Load and concatenate LaTeX content from:
      - a directory containing ADictML*expanded.tex files, OR
      - a single .tex file (backwards compatible).

    New naming convention: ADictML******expanded.tex
    """
    p = Path(source).expanduser()

    if p.is_file():
        return p.read_text(encoding="utf-8")

    if not p.is_dir():
        raise FileNotFoundError(f"Glossary source not found: {p}")

    files = sorted(p.glob("ADictML*expanded.tex"))
    if not files:
        files = sorted(p.glob("ADictML*Expanded.tex"))

    if not files:
        raise FileNotFoundError(
            f"No expanded glossary files found in {p} matching ADictML*expanded.tex (or ADictML*Expanded.tex)."
        )

    print(f"📚 Loading {len(files)} expanded glossary file(s) from: {p}")
    combined = []
    for f in files:
        txt = f.read_text(encoding="utf-8")
        combined.append(f"% --- BEGIN FILE: {f.name} ---\n{txt}\n% --- END FILE: {f.name} ---\n")
    return "\n".join(combined)


# ---------- Your existing post-processing helpers ----------

def fix_latex_in_file(md_path: PathLike) -> None:
    p = Path(md_path)
    content = p.read_text(encoding="utf-8")
    fixed = fix_latex_in_text(content)
    p.write_text(fixed, encoding="utf-8")
    print(f"✔ Fixed LaTeX math in: {md_path}")


def remove_reference_blocks_and_headers(content: str) -> str:
    lines = content.splitlines()
    cleaned_lines = []

    in_yaml_header = False
    yaml_lines = []
    i = 0

    # Preserve front-matter block
    if lines and lines[0].strip() == "---":
        in_yaml_header = True
        yaml_lines.append(lines[0])
        i = 1
        while i < len(lines):
            yaml_lines.append(lines[i])
            if lines[i].strip() == "---":
                i += 1
                break
            i += 1

    cleaned_lines.extend(yaml_lines)

    # Skip bibliography block and handle references
    skip_bib_block = False
    for line in lines[i:]:
        if line.strip() == "---" and not skip_bib_block:
            skip_bib_block = True
            continue
        if skip_bib_block:
            if line.strip().startswith("bibliography:"):
                continue
            elif line.strip() == "---":
                skip_bib_block = False
                continue
            else:
                continue

        if re.match(r'^#\s+.+\{#.+\}', line):
            continue

        if line.strip() == ':::::: {#refs .references .csl-bib-body .hanging-indent entry-spacing="0"}':
            cleaned_lines.append('**References**')
            cleaned_lines.append('')
            continue

        if line.strip().startswith(":::"):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def clean_markdown_file(input_path: Path, output_path: Path) -> None:
    content = Path(input_path).read_text(encoding="utf-8")
    content = remove_reference_blocks_and_headers(content)
    Path(output_path).write_text(content, encoding="utf-8")
    print(f"✅ Cleaned: {output_path.name}")


def append_footer_to_markdown(md_path: PathLike) -> None:
    footer = """
---

📚 This explanation is part of the [Aalto Dictionary of Machine Learning](https://AaltoDictionaryofML.github.io) — 
an open-access multi-lingual glossary developed at Aalto University to support 
accessible and precise communication in ML.
""".strip()

    path = Path(md_path)
    content = path.read_text(encoding="utf-8")

    if "Aalto Dictionary of Machine Learning" not in content:
        content = content.rstrip() + "\n\n" + footer + "\n"
        path.write_text(content, encoding="utf-8")
        print(f"✅ Footer added to: {md_path}")
    else:
        print(f"⚠️ Footer already present in: {md_path}")


def remove_math_and_raw(text: str) -> str:
    """
    Remove LaTeX math and Jekyll raw tags from Markdown text.
    Keeps all other Markdown content intact.
    """
    text = re.sub(r"{%\s*raw\s*%}", "", text)
    text = re.sub(r"{%\s*endraw\s*%}", "", text)
    text = re.sub(r"{%.*?%}", "", text, flags=re.DOTALL)
    text = re.sub(r"{{.*?}}", "", text, flags=re.DOTALL)

    text = re.sub(r"\$\$(.*?)\$\$", "", text, flags=re.DOTALL)
    text = re.sub(r"\\\[(.*?)\\\]", "", text, flags=re.DOTALL)

    envs = r"(equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?)"
    text = re.sub(rf"\\begin\{{{envs}\}}.*?\\end\{{\1\}}", "", text, flags=re.DOTALL)

    text = re.sub(r"\\\((.*?)\\\)", "", text, flags=re.DOTALL)
    text = re.sub(r"(?<!\$)\$(?!\$)([^$]*?)(?<!\$)\$(?!\$)", "", text, flags=re.DOTALL)

    text = re.sub(r"\\ensuremath\{.*?\}", "", text, flags=re.DOTALL)

    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def make_substack_ready(md_in_path: PathLike, md_out_path: PathLike) -> None:
    raw = Path(md_in_path).read_text(encoding="utf-8")
    cleaned = remove_math_and_raw(raw)
    Path(md_out_path).write_text(cleaned, encoding="utf-8")


# ---------------- MAIN ----------------

if __name__ == "__main__":
    # --- CONFIG: update these paths ---
    EXPANDED_SOURCES = "/Users/junga1/AaltoDictionaryofML.github.io/assets"   # directory containing ADictML*expanded.tex
    BIB_FILE = "/Users/junga1/AaltoDictionaryofML.github.io/assets/Literature.bib"

    OUTPUT_FOLDER = "../_posts"
    IMAGE_OUTPUT_DIR = "../images"
    TEX_OUTPUT_DIR = "../"

    # Choose a glossary key to post
    blog_sample_term = "spectraldecomp"     # e.g., "pmf", "spectraldecomp"
    slug = "spectral-decomposition"         # filename slug (avoid spaces)

    heute = date.today().isoformat()

    # --- Load + parse expanded glossary files ---
    content = load_expanded_glossary_sources(EXPANDED_SOURCES)
    glossary = parse_glossary(content)

    if blog_sample_term not in glossary:
        raise KeyError(
            f"Term '{blog_sample_term}' not found. "
            f"Parsed {len(glossary)} entries. Check key spelling / expanded sources."
        )

    entry_text = glossary[blog_sample_term]

    # --- TikZ handling (optional) ---
    tikz_code = extract_tikz_from_entry(entry_text)
    if tikz_code:
        print("🔍 TikZ figure found – compiling to PNG.")
        compile_tikz_to_png(tikz_code, blog_sample_term + "_tikz", output_dir=IMAGE_OUTPUT_DIR)
        image_rel_path = f"../images/{blog_sample_term}_tikz.png"
        generate_texfile_with_image(
            term=blog_sample_term,
            description=entry_text,
            image_path=image_rel_path,
            output_dir=TEX_OUTPUT_DIR
        )
    else:
        print("ℹ️ No TikZ figure found – generating TeX without image.")
        generate_texfile_with_image(
            term=blog_sample_term,
            description=entry_text,
            image_path=None,
            output_dir=TEX_OUTPUT_DIR
        )

    # --- Convert TeX to Markdown blog post (raw) ---
    tex_file = Path(TEX_OUTPUT_DIR) / f"{blog_sample_term}.tex"
    mdfilename = generate_blog_post(
        tex_file=tex_file,
        bib_file=BIB_FILE,
        post_slug=slug,
        post_date=heute,
        title=f"Aalto Dictionary of ML – {blog_sample_term}",
        seo_title=blog_sample_term,
        seo_description=blog_sample_term,
        output_dir=OUTPUT_FOLDER
    )

    if mdfilename is None:
        raise RuntimeError("Pandoc conversion failed; no markdown produced.")

    # Paths for canonical Jekyll MD and Substack-ready MD
    output_path = Path(OUTPUT_FOLDER) / f"{heute}-{slug}.md"
    substack_path = Path(OUTPUT_FOLDER) / f"{heute}-{slug}_substack.md"

    # Protect LaTeX from Jekyll/Liquid, then clean for Jekyll
    fix_latex_in_file(mdfilename)
    clean_markdown_file(Path(mdfilename), output_path)
    append_footer_to_markdown(output_path)

    # Remove raw temp file
    Path(mdfilename).unlink(missing_ok=True)

    # Produce Substack-ready twin
    make_substack_ready(output_path, substack_path)

    print(f"✅ Jekyll post:     {output_path}")
    print(f"✅ Substack-ready:  {substack_path}")
