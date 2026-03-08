# Effects — Full Reference

## Effect Blocks

See also `reference/events/_events.info` and `reference/common/character_interactions/_character_interactions.info`.

Effects are executed in effect script blocks. These are either:
- Explicitly named: `effect = { }`
- Named by when they execute: `immediate = { }` (fires before event window opens), `after = { }` (fires after an option is picked)
- Triggered by game actions: `on_accept = { }` in character interactions (NOT the same as on_actions)

Some blocks are **hybrid** — they accept effects alongside other things:
```
option = {
	is_shown = { is_ai = yes }      # trigger block
	ai_will_do = { base = 100 }     # AI logic block
	add_gold = 100                   # effect
}
```

## Effect Syntax

### Code Effects

Code effects have predetermined syntax and usually require a specific scope type context.

Generate the full list: `script_docs` console command → `effects.log`

#### Boolean Form

Followed by `= yes`. Depends on the scope context, no other arguments.
```
release_from_prison = yes
```

#### Simple Form

Requires a single argument (scope, database key, or number):
```
marry = scope:bride
change_prison_type = house_arrest
add_gold = 1000
```

#### Complex Form

Uses multiple parameters in a block (booleans, scopes, database keys, numbers, flags):
```
imprison = {
	target = scope:imprisoned_character
	type = house_arrest
}
```

Some effects have both simple and complex forms.

## Scripted Effects

Macros that replace an assortment of effects with a single statement. Defined in `common/scripted_effects/`. Can use other scripted effects but **recursion is not allowed**.

### Simple Form

```
# Definition:
give_gold_prestige_piety = {
	add_gold = 1000
	add_prestige = 1000
	add_piety = 1000
}

# Usage:
give_gold_prestige_piety = yes
```

Because scripted effects can be used in many contexts, **avoid using ambiguous event targets like `root` or `prev` in their definitions**.

### Complex Form (Text Replacement / Parameters)

Arguments are defined with `$NAME$` in the definition and passed without `$` signs at usage:

```
# Definition:
give_gold_prestige_piety = {
	add_gold = $VALUE$
	add_prestige = $VALUE$
	add_piety = $VALUE$
}

# Usage:
give_gold_prestige_piety = { VALUE = 1000 }
```

**Text replacement is literal** — it happens before the scripted effect is evaluated. This has important implications when passing event targets or script values, because their interpretation is contextual.

Example of the pitfall:
```
# Definition:
give_gold = {
	$GIVER$ = {
		remove_short_term_gold = $VALUE$
		$TAKER$ = {
			add_gold = $VALUE$
		}
	}
}

# Usage — make father give money to mother:
give_gold = {
	GIVER = father
	TAKER = mother
	VALUE = 1000
}
```

After text replacement, this becomes:
```
father = {
	remove_short_term_gold = 1000
	mother = {
		add_gold = 1000
	}
}
```

The `mother` event target is now resolved in the context of the **father** scope (i.e., the father's mother), NOT the mother of the original character. This is because the literal text `mother` is placed inside the `father` block.

**Caution**: Always consider the scope context when passing event targets as arguments to scripted effects.
