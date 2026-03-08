# CK3 Modding Skill for Claude Code

A Claude Code skill that provides expert assistance with Crusader Kings III modding. Covers the full Paradox "Jomini" scripting language — scopes, effects, triggers, events, decisions, and every major moddable system.

## What's Included

- **SKILL.md** — Top-level index with core scripting concepts (syntax, scopes, operators, variables, statements, lists, iterators, templates, modifiers, localization)
- **21 topic guides** — Detailed reference docs for each major system (events, traits, decisions, cultures, religions, etc.)
- **165 `.info` reference files** — Authoritative system documentation extracted from the CK3 game directory, organized in `reference/`

## Installation

Copy or symlink the `ck3-modding/` directory into your Claude Code skills folder:

```bash
# Option 1: Symlink (recommended — stays in sync with repo)
ln -s /path/to/ck3-claude-skill/ck3-modding ~/.claude/skills/ck3-modding

# Option 2: Copy
cp -r /path/to/ck3-claude-skill/ck3-modding ~/.claude/skills/ck3-modding
```

Claude Code will automatically load `SKILL.md` when working in any CK3 mod project.

## Updating Reference Files

The `reference/` directory contains `.info` files copied from the CK3 game directory. After a game update, re-sync them:

```bash
python sync_ck3_info.py
```

The script auto-detects common Steam installation paths. If auto-detection fails, specify your CK3 install manually:

```bash
python sync_ck3_info.py --game-dir "/path/to/Crusader Kings III/game"
```

Common Steam paths:
- **Windows:** `C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game`
- **Linux:** `~/.steam/steam/steamapps/common/Crusader Kings III/game`
- **macOS:** `~/Library/Application Support/Steam/steamapps/common/Crusader Kings III/game`

Options:
- `--game-dir PATH` — Path to your CK3 `game/` directory
- `--skill-dir PATH` — Override destination (default: `~/.claude/skills/ck3-modding/reference`)
- `--clean` — Wipe the reference directory before copying

## Topic Guides

| Guide | Covers |
|-------|--------|
| `scopes.md` | Database scopes, context switching, root/prev/this, list-builders, saved scopes |
| `effects.md` | Effect forms, scripted effects, text replacement pitfalls |
| `triggers.md` | Early out, logic blocks, comparisons, scripted triggers |
| `variables.md` | Normal/global/local/dead variables, chaining, UI display |
| `events.md` | Event structure, portraits, themes, options, on_actions |
| `decisions.md` | Decision structure, all keys, localization, widgets |
| `traits.md` | Categories, flags, generation, groups, level tracks, dynamic icons |
| `cultures.md` | Groups, cultures, names, patronyms, ethnicities |
| `religions.md` | Families, religions, faiths, holy sites, localization keys |
| `ai.md` | AI defines, chance/weight, personality values, conqueror pattern |
| `bookmarks.md` | Structure, portraits, map images, CoA |
| `characters.md` | DNA, outfit tags, history characters |
| `dynasties.md` | Dynasties, houses, CoA, scoping limitations |
| `governments.md` | Government structure and caveats |
| `history.md` | Title history, culture history, effects in history |
| `holdings.md` | Holding types, auto-generated modifiers |
| `lifestyles.md` | Lifestyles, focuses, perks, conditional modifiers |
| `regiments.md` | Men-at-arms types, unlocking via innovations/traditions |
| `script_values.md` | Formulas, execution order, inlining, chaining |
| `story_cycles.md` | Structure, passthrough pattern, persistent storage |
| `struggles.md` | Phases, catalysts, phase effects |

## Requirements

- Claude Code CLI
- Crusader Kings III (for syncing `.info` files after game updates)
- Python 3 (for `sync_ck3_info.py` only)

## License

The `.info` reference files are extracted from Crusader Kings III by Paradox Interactive. The guide content is original documentation.
