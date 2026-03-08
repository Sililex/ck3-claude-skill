# Variables — Full Reference

See also `reference/events/_events.info`.

Variables store information permanently until removed.

## Setting a Variable

Set with `set_variable` on the scope in the current context:

```
set_variable = {
	name = X
	value = Y
}
```

The name is an arbitrary string — setting a variable defines it (no predefined list).

### Value types

**Boolean** — simple form shorthand:
```
set_variable = X
# equivalent to:
set_variable = { name = X value = yes }
# on a character, also equivalent to:
add_character_flag = X
```

**Number** — arbitrary decimal:
```
set_variable = { name = test value = 2.37 }
```

Calculated dynamically with script math:
```
set_variable = {
	name = test
	value = {
		value = 5
		add = 2
		multiply = 3
	}
}
```

Or set to a script value:
```
set_variable = { name = test value = some_script_value }
```

Most triggers that compare against a number (support `<`, `<=`, `=`, `!=`, `>`, `>=`) can also be used as values:
```
set_variable = { name = test value = prestige }
set_variable = { name = test value = "culture.cultural_acceptance(culture:french)" }
```

**Flag value**:
```
set_variable = { name = test value = flag:some_flag }
```

**Scope** — stores a pointer (not a copy) to a scope:
```
set_variable = { name = test value = scope:some_scope }
```

Any means of accessing a scope works here: database access, event targets, etc.

## Modifying a Variable

Setting a variable with the same name **replaces** the existing one (even if different type).

For numerical variables, use `change_variable`:
```
change_variable = {
	name = X
	add = Y        # or multiply = Y
}
```

## Removing a Variable

Variables persist until:
- Manually removed in script
- The scope they're stored on is destroyed
- If stored on a character, when the character dies

**Remove when no longer useful** to avoid savegame bloat:
```
remove_variable = X
```

## Accessing a Variable

Variables are accessed from the scope they were set on, using `var:<name>`.

Check existence first with `has_variable` trigger.

**Chaining** — chain to the scope it's stored on:
```
scope:some_scope.var:some_var
```

If the variable stores a scope, event targets can be chained off it:
```
scope:some_scope.var:some_var.father
```

Variables storing scopes can chain to other variables:
```
scope:some_scope.var:some_var.var:other_var
```

## Global Variables

Set on the gamestate itself, accessible from any context:

| Operation | Effect |
|-----------|--------|
| Set | `set_global_variable` |
| Change | `change_global_variable` |
| Remove | `remove_global_variable` |
| Access | `global_var:some_global_var` |
| Check existence | `has_global_variable` |

Otherwise works identically to normal variables.

## Local Variables

Set on a **top scope** (a temporary abstract object), accessible from any context within that same top scope. Because top scopes are temporary, local variables are much less permanent than regular variables. In most cases, using a saved scope or saved scope value is more practical.

| Operation | Effect |
|-----------|--------|
| Set | `set_local_variable` |
| Change | `change_local_variable` |
| Remove | `remove_local_variable` |
| Access | `local_var:some_local_var` |
| Check existence | `has_local_variable` |

Useful as counters or temporary state during complex effect chains.

## Dead Character Variables

Variables that persist on dead characters. Require a `days` duration parameter (for performance):

| Operation | Effect |
|-----------|--------|
| Set | `set_dead_character_variable` (requires duration) |
| Access | `dead_var:some_var` |

No `change_` effect exists for dead character variables.

## Summary Table

| Type | Set | Access | Change | Remove | Stored on | Lifetime |
|------|-----|--------|--------|--------|-----------|----------|
| Normal | `set_variable` | `var:` | `change_variable` | `remove_variable` | Scope object | Until removed or scope destroyed |
| Global | `set_global_variable` | `global_var:` | `change_global_variable` | `remove_global_variable` | Gamestate | Until removed |
| Local | `set_local_variable` | `local_var:` | `change_local_variable` | `remove_local_variable` | Top scope (temporary) | When top scope ends |
| Dead | `set_dead_character_variable` | `dead_var:` | N/A | N/A | Dead character | Duration specified |

## Displaying in UI / Localization

- Normal variable: `[GetPlayer.MakeScope.Var('test').GetValue]`
- Global variable: `[GetGlobalVariable('test').GetValue]`
- If variable stores a character: use `GetCharacter` instead of `GetValue`
- Script values (not variables): `[GetPlayer.MakeScope.ScriptValue('my_value')]` (no `GetValue`)
