#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  1 19:06:39 2025

@author: junga1
"""

import re
from pathlib import Path

def fix_latex_in_file(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    in_raw_block = False

    for line in lines:
        modified = line
        if not in_raw_block:
            # Detect LaTeX expressions with {{ or }}
            if re.search(r"\$\$?.*{{.*}}.*\$\$?", line):
                new_lines.append("{% raw %}\n")
                new_lines.append(modified)
                new_lines.append("{% endraw %}\n")
                in_raw_block = False  # Stay out; single-line wrap
            elif "{{" in line or "}}" in line:
                new_lines.append("{% raw %}\n")
                new_lines.append(modified)
                new_lines.append("{% endraw %}\n")
            else:
                new_lines.append(modified)
        else:
            new_lines.append(modified)

    with open(md_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"✔ Fixed: {md_path}")

# --- Run the script on a specific file ---
if __name__ == "__main__":
    md_file = Path("../_posts/2025-06-01-Generalization.md")  # Modify as needed
    if md_file.exists():
        fix_latex_in_file(md_file)
    else:
        print(f"❌ File not found: {md_file}")