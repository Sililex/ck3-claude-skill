# Scopes — Full Reference

## Database Scope

Scope most often refers to a database object, and the database itself is referred to as the scope type (characters, titles, provinces, etc.).

Full list of scope types: generate with `script_docs` console command, see `event_scopes.log`.

See also `reference/events/_events.info` and `reference/common/character_interactions/_character_interactions.info`.

A database scope has three characteristics:
1. You can **read** information from it (triggers)
2. You can **write/modify** it (effects)
3. You can **move** from one to another

Some scopes are created on game start from history files, map data, or common folders. Some can be created at runtime in code (naturally born characters) or script (`create_character` effect, dynamic titles).

## Primitive Scope

Numbers, booleans (`yes`/`no`), and flag values (`flag:some_string`) are primitive scopes. They cannot be modified or accessed as objects. Understanding that "numbers are scopes" helps with advanced functionality and error logging.

## Top Scope

A top scope is a temporary abstract object created by the game to store information, mainly for retrieval in localization or GUI.

## Accessing Scopes

Effects and triggers execute in a **context**, and most work from specific scope types.

Example: `is_ai = no` only makes sense for a character scope. Using it on another scope type throws an error.

### root

Effect/trigger blocks often have a default context provided by code. `root` is a shortcut to that default context.

**`root` is NOT "the player"** — that's a common misconception. In multiplayer there are multiple players; `root` is simply the default context of the current block.

- In an event's `immediate` block, root = the character receiving the event
- Not all blocks have a root (e.g. character interactions don't — it would be ambiguous between sender/receiver)
- Root is not necessarily a character scope

### Context Switch

Change context by opening a new block with the target scope:

```
immediate = {
	# context = character receiving the event
	title:k_france = {
		# context = Kingdom of France
	}
	# context reverts to character
}
```

Nest as deep as needed. Each new block = one more tab of indentation.

Use `root` to jump back to the default context at any time:

```
immediate = {
	title:k_france = {
		# context = Kingdom of France
		root = {
			# context = character receiving the event
		}
	}
}
```

**Failed context switch**: Trying to switch to an invalid scope (e.g. typo `title:k_frnace`) fails silently or errors.

### Database Access

Scopes have unique keys/IDs, accessed with `<scope_type>:<scope_key>`:

- `title:k_france`
- `culture:english`
- `faith:orthodox`
- `character:123456`

**Characters have two IDs**: historical (predetermined in history files) and runtime (assigned on creation). Non-historical characters only have runtime IDs, which are not consistent across saves and **cannot be referenced in script**. Use saved scopes or list-builders to access them.

### Event Targets

Scopes with a unique relation from one to another are accessed through event targets. They are not prefixed (the game knows their scope type).

Full list: `event_targets.log`

Example from the log:
```
holder - Get holder of scoped title
Input Scopes: landed_title
Output Scopes: character
```

- **Output Scopes** = the scope type you get
- **Input Scopes** = the scope type you must be in to use it

Event targets can be chained with `.`:
```
title:k_france.holder = {
	# context = the character holding France
}
```

### this

`this` is the current scope. Useful for scope comparison or feeding the current scope as an argument.

### prev

`prev` is the previous scope (one step back). Useful for comparison, arguments, and inside list-builders.

```
title:k_france = {
	holder = {
		prev = {
			# context = title:k_france (one step back)
		}
	}
}
```

**Unlike CK2, `prev` cannot be chained.** There is no `prevprev`. Using `prev = { prev = {` goes back to the original scope (not two steps).

### Saved Scopes

An arbitrarily-named pointer to a specific scope: `scope:<name>`.

Can be saved by code (e.g. `scope:actor`, `scope:recipient` in interactions) or by script:

```
title:k_france.holder = {
	save_scope_as = king_of_france
}
scope:king_of_france = {
	# access the saved scope
}
```

**Key rules:**
- Saved scopes carry throughout an **unbroken effect chain** (e.g. event A fires event B, scope is accessible in B)
- Auto-cleared when the chain ends. Can be manually cleared with `clear_saved_scope`.
- `save_temporary_scope_as` can be used in both effect and trigger blocks, but expires at the end of the current block (does NOT carry through chains).
- A name can only be used once — saving with an existing name **overwrites** it.

**Passing saved scopes from UI:**
```
"[ScriptedGui.Execute( GuiScope.SetRoot( GetPlayer.MakeScope ).AddScope( 'target', CharacterWindow.GetCharacter.MakeScope ).End )]"
```

## List-Builders

Scopes with a **one-to-many** relation cannot use event targets (ambiguous). Instead, use list-builders.

Example: a character has one `mother` (event target), but a mother has multiple children — no `child` event target exists. Use `every_child`, `random_child`, etc.

### every_X (effect)

Accesses all scopes in the list, executes effects for each:

```
every_child = {
	add_gold = 10
}
```

With `limit` to filter:
```
every_child = {
	limit = { is_female = yes }
	add_gold = 10
}
```

Using `prev` to affect the parent scope:
```
every_child = {
	limit = { is_female = yes }
	prev = {
		add_gold = 10
	}
}
# current character gets 10 gold per female child
```

**Saving scopes in every_X**: only the **last** scope in the list is effectively saved (each iteration overwrites the saved scope).

### random_X (effect)

Picks one random scope from the list:

```
random_child = {
	limit = { is_female = yes }
	add_gold = 10
}
```

If list is empty or no scope meets the limit, effects are not executed.

**Common pattern** — save a random scope for later use:
```
random_child = {
	limit = {
		is_female = yes
		is_adult = yes
		is_married = no
	}
	save_scope_as = celibate_daughter
}
```

This is the main way to access non-historical characters (who can't be accessed by ID).

### ordered_X (effect)

Sorts the list by `order_by` and by default accesses the **first** scope (descending order):

```
ordered_child = {
	order_by = age
	add_gold = 10
}
# eldest child gets 10 gold
```

Additional parameters:
- **`position`** — access a specific index (0-based): `position = 1` = 2nd item
- **`min` / `max`** — iterate a range of indices
- **`check_range_bounds = no`** — avoid errors when range exceeds list size

```
ordered_child = {
	limit = { is_female = yes }
	order_by = age
	max = 2
	check_range_bounds = no
}
# the 3 eldest daughters get 10 gold, starting with oldest
```

**Warning**: in script math, `ordered_X` defaults to iterating through ALL scopes in order rather than just the first. This may be a bug.

### any_X (trigger)

Returns true if the enclosed triggers evaluate to true for **any** scope in the list:

```
any_child = {
	age > 10
}
# true if any child is older than 10
```

With `filter` to narrow the list:
```
any_child = {
	filter = { is_female = yes }
	age > 10
}
# true if any female child is older than 10
```

`save_temporary_scope_as` can save the first matching scope:
```
any_child = {
	filter = { is_female = yes }
	age > 10
	save_temporary_scope_as = teenage_daughter
}
```

**`count`** — require a specific number of matches:
```
any_child = {
	count >= 2
	is_female = yes
	age > 10
}
# true if at least 2 female children are older than 10
```

**`percent`** — require a portion of matches:
```
any_child = {
	percent >= 0.5
	is_female = yes
	age > 10
}
# true if at least half are female and older than 10
```

**Do NOT use `limit` inside `any_X`** — use `filter` instead. Do not use effects.

## Saved Scope Values

A saved scope value is a pointer to a **primitive scope** (number, boolean, flag), using the same `scope:<name>` syntax.

Saved with `save_scope_value_as`:
```
save_scope_value_as = {
	name = cost
	value = primary_heir.age
}
add_gold = scope:cost
```

Flag values:
```
save_scope_value_as = {
	name = kill_locale
	value = flag:tower
}
if = {
	limit = { scope:kill_locale = flag:tower }
	# ...
}
```

Same lifecycle rules as saved scopes (carry through effect chains, cleared at end).
