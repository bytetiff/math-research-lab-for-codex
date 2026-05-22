from __future__ import annotations

from pathlib import Path
import sys

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PLUGIN_ROOT / "src"))

from math_research_lab.script_cli import main as _main


def main(argv: list[str] | None = None) -> int:
    '''Run this Math Research Lab command line utility.'''
    return _main('check_split_overlap', argv)


if __name__ == "__main__":
    raise SystemExit(main())
