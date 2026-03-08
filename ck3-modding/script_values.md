# Script Values — Reference

Script values are functions that calculate a value. Usable almost anywhere in script. Defined in `common/script_values/` as `.txt` files.

See `reference/common/script_values/_script_values.info`.

## Simple Values

```
minor_stress_gain = 20
```

Used: `add_stress = minor_stress_gain`

## Formulas

```
sum_of_all_skills_value = {
	add = intrigue
	add = diplomacy
	add = stewardship
	add = martial
	add = learning
}
```

### All Operators

```
name = {
	value = ...          # set the value
	add = ...
	subtract = ...
	multiply = ...
	divide = ...         # careful: don't divide by 0
	modulo = ...

	max = ...            # cap: set to this if currently higher
	min = ...            # floor: set to this if currently lower

	round = yes          # nearest whole number
	ceiling = yes        # round up (toward +infinity)
	floor = yes          # round down (toward -infinity)

	if = {
		limit = { ... }
		add = 5
	}
	else_if = {
		limit = { ... }
		multiply = 2
	}
	else = {
		subtract = 1
	}

	fixed_range = {      # random fixed-point number
		min = ...
		max = ...
	}
	integer_range = {    # random integer
		min = ...
		max = ...
	}
}
```

**Script values cannot change gamestate** — no setting variables, no executing most effects.

Scope matters: a province won't have `age`.

## Execution Order

Operations execute **in order defined**:

```
value = {
	add = 5       # 5
	multiply = 4  # 20
	max = 10      # 10 (capped)
	add = 5       # 15
}
# result: 15
```

## Inlining

Formulas can be written inline wherever script values work — no need to name them if used once:

```
add_gold = {
	value = gold
	multiply = {
		value = 1
		multiply = 0.5
	}
}
```

## Chaining

Named script values can be scope-chained:

```
# Definition:
example_age = { value = age }

# Usage:
add_gold = {
	value = mother.example_age
}
```

## Ranges

```
add_gold = { 1 5 }                              # random 1-5
add_gold = { named_value another_named_value }   # resolve named values
```

Cannot inline formulas in ranges. Use `integer_range` / `fixed_range` instead.

## Lists in Script Values

`every_` and `ordered_` lists work:

```
add_gold = { every_child = { add = 1 } }    # gold = number of children

add_gold = {
	ordered_child = {
		order_by = age
		max = 3
		add = age
	}
}
```

**Do NOT use `any_` lists** — those are for triggers only.

## Scoping

Change scope within script values same as regular script:

```
add_gold = {
	father = {
		every_child = { add = 1 }
	}
}
# adds gold = number of father's children
```

## Saving Current Value

Use `save_temporary_value_as` to capture the current value mid-calculation:

```
temp = {
	add = 10
	divide = 2
	save_temporary_value_as = temp_total
	multiply = scope:temp_total
}
# result: 25 ((10/2) * (10/2) = 5 * 5)
```

Useful for:
- Avoiding recalculating expensive values
- Branching based on whether current value is positive/negative

## Displaying in UI

**Character scope** (player as root):
```
text_single = {
	raw_text = "[GetPlayer.MakeScope.ScriptValue('my_value')]"
}
```

**No scope needed**:
```
"[EmptyScope.ScriptValue('my_value')]"
```

**Passing scopes from UI**:
```
"[GuiScope.SetRoot( GetPlayer.MakeScope ).AddScope( 'target', CharacterWindow.GetCharacter.MakeScope ).ScriptValue('sval_name')]"
```

**Performance warning**: UI recalculates script values **every frame**. Complex script values in UI cause massive lag. Consider setting variables equal to the script value and displaying the variable instead.
