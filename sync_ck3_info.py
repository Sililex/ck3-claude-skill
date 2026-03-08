#!/usr/bin/env python3
"""
Sync .info reference files from CK3 game directory into the Claude Code
ck3-modding skill directory.

Copies all .info files, preserving the relative directory structure from the
game root. Intended to be re-run whenever the game updates.

Usage:
    python sync_ck3_info.py --game-dir "/path/to/Crusader Kings III/game"
    python sync_ck3_info.py [--skill-dir PATH] [--clean]

The script will attempt to auto-detect your CK3 installation if --game-dir
is not provided. Override with --game-dir if auto-detection fails.
"""

import argparse
import platform
import shutil
import sys
from pathlib import Path

DEFAULT_SKILL_DIR = Path.home() / ".claude" / "skills" / "ck3-modding" / "reference"

# Common Steam installation paths by platform
_STEAM_CANDIDATES = {
    "Windows": [
        Path("C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game"),
        Path("C:/Program Files/Steam/steamapps/common/Crusader Kings III/game"),
        Path("D:/SteamLibrary/steamapps/common/Crusader Kings III/game"),
        Path("E:/SteamLibrary/steamapps/common/Crusader Kings III/game"),
    ],
    "Linux": [
        Path.home() / ".steam" / "steam" / "steamapps" / "common" / "Crusader Kings III" / "game",
        Path.home() / ".local" / "share" / "Steam" / "steamapps" / "common" / "Crusader Kings III" / "game",
    ],
    "Darwin": [
        Path.home() / "Library" / "Application Support" / "Steam" / "steamapps" / "common" / "Crusader Kings III" / "game",
    ],
}


def find_game_dir() -> Path | None:
    """Try to auto-detect the CK3 game directory."""
    candidates = _STEAM_CANDIDATES.get(platform.system(), [])
    for candidate in candidates:
        if candidate.is_dir() and any(candidate.rglob("*.info")):
            return candidate
    return None


def sync_info_files(game_dir: Path, skill_dir: Path, clean: bool = False) -> None:
    if not game_dir.is_dir():
        print(f"Error: game directory not found: {game_dir}", file=sys.stderr)
        sys.exit(1)

    info_files = sorted(game_dir.rglob("*.info"))
    if not info_files:
        print(f"Error: no .info files found in {game_dir}", file=sys.stderr)
        sys.exit(1)

    if clean and skill_dir.exists():
        print(f"Cleaning {skill_dir}")
        shutil.rmtree(skill_dir)

    skill_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    for src in info_files:
        rel = src.relative_to(game_dir)
        dst = skill_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied += 1

    print(f"Copied {copied} .info files from\n  {game_dir}\nto\n  {skill_dir}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--game-dir", type=Path, default=None,
                        help="Path to CK3 game/ directory (auto-detected if omitted)")
    parser.add_argument("--skill-dir", type=Path, default=DEFAULT_SKILL_DIR,
                        help="Destination directory for .info files")
    parser.add_argument("--clean", action="store_true",
                        help="Remove existing reference dir before copying")
    args = parser.parse_args()

    game_dir = args.game_dir
    if game_dir is None:
        game_dir = find_game_dir()
        if game_dir is None:
            print("Error: could not auto-detect CK3 installation.", file=sys.stderr)
            print("Please provide --game-dir /path/to/Crusader Kings III/game", file=sys.stderr)
            sys.exit(1)
        print(f"Auto-detected CK3 at: {game_dir}")

    sync_info_files(game_dir, args.skill_dir, args.clean)


if __name__ == "__main__":
    main()
