"""
Fixes a pandoc-to-typst table pagination bug in the workbook's PDF build.

pandoc's typst writer wraps every markdown table in `#figure(align(center)[
#table(...)], kind: table)`. In Typst, a figure is NOT breakable across pages
(only a bare table is) -- so any table too tall to fit in the remaining page
space doesn't flow to the next page, it overflows and its rows visually
overlap the page boundary. Short tables in this workbook happened to fit on
one page, which is why this went unnoticed until the 11-row troubleshooting
table didn't.

This strips the figure wrapper (which we don't use for numbering/captions
anyway -- none of this workbook's tables have a pandoc caption) down to a
bare, page-breakable `#align(center)[#table(...)]`, applied uniformly so any
future long table is protected too, not just the one that broke.

Usage: python fix_workbook_tables.py input.typ
(rewrites the file in place)
"""
import sys
from pathlib import Path

PREFIX_OLD = "#figure(\n  align(center)[#table("
PREFIX_NEW = "#align(center)[#table("
SUFFIX_OLD = ")]\n  , kind: table\n  )"
SUFFIX_NEW = ")]"


def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "workbook.typ")
    text = path.read_text(encoding="utf-8")

    n_prefix = text.count(PREFIX_OLD)
    n_suffix = text.count(SUFFIX_OLD)
    if n_prefix != n_suffix:
        print(f"WARNING: found {n_prefix} figure-table prefixes but {n_suffix} suffixes -- "
              f"pandoc's output format may have changed; check before trusting this fix.")

    text = text.replace(PREFIX_OLD, PREFIX_NEW).replace(SUFFIX_OLD, SUFFIX_NEW)
    path.write_text(text, encoding="utf-8")
    print(f"Unwrapped {n_prefix} table(s) from non-breakable figures in {path}")


if __name__ == "__main__":
    sys.exit(main())
