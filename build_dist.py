#!/usr/bin/env python
"""Package ai-trace-remover into a source .zip and a Windows .exe.

Run from the skill root:

    python build_dist.py            # source .zip only (pure stdlib, always works)
    python build_dist.py --exe      # additionally build a single-file Windows .exe

The skill is pure standard library (no runtime dependencies), so the source
archive is fully self-contained: unzip and run ``python -m src.cli``. The
.exe wraps the same entry point for users without Python installed.

Output goes to ``dist/`` only; no build artifacts pollute the source tree:

    dist/ai-trace-remover-1.0.0.zip        # source distribution
    dist/ai-trace-remover.exe              # Windows single-file binary (with --exe)

The source zip excludes ``__pycache__``, ``.pytest_cache``, ``dist`` and the
two temporary build files this script creates.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"

# Files / directories that make up a shippable source distribution.
INCLUDE_FILES = [
    "SKILL.md", "README.md", "README_zh.md", "LICENSE", "AUTHORS.md",
    "CHANGELOG.md", "CITATION.cff", "CONTRIBUTING.md",
    "pyproject.toml", "requirements.txt", ".gitignore", "build_dist.py",
]
INCLUDE_DIRS = ["src", "references", "tests"]
EXCLUDE_DIR_PARTS = {"__pycache__", ".pytest_cache", "dist"}

# Temporary build helper files this script writes, kept out of the source zip.
_TEMP_FILES = {"build_dist.py", "_pyi_main.py"}


def _version() -> str:
    sys.path.insert(0, str(ROOT))
    from src import __version__
    return __version__


def build_zip() -> Path:
    out = DIST / f"ai-trace-remover-{_version()}.zip"
    out.parent.mkdir(parents=True, exist_ok=True)
    prefix = f"ai-trace-remover-{_version()}"

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in INCLUDE_FILES:
            p = ROOT / name
            if p.exists():
                zf.write(p, f"{prefix}/{name}")
        for d in INCLUDE_DIRS:
            base = ROOT / d
            if not base.exists():
                continue
            for p in sorted(base.rglob("*")):
                if not p.is_file():
                    continue
                rel = p.relative_to(ROOT)
                if any(part in EXCLUDE_DIR_PARTS for part in rel.parts[:-1]):
                    continue
                zf.write(p, f"{prefix}/{rel}")

    size = out.stat().st_size
    print(f"[zip] wrote {out} ({size} bytes)")
    return out


def _write_entry_files() -> None:
    """Write the PyInstaller entry file so the package bundles as a real package."""
    # _pyi_main.py: PyInstaller entry (run with --onefile). It imports the CLI
    # from the bundled 'src' package and runs main(). The CLI itself rebinds
    # stdout/stderr to UTF-8 on first call so the Chinese report renders even
    # under a legacy Windows console (cp1252).
    (ROOT / "_pyi_main.py").write_text(
        "# -*- coding: utf-8 -*-\n"
        "import sys\n"
        "from src.cli import main\n\n"
        "if __name__ == '__main__':\n"
        "    sys.exit(main())\n",
        encoding="utf-8",
    )


def build_exe() -> Path:
    out = DIST / f"ai-trace-remover-{_version()}-windows.exe"
    out.parent.mkdir(parents=True, exist_ok=True)
    _write_entry_files()

    py = sys.executable
    colon = ":" if os.name == "nt" else os.pathsep
    cmd = [
        py, "-m", "PyInstaller",
        "--onefile",
        "--name", f"ai-trace-remover-{_version()}-windows",
        "--clean", "--noconfirm",
        "--hiddenimport", "src.cli",
        f"--add-data={ROOT / 'src'}{colon}src",
        f"--add-data={ROOT / 'references'}{colon}references",
        f"--paths={ROOT}",
        f"--distpath={DIST}",
        f"--workpath={DIST / '_pyi_work'}",
        f"--specpath={DIST}",
        str(ROOT / "_pyi_main.py"),
    ]
    print("[exe] building Windows single-file binary with PyInstaller...")
    r = subprocess.run(cmd)
    if r.returncode != 0:
        # Clean up the temporary entry file regardless.
        _cleanup_temp()
        raise SystemExit(
            "PyInstaller build failed. Install it first: pip install pyinstaller"
        )
    _cleanup_temp()
    print(f"[exe] wrote {out}")
    return out


def _cleanup_temp() -> None:
    for name in _TEMP_FILES:
        p = ROOT / name
        if p.name != "build_dist.py" and p.exists():
            p.unlink()
    # Also remove the PyInstaller work dir and any stray spec.
    for sub in (DIST / "_pyi_work",):
        shutil.rmtree(sub, ignore_errors=True)
    for spec in DIST.glob("*.spec"):
        spec.unlink()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Build dist artifacts for ai-trace-remover.")
    ap.add_argument("--exe", action="store_true",
                    help="also build the Windows single-file .exe (needs PyInstaller)")
    args = ap.parse_args(argv)

    build_zip()
    if args.exe:
        build_exe()
    print("\ndone.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
