# Triggers — Full Reference

See also `reference/common/traits/_traits.info`.

A trigger is a check that returns true or false for the scope where it's used.

Example: `is_ai = yes` returns true for an AI character, false for a player.

Triggers that compare values can also **return the value itself**:
`add_gold = gold` adds the same amount of gold the character currently has.

Full list: `script_docs` console command → `triggers.log`

## Trigger Blocks

Triggers are used in trigger script blocks, usually:
- Explicitly named: `trigger = { }`
- Named as yes/no questions: `is_shown = { }`, `is_valid = { }`

Triggers can also appear in **hybrid blocks** alongside other things:
```
modifier = {
	is_ai = yes     # trigger
	factor = 0      # operator (not a trigger)
}
```

### Early Out

Trigger blocks use **early out**: as soon as a trigger evaluates false, the rest of the block is skipped.

This is useful to **avoid errors**:
```
trigger = {
	exists = primary_spouse
	culture = primary_spouse.culture
}
```
If `exists = primary_spouse` is false, the second trigger is never evaluated (no error from missing spouse).

It is also useful for **performance**: put the triggers most likely to fail first.
```
trigger = {
	is_ai = no                  # most characters are AI — fails fast
	is_independent_ruler = yes
}
```

**Exception**: when tooltipped, early-out does NOT apply. Use `trigger_if` to guard against errors in tooltipped blocks:
```
# Safe even when tooltipped:
trigger_if = {
	limit = { exists = primary_spouse }
	culture = primary_spouse.culture
}
```

## Logic Blocks

By default, all triggers in a block must be true (implicit AND). Logic blocks change this.

### AND
```
AND = {
	is_ai = no
	is_independent_ruler = yes
}
```
True if both conditions are true. (Same as default behavior, but explicit.)

### OR
```
OR = {
	is_ai = no
	is_independent_ruler = yes
}
```
True if either condition is true.

### NOT / NOR / NAND

**NOT** — true if the enclosed trigger is false. Should only contain a **single trigger** to avoid ambiguity:
```
NOT = { has_title = title:k_france }
```

**NAND** — true if NOT all conditions are true (i.e. at least one is false):
```
NAND = {
	has_title = title:k_france
	has_title = title:k_aquitaine
}
# true unless they hold BOTH titles
```

**NOR** — true if NONE of the conditions are true:
```
NOR = {
	has_title = title:k_france
	has_title = title:k_aquitaine
}
# true only if they hold neither title
```

Aliases: `all_false` = NOR, `any_false` = NAND.

## Limit Blocks

The `limit` block is used for conditional effects and triggers.

### In if/else_if (effect blocks)
```
if = {
	limit = { is_ai = no }
	add_gold = 100
}
```

### In effect list-builders
```
every_child = {
	limit = { is_male = yes }
	add_gold = 100
}
```

**Note**: `any_X` does NOT use `limit` — use `filter` instead.

### In trigger_if/trigger_else_if/trigger_else (trigger blocks)

Checks a trigger only if the limit is true:
```
trigger_if = {
	limit = { is_ai = no }
	is_independent_ruler = yes
}
```

## Trigger Syntax

### Scope Comparison

Two scopes on either side of `=`. True if they are the same object:
```
title:k_france.holder = father
```

Both sides must be valid (exist). Use `?=` to guard the left-hand side:
```
title:k_france.holder ?= father
```

Both sides must be the **same scope type** even if they are different objects.

### Value Comparison

Two numerical values with `=`, `>`, `>=`, `<`, `<=`:
```
gold > 1000
```

Numerical values can be: a number, a named value, a script_value, a saved scope value, or a variable storing a number.

### Code Triggers

Predetermined syntax, usually require a specific scope type.

#### Basic Triggers
Check positive or negative result:
```
is_ai = no
```

#### Simple Triggers
Check against a single argument (scope, database key):
```
is_vassal_of = scope:actor
has_trait = infirm
```

#### Complex Triggers
Use multiple parameters in a block:
```
is_scheming_against = {
	target = liege
	type = murder
}
```

Some code triggers have both simple and complex forms.

#### In-line Complex Triggers

Some complex triggers can be written in one line to **return a value**, using quotation marks with the argument in brackets:
```
distance_to_liege_sval = {
	value = "realm_to_title_distance_squared(liege.capital_county)"
}
```

This only works with triggers that have `Traits: <, <=, =, !=, >, >=` in their description.

Multiple arguments use `|` separator:
```
value = "has_trait_xp(lifestyle_traveler|danger)"
```

## Scripted Triggers

Macros that replace a set of triggers with a single statement. Defined in `common/scripted_triggers/` (or locally in event files, scoped to that file only).

### Basic Form
```
# Definition:
is_rich_adult_independent_ruler = {
	is_adult = yes
	is_independent_ruler = yes
	gold > 1000
}

# Usage:
is_rich_adult_independent_ruler = yes

# Negated:
is_rich_adult_independent_ruler = no
# equivalent to: NOT = { is_rich_adult_independent_ruler = yes }
```

Avoid using ambiguous event targets like `root` or `prev` in definitions.

### Complex Form (Text Replacement)

Same literal text replacement as scripted effects — `$PARAM$` in definition, `PARAM = value` at usage:
```
# Definition:
is_related_vassal_of = {
	is_vassal_of = $TARGET$
	is_close_family_of = $TARGET$
}

# Usage:
is_related_vassal_of = {
	TARGET = title:k_france.holder
}
```

Text replacement happens **before** evaluation. Same contextual pitfalls as scripted effects apply.

## Logical Operators Summary

| Name | Description | True when |
|------|-------------|-----------|
| `AND` | All triggers must be true | All children true |
| `OR` | At least one must be true | Any child true |
| `NOT` | Negation (use with single trigger) | Child is false |
| `NOR` / `all_false` | Negated OR | All children false |
| `NAND` / `any_false` | Negated AND | Any child false |
| `switch` | Switch on a trigger value | Matching case is true |
| `trigger_if` | Conditional check | Limit true → check triggers |
| `trigger_else_if` | Chained conditional | Previous limit false, this limit true |
| `trigger_else` | Fallback | All previous limits false |

### switch (trigger form)
```
switch = {
	trigger = has_culture
	culture:english = { <triggers> }
	culture:french = { <triggers> }
	fallback = { <triggers> }
}
```
