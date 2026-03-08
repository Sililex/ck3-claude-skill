---
description: Expert CK3 modding assistance - scripting, events, triggers, effects, scopes, localization
---

You are assisting with Crusader Kings III modding. CK3 uses a custom Paradox scripting language (called "Jomini script") — not JSON, not YAML — with its own rules.

**Always consult the relevant `.info` reference file before writing or reviewing code for a system.** They are in the `reference/` directory alongside this SKILL.md.

**Detailed reference files**: `scopes.md`, `effects.md`, `triggers.md`, `variables.md`, `ai.md`, `bookmarks.md`, `characters.md`, `cultures.md`, `decisions.md`, `dynasties.md`, `events.md`, `governments.md`, `history.md`, `holdings.md`, `lifestyles.md`, `regiments.md`, `religions.md`, `script_values.md`, `story_cycles.md`, `struggles.md`, `traits.md`

# What Script Can and Cannot Do

- Most AI/army behavior is hardcoded and inaccessible to modders.
- UI is a separate system. Use Scripted GUIs to bridge script and UI.
- History modding uses a slightly different static system but allows effects.
- No access to the OS, no string manipulation, no in-line math, one-dimensional arrays only.

# Three Function Types

Generate full lists with `script_docs` console command (outputs to logs folder).

1. **Effects** — do something (e.g. `add_gold`). Used in effect blocks: `immediate = {}`, `effect = {}`, `on_accept = {}`, event option bodies. **See `effects.md` for full reference (forms, scripted effects, text replacement pitfalls).**
2. **Triggers** — check something, return true/false (e.g. `is_ai = yes`). Used in trigger blocks: `limit = {}`, `trigger = {}`, `is_shown = {}`, `is_valid = {}`. **See `triggers.md` for full reference (early out, logic blocks, scope/value comparison, in-line complex triggers).**
3. **Event targets** — select another game object (e.g. `primary_heir`). We call objects "scopes" and switching between them "scoping".

**Never put effects where triggers are expected, or vice versa.** The game will error or silently fail.

# Syntax

```
x = y
x = { y = z }
x = {
	a = b
	e = {
		f = g
	}
}
```

- Effects and triggers always need a paired parameter (sometimes just `= yes`).
- Triggers can use `= no` to check the opposite: `is_ai = no` is the same as `NOT = { is_ai = yes }`.
- Triggers that check a value can also return it: `add_gold = age` adds gold equal to the character's age.
- Complex triggers with a target use special syntax: `add_gold = "opinion(liege)"` (quotes required).
- Indentation (tabs) doesn't affect execution but is critical for readability — one tab per code block level.
- Comments: `#`

# Scopes

Scopes are database objects (characters, titles, provinces, cultures, faiths, etc.). Effects/triggers must be used on the correct scope type.

**For the full scopes reference (context switching, list-builders, saved scopes, `every_X`/`random_X`/`ordered_X`/`any_X`, etc.), see `scopes.md`.**

Key points:
- **`root`** — default context of the current block (NOT "the player"). In events, it's the character receiving the event.
- **`prev`** — previous scope (one step back). Cannot be chained (`prevprev` does not exist).
- **`this`** — current scope. Useful for comparisons: `this = root`.
- **Context switch**: open a new block with the target scope: `title:k_france = { ... }`
- **Chaining**: `primary_heir.faith.religious_head` chains scope transitions with `.`
- **Database access**: `title:k_france`, `culture:english`, `faith:orthodox`, `character:123456`
- **`?=`** — checks existence before comparing: `capital_county ?= title:c_byzantion`
- **Non-historical characters** cannot be accessed by ID — use `random_X` + `save_scope_as` to find and save them.

**Important**: Do NOT use `scope:` before `root`, `prev`, or `this`. `scope:` is only for saved scopes.

# Operators

## Logic Operators

`AND`, `OR`, `NOT`, `NOR`, `NAND` — convention is to capitalize for readability.

```
OR = {
	is_ai = yes
	gold > 100
}
```

- `AND` — true if all conditions true (all trigger blocks are AND by default)
- `OR` — true if any condition true
- `NOT` / `NOR` — true if all conditions false (they are equivalent)
- `NAND` — true if any condition false

Can be nested: `OR = { AND = { NOT = { ... } } }`

## Relational Operators

- `=` — equality / scope comparison (`primary_heir = primary_spouse`)
- `!=` — not equal
- `<`, `<=`, `>`, `>=` — value comparisons
- `?=` — checks existence first, then compares. `capital_county ?= title:c_byzantion` is equivalent to `exists = capital_county` + `capital_county = title:c_byzantion`

# Saved Scopes

Save an object to reference later. Exists only in the current script execution chain (persists through called events/scripted effects, gone when the chain ends).

```
primary_heir = { save_scope_as = my_son }
scope:my_son = { death = natural }
```

`save_scope_value_as` saves a value or string flag:
```
save_scope_value_as = {
	name = cost
	value = primary_heir.age
}
add_gold = scope:cost

save_scope_value_as = {
	name = kill_locale
	value = flag:tower
}
if = {
	limit = { scope:kill_locale = flag:tower }
	# ...
}
```

**In trigger blocks, use `save_temporary_scope_as` and `save_temporary_scope_value_as`.** Normal versions will not work there.

Some saved scopes are premade by the game in on_actions and character interactions (e.g. `scope:actor`, `scope:recipient`). Check comments in on_action files.

# Variables

**See `variables.md` for full reference (all types, chaining, UI display, dead character variables).**

Quick summary: `set_variable`, access with `var:`, change with `change_variable`, remove with `remove_variable`.

| Type | Access | Storage |
|------|--------|---------|
| Normal | `var:` | On scope object (lost on character death) |
| Global | `global_var:` | Gamestate (accessible anywhere) |
| Local | `local_var:` | Temporary (gone when block ends) |
| Dead | `dead_var:` | Dead character (requires duration) |

Variables can be chained: `scope:someone.var:my_var.father.var:other_var`

# Statements

## if / else_if / else (EFFECT blocks only)

```
if = {
	limit = { is_ai = no }
	add_gold = 100
}
else_if = {
	limit = { ... }
	# effect
}
else = {
	# effect
}
```

`limit` acts like AND — multiple conditions inside without needing `AND = {}`.

**Common mistake**: putting effects inside `limit` instead of the `if` block.

## switch

Replaces chains of else_ifs checking the same trigger:
```
switch = {
	trigger = has_culture
	culture:english = { add_gold = 10 }
	culture:french = { add_gold = 20 }
}
```

## while loop

```
while = {
	count = 10
	add_gold = 100
}

while = {
	limit = { gold > 0 }
	remove_short_term_gold = 50
}
```

Limited to 1000 iterations by default. No break statement.

## trigger_if / trigger_else_if / trigger_else (TRIGGER blocks only)

Checks a trigger conditionally. If limit is false, the check is skipped entirely.

```
trigger_if = {
	limit = { is_ai = no }
	is_independent_ruler = yes
}
```

**Must finish with `trigger_else` when using `trigger_else_if`** (even if empty). Plain `trigger_if` alone doesn't require it.

**Only use in trigger blocks, never in effect blocks.**

# Lists / Arrays

Lists hold objects, variables, or string flags. Cannot hold other lists.

## List Types

| Type | Add effect | Persistent? | Notes |
|------|-----------|-------------|-------|
| Simple | `add_to_list` | No (execution only) | |
| Local variable | `add_to_local_variable_list` | No | Supports duration |
| Temporary | `add_to_temporary_list` | No | **Can be used in trigger blocks** |
| Variable | `add_to_variable_list` | Yes (on scope) | Supports duration |
| Global variable | `add_to_global_variable_list` | Yes (global) | Supports duration |

Items are not duplicated if already in the list.

**`add_to_variable_list` gotcha**: run the effect on the scope that stores the list, not the target:
```
every_ruler = {
	root = {
		add_to_variable_list = {
			name = rulers
			target = prev
		}
	}
}
```

Always `clear_variable_list` before recreating a list to avoid stale items.

Check membership: `is_in_list`, `is_target_in_variable_list`, etc.

# Iterators

## Effect Iterators (effect blocks only)

- `every_x` — runs through all items in order
- `ordered_x` — orders by a value, can iterate all or pick one
- `random_x` — picks one random item, chance can be manipulated

All support `limit = {}` (optional; if false, effect is skipped for that item).

## Trigger Iterator

- `any_x` — returns true if condition is true for any/all items

Supports `count` and `percent` with relational operators:
```
any_living_character = {
	count > 10
	has_culture = culture:english
	is_adult = yes
}
```

**Do NOT use `limit` inside `any_` — it is already a trigger block. No effects either.**

## List Iterators

`every_in_list`, `ordered_in_list`, `random_in_list`, `any_in_list` (and `_local_` / `_global_` variants).

Specify list with `list = name` or `variable = name`.

**Performance warning**: Avoid nested iterators over large sets (e.g. `every_living_character = { every_province = {` — 20000 × 9000 iterations).

# Templates

## Scripted Effects

Defined in `common/scripted_effects/` (global) or in event files with `scripted_effect` keyword:
```
my_effect = { add_gold = 100 }
```
Used: `my_effect = yes`

### Substitution (Parameters)

Use `$PARAM$` in the definition:
```
gift = { add_gold = $VAL$ }
```
Call with: `gift = { VAL = 100 }`

Can replace any part of script, including effect names:
```
my_iterator = { every_$WHO$ = { add_gold = 10 } }
my_iterator = { WHO = child }
```

Can insert whole blocks:
```
do_anything = { $DO$ }
do_anything = { DO = "add_gold = 100" }
```

Convention: capitalize parameter names for readability.

## Scripted Triggers

Same as scripted effects but for trigger blocks. Defined in `common/scripted_triggers/`.

Can use `= no` when calling to check the inverse. Substitution works the same way.

## Script Values

Run a calculation and return a value. Defined in `common/script_values/`:
```
my_value = {
	add = age
	add = 10
	divide = 5
}
```
Used: `add_gold = my_value`

In UI: `[GetPlayer.MakeScope.ScriptValue('my_value')]` (no `GetValue`).

**Performance**: Script values recalculate every time they're used. Complex ones cause lag, especially in UI (recalculates every frame).

# Modifiers

There are two unrelated things both called "modifier" in CK3:

1. **Character/scope modifiers** — long-term bonuses/penalties applied to a character, dynasty, county, etc. Defined in `common/modifiers/`. See `reference/common/modifiers/_modifiers.info`.
2. **Weight modifiers** — change the chances of random effects happening (used in `ai_chance`, `weight_multiplier`, etc.). These are unrelated to scope modifiers.

## Creating a Modifier

```
my_new_modifier = {
	icon = economy_positive
	tax_mult = 0.25
	county_opinion_add = -30
}
```

Icons are in `gfx/interface/icons/modifiers/`. Common naming: `{category}_positive` / `{category}_negative` (e.g. `diplomacy_positive`, `health_negative`, `economy_positive`, `stress_negative`, `fertility_positive`, `prowess_negative`).

Full list of modifier values (what stats they can affect): see `reference/common/modifier_definition_formats/_definitions.info`.

# Localization

- Files are YAML with BOM encoding, `l_english:` header
- Keys use `:0` suffix (`:1`, `:2` for revisions indicating changed text)
- Scope access: `[character.GetName]`, `[character.GetSheHe]`, `[title.GetName]`
- Custom loc: `[character.Custom('custom_loc_key')]`

# System Reference Files

Detailed documentation for each moddable system lives in the `reference/` directory, mirroring the game's `.info` files.

## Most Commonly Used References

| System | Reference File |
|--------|---------------|
| Events | `reference/events/_events.info` |
| Decisions | `reference/common/decisions/_decisions.info` |
| Casus Belli | `reference/common/casus_belli_types/_casus_belli.info` |
| On Actions | `reference/common/on_action/_on_actions.info` |
| Story Cycles | `reference/common/story_cycles/_story_cycles.info` |
| Character Interactions | `reference/common/character_interactions/_character_interactions.info` |
| Traits | `reference/common/traits/_traits.info` |
| Buildings | `reference/common/buildings/_buildings.info` |
| Laws | `reference/common/laws/_laws.info` |
| Schemes | `reference/common/schemes/scheme_types/_schemes.info` |
| Factions | `reference/common/factions/_factions.info` |
| Script Values | `reference/common/script_values/_script_values.info` |
| Scripted Modifiers | `reference/common/scripted_modifiers/_scripted_modifiers.info` |
| Modifiers | `reference/common/modifiers/_modifiers.info` |
| Culture | `reference/common/culture/cultures/_cultures.info` |
| Religion | `reference/common/religion/religions/_religions.info` |
| Effect Localization | `reference/common/effect_localization/_effect_localization.info` |
| Trigger Localization | `reference/common/trigger_localization/_trigger_localization.info` |
| Custom Loc | `reference/common/customizable_localization/_custom_loc.info` |
| Succession | `reference/common/succession_election/_succession_election.info` |
| Men at Arms | `reference/common/men_at_arms_types/_men_at_arms_types.info` |
| Governments | `reference/common/governments/_governments.info` |
| History | `reference/history/_history.info` |

## All Reference Files

All 165 `.info` files are in `reference/`, preserving the game directory structure. Browse:
- `reference/common/` — gameplay systems
- `reference/events/` — event structure
- `reference/history/` — history file format
- `reference/gfx/` — graphical definitions
- `reference/gui/` — UI widgets

# Testing

- Console: `effect add_gold = 100` or `trigger is_ai = yes`
- Script runner: `explorer` console command
- Run folder: place script in `run/filename.txt`, execute with `run filename.txt`
- `-develop` launch option: instant reload of events/decisions
- `-debug_mode` launch option: enables console
- `release_mode` console command: shows error tracker in game
- Validation: CK3 Tiger (VS Code extension)
- Error log: keep open while testing

# Updating Reference Files

Run `python sync_ck3_info.py` from the repo root to re-sync after game updates. The script auto-detects common Steam paths, or use `--game-dir` to specify your CK3 install. See `README.md` in the repo root for details.
