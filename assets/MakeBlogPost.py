
import re
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import tempfile
import os
from pathlib import Path
from datetime import date
import subprocess
from typing import Union
from pdf2image import convert_from_path

PathLike = Union[str, Path]

# --- LaTeX + Markdown safety wrappers (add near imports) ---
RAW_OPEN  = "{% raw %}"
RAW_CLOSE = "{% endraw %}"

# Match fenced code blocks ```...``` (any language) and existing raw blocks.
FENCE_OR_RAW_RE = re.compile(
    r"(```.*?```|{% raw %}.*?{% endraw %})",
    flags=re.DOTALL
)

# Display math: $$...$$ (can be multiline)
DISPLAY_MATH_RE = re.compile(
    r"\$\$(.+?)\$\$",
    flags=re.DOTALL
)

# Inline math: $...$ (but not $$...$$)
INLINE_MATH_RE = re.compile(
    r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)",
    flags=re.DOTALL
)

BASE_IMAGE_URL = "https://AaltoDictionaryofML.github.io/images/"

def _wrap_math_segment(segment: str) -> str:
    """
    Wrap only math tokens ($...$ or $$...$$) that contain {{ or }} using {% raw %}...{% endraw %}.
    No extra whitespace/newlines are inserted; we wrap ONLY the math token itself.
    """

    def wrap_if_liquid(match: re.Match) -> str:
        full  = match.group(0)  # the full $...$ or $$...$$ token
        inner = match.group(1)  # the inside of math delimiters
        if "{{" in inner or "}}" in inner:
            return f"{RAW_OPEN}{full}{RAW_CLOSE}"
        return full

    # Order matters: handle display math first (can span multiple lines), then inline math
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
            # Leave code fences & existing raw blocks untouched
            fixed_parts.append(part)
        else:
            fixed_parts.append(_wrap_math_segment(part))
    return "".join(fixed_parts)



def extract_tikz_from_entry(entry_text):
    match = re.search(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', entry_text, re.DOTALL)
    if match:
        return match.group(0)
    else:
        # Try fallback for your custom {tikzpicture} ... {tikzpicture} style
        match = re.search(r'\{tikzpicture\}.*?\{tikzpicture\}', entry_text, re.DOTALL)
        if match:
            tikz_inner = match.group(0)[13:-13].strip()  # remove {tikzpicture} ... {tikzpicture}
            return f"\\begin{{tikzpicture}}\n{tikz_inner}\n\\end{{tikzpicture}}"
    raise ValueError("No tikzpicture found")
    
def replace_tikz_with_includegraphics(description, image_path):
    """
    Replace the TikZ block in the description with a single \includegraphics command.
    """
    include_cmd = fr"\\includegraphics[width=0.8\\linewidth]{{{image_path}}}"
    print(include_cmd)
    print(re.sub(
        r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',
        include_cmd,
        description,
        count=1,
        flags=re.DOTALL
    ))
    return re.sub(
        r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',
        include_cmd,
        description,
        count=1,
        flags=re.DOTALL
    )


def compile_tikz_to_png(tikz_code, filename="tikz_figure", output_dir="../images"):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Output path (e.g., blog_posts/images/generalization.png)
    output_png_path = os.path.join(output_dir, f"{filename}.png")

    # LaTeX document wrapper
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
"""
    tex_path ="figure.tex"
    with open(tex_path, "w") as f:
        f.write(latex_code)
        print(latex_code)

        # Compile LaTeX to PDF
    subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_path])
    print(tex_path)

    pdf_path = "figure.pdf"

        # Convert PDF to PNG using ImageMagick
    subprocess.run([
            "convert", "-density", "300", pdf_path, "-quality", "90", output_png_path
        ])

    print(f"✅ Saved PNG to: {output_png_path}")
    
    
def generate_texfile_with_image(term, description, image_path, output_dir="../"):
    """
    Generate a LaTeX file containing the full glossary description with the TikZ replaced by image.
    """
    from pathlib import Path

    tex_output_path = Path(output_dir) / f"{term}.tex"
    os.makedirs(tex_output_path.parent, exist_ok=True)

    # Replace TikZ block with includegraphics
    description_with_image = replace_tikz_with_includegraphics(description, image_path)

    # Generate LaTeX document
    tex_code = f"""\\documentclass{{article}}
\\usepackage{{graphicx}}
\\usepackage{{caption}}
\\usepackage{{amsmath, amssymb}}
\\usepackage[margin=2.5cm]{{geometry}}

\\begin{{document}}

\\section*{{{term.capitalize()}}}

{description_with_image}

\\end{{document}}
"""

    with open(tex_output_path, "w", encoding="utf-8") as f:
        f.write(tex_code)
        print(f"✅ LaTeX file written to: {tex_output_path}")

        

def convert_pandoc_figures_to_html(md_text):
    """
    Converts Pandoc-style image+caption blocks to HTML <figure> with <figcaption>,
    preserving inline LaTeX and width attributes.
    """
    figure_pattern = re.compile(
        r'!\[([^\]]+)\]\(([^)]+)\)\{([^}]*)\}',
        flags=re.DOTALL
    )

    def repl(match):
        caption = match.group(1).strip()
        img_path = match.group(2).strip()
        attr_string = match.group(3).strip()

        # Extract width="..." if present
        width_match = re.search(r'width\s*=\s*["\']?([\d.]+%)["\']?', attr_string)
        width_attr = f' width="{width_match.group(1)}"' if width_match else ''

        # Optionally extract id from #fig:xyz
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
    tex_file,
    bib_file,
    output_dir="../",
    title="Dictionary of ML – Geometric Median",
    seo_title="Geometric Median – A Robust Alternative to the Mean in Machine Learning",
    seo_description="Understand the geometric median, a key concept in robust statistics and machine learning, minimizing total distance to data points and outperforming the mean under outliers.",
    post_slug="geometric-median",
    post_date=None
):
    """
    Converts a LaTeX file to Markdown using Pandoc and adds Jekyll front matter.

    Args:
        tex_file (str): Path to LaTeX file.
        bib_file (str): Path to BibTeX file.
        output_dir (str): Directory to save generated .md post.
        title (str): Title for the blog post.
        seo_title (str): SEO title for the blog post.
        seo_description (str): SEO description.
        post_slug (str): Filename slug.
        post_date (str): Publication date (YYYY-MM-DD), defaults to today.
    """
    post_date = post_date or date.today().isoformat()
    filename = f"{post_date}-{post_slug}_raw.md"
    output_path = Path(output_dir) / filename

    os.makedirs(output_path.parent, exist_ok=True)

    # Temporary file for Pandoc output (without front matter)
    temp_md_path = Path("temp_pandoc_output.md")

    # Build and run Pandoc command
    command = [
        "pandoc",
        tex_file,
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
        return


    # Read and post-process the generated Markdown
    with open(temp_md_path, "r", encoding="utf-8") as f:
        markdown_body = f.read()

    # Convert Pandoc-style figures to HTML
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

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(front_matter+markdown_body)
    os.remove(temp_md_path)
  #  os.remove(tex_file)
    print(f"✅ Blog post written to: {output_path}")
    return output_path





# --- Step 1: Load LaTeX glossary content ---
with open("/Users/junga1/AaltoDictionaryofML.github.io/assets/ADictML_Glossary_Expanded.tex", "r", encoding="utf-8") as f:
    content = f.read()

# --- Step 2: Match glossary entries ---
entry_pattern = re.compile(r"\\newglossaryentry\{([^}]+)\}\s*\{(.*?)\n\}", re.DOTALL)
entries = entry_pattern.findall(content)

# --- Step 3: Extract content inside balanced braces ---
def extract_balanced_braces(s, start):
    assert s[start] == '{'
    depth = 0
    for i in range(start, len(s)):
        if s[i] == '{':
            depth += 1
        elif s[i] == '}':
            depth -= 1
            if depth == 0:
                return s[start + 1:i], i + 1
    raise ValueError("Unbalanced braces in LaTeX description.")

# --- Step 4: Parse glossary entries ---
glossary = {}
for key, body in entries:
    body_cleaned = re.sub(r"%.*", "", body)          # remove comments
    body_cleaned = re.sub(r"[ \t]+", " ", body)      # collapse horizontal whitespace only
    body_cleaned = re.sub(r"\s+\n", "\n", body_cleaned)  # optional: clean trailing space before linebreak

    
    # --- Extract name ---
    name_start = body_cleaned.find("name=") 
    try:
        name_text, _ = extract_balanced_braces(body_cleaned, name_start + len("name="))
    except:
        name_text = key  # fallback

    # --- Extract description ---
    desc_start = body_cleaned.find("description={")
    if desc_start == -1:
        continue

    try:
        desc_text, _ = extract_balanced_braces(body_cleaned, desc_start + len("description="))
    except ValueError:
        continue

    print(desc_text+"\n")
    glossary[key.strip()] = desc_text
    
def fix_latex_in_file(md_path: str | Path):
    p = Path(md_path)
    content = p.read_text(encoding="utf-8")
    fixed = fix_latex_in_text(content)
    p.write_text(fixed, encoding="utf-8")
    print(f"✔ Fixed LaTeX math in: {md_path}")
    
# def fix_latex_in_file(md_path):
#     with open(md_path, "r", encoding="utf-8") as f:
#         lines = f.readlines()

#     new_lines = []
#     in_raw_block = False

#     for line in lines:
#         modified = line
#         if not in_raw_block:
#             # Detect LaTeX expressions with {{ or }}
#             if re.search(r"\$\$?.*{{.*}}.*\$\$?", line):
#                 new_lines.append("{% raw %}\n")
#                 new_lines.append(modified)
#                 new_lines.append("{% endraw %}\n")
#                 in_raw_block = False  # Stay out; single-line wrap
#             elif "{{" in line or "}}" in line:
#                 new_lines.append("{% raw %}\n")
#                 new_lines.append(modified)
#                 new_lines.append("{% endraw %}\n")
#             else:
#                 new_lines.append(modified)
#         else:
#             new_lines.append(modified)

#     with open(md_path, "w", encoding="utf-8") as f:
#         f.writelines(new_lines)

#     print(f"✔ Fixed: {md_path}")
    
def remove_reference_blocks_and_headers(content: str) -> str:
    lines = content.splitlines()
    cleaned_lines = []

    in_yaml_header = False
    yaml_lines = []
    i = 0

    # Step 1: Preserve front-matter block (layout, title, etc.)
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

    # Step 2: Skip bibliography block and handle references
    skip_bib_block = False
    for line in lines[i:]:
        # Remove bibliography YAML block
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
                continue  # still inside bibliography block

        # Remove H1 headings like "# Title {#...}"
        if re.match(r'^#\s+.+\{#.+\}', line):
            continue

        # Replace CSL reference block marker
        if line.strip() == ':::::: {#refs .references .csl-bib-body .hanging-indent entry-spacing="0"}':
            cleaned_lines.append('**References**')
            cleaned_lines.append('')
            continue

        # Remove other citation lines
        if line.strip().startswith(":::"):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def clean_markdown_file(input_path: Path, output_path: Path):
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = remove_reference_blocks_and_headers(content)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Cleaned: {output_path.name}")
    
    
    
def append_footer_to_markdown(md_path):
    footer = """
---

📚 This explanation is part of the [Aalto Dictionary of Machine Learning](https://AaltoDictionaryofML.github.io) — 
an open-access multi-lingual glossary developed at Aalto University to support 
accessible and precise communication in ML.
"""

    path = Path(md_path)
    content = path.read_text(encoding="utf-8")

    if "Aalto Dictionary of Machine Learning" not in content:
        content = content.rstrip() + "\n\n" + footer.strip() + "\n"
        path.write_text(content, encoding="utf-8")
        print(f"✅ Footer added to: {md_path}")
    else:
        print(f"⚠️ Footer already present in: {md_path}")
        
        
def remove_math_and_raw(text: str) -> str:
    """
    Remove LaTeX math and Jekyll raw tags from Markdown text.
    Keeps all other Markdown content intact.
    """

    # --- 1) Remove Jekyll raw / Liquid tags ---
    text = re.sub(r"{%\s*raw\s*%}", "", text)
    text = re.sub(r"{%\s*endraw\s*%}", "", text)
    text = re.sub(r"{%.*?%}", "", text, flags=re.DOTALL)
    text = re.sub(r"{{.*?}}", "", text, flags=re.DOTALL)

    # --- 2) Remove LaTeX display math ---
    text = re.sub(r"\$\$(.*?)\$\$", "", text, flags=re.DOTALL)   # $$...$$
    text = re.sub(r"\\\[(.*?)\\\]", "", text, flags=re.DOTALL)   # \[...\]

    # --- 3) Remove math environments ---
    envs = r"(equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?)"
    text = re.sub(
        rf"\\begin\{{{envs}\}}.*?\\end\{{\1\}}",
        "",
        text,
        flags=re.DOTALL
    )

    # --- 4) Remove inline math ---
    text = re.sub(r"\\\((.*?)\\\)", "", text, flags=re.DOTALL)   # \( ... \)
    text = re.sub(r"(?<!\$)\$(?!\$)([^$]*?)(?<!\$)\$(?!\$)", "", text, flags=re.DOTALL)

    # --- 5) Remove \ensuremath{...} ---
    text = re.sub(r"\\ensuremath\{.*?\}", "", text, flags=re.DOTALL)

    # --- 6) Tidy up spacing ---
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    return text


def make_substack_ready(md_in_path: PathLike, md_out_path: PathLike) -> None:
    """
    Make a Markdown post 'Substack-ready' by removing LaTeX math and raw tags.
    """
    raw = Path(md_in_path).read_text(encoding="utf-8")
    cleaned = remove_math_and_raw(raw)
    Path(md_out_path).write_text(cleaned, encoding="utf-8")

        
        
# def make_substack_ready(md_in_path: str | Path,
#                         md_out_path: str | Path,
#                         image_base_url: str = BASE_IMAGE_URL) -> None:
#     text = Path(md_in_path).read_text(encoding="utf-8")

#     # 1) Remove Jekyll Liquid guards and tags
#     text = re.sub(r"{%\s*raw\s*%}", "", text)
#     text = re.sub(r"{%\s*endraw\s*%}", "", text)
#     text = re.sub(r"{%.*?%}", "", text, flags=re.DOTALL)
#     text = re.sub(r"{{.*?}}", "", text, flags=re.DOTALL)

#     # 2) Optional: simplify glossary macros \gls{term} -> term
#     text = re.sub(r"\\gls\{([^}]+)\}", r"\1", text)

#     # 3) Un-escape LaTeX math if present
#     text = text.replace(r"\$", "$")
#     text = re.sub(r"\\([{}])", r"\1", text)  # remove backslashes before { }

#     # 4) Make image paths absolute for Substack
#     #    e.g., ../images/foo.png  -> https://.../images/foo.png
#     text = text.replace("../images/", image_base_url)

#     # 5) Tidy spacing
#     text = re.sub(r"\n{3,}", "\n\n", text)

#     Path(md_out_path).write_text(text, encoding="utf-8")
        
########## MAIN 


blog_sample_term= "markovsinequality"
slug="Markov's inequality"
output_folder = "../_posts"
heute = date.today().isoformat()
entry_text = glossary[blog_sample_term]
try:
    tikz_code = extract_tikz_from_entry(entry_text)
    compile_tikz_to_png(tikz_code, blog_sample_term+"_tikz")
    generate_texfile_with_image(
        term=blog_sample_term,
        description=entry_text,
        image_path="../images/"+blog_sample_term+"_tikz.png"
    )
    mdfilename = generate_blog_post(
       tex_file="../"+blog_sample_term+".tex" ,
       bib_file="/Users/junga1/AaltoDictionaryofML.github.io/assets/Literature.bib",
       post_slug=slug,post_date=heute,
       title="Aalto Dictionary of ML – "+slug,
       seo_title="Generalization – How Machine Learning Models Handle Unseen Data",
       seo_description="Explore the concept of generalization in machine learning: how models trained on a dataset perform on new, unseen data.",
       output_dir=output_folder
   )
except Exception as e:
    print("Error:", e)
    

# Paths for canonical Jekyll MD and Substack-ready MD
output_path = Path(output_folder) / f"{heute}-{slug}.md"
substack_path =  f"{heute}-{slug}_substack.md"

# Keep your original cleaning for Jekyll
fix_latex_in_file(mdfilename)                 # protects LaTeX from Jekyll/Liquid
clean_markdown_file(mdfilename, output_path)  # your existing Jekyll MD cleaner
append_footer_to_markdown(output_path)
os.remove(mdfilename)

# Produce Substack-ready twin
make_substack_ready(output_path, substack_path)

print(f"✅ Jekyll post:     {output_path}")
print(f"✅ Substack-ready:  {substack_path}")
    
# output_path = Path(output_folder+"/"+f"{heute}-{slug}.md")
# fix_latex_in_file(mdfilename)
# clean_markdown_file(mdfilename,output_path)
# append_footer_to_markdown(output_path)
# os.remove(mdfilename)