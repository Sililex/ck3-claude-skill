# Story Cycles Modding — Reference

A story cycle is an event manager that fires events periodically and stores related values. Can also be used purely as persistent variable storage that survives character death.

Defined in `common/story_cycles/`. See `reference/common/story_cycles/_story_cycles.info`.

## Creating a Story Cycle

Create in script with: `create_story = story_cycle_name`

The owner is the character in whose context the effect runs.

## Structure

```
story_cycle_name = {
	on_setup = { }
	on_end = { }
	on_owner_death = { }

	effect_group = {
		days = 30              # or months/years. Range: days = { 30 60 }

		trigger = { }          # optional: group-level trigger

		triggered_effect = {
			trigger = { }      # optional: effect-level trigger
			effect = { }
		}

		triggered_effect = { } # multiple allowed per group
	}

	effect_group = { }         # multiple groups allowed
}
```

## Blocks

### on_setup

Runs when the story is created. Effects apply to the **story scope** by default. Use `story_owner` to affect the owner:

```
on_setup = {
	story_owner = {
		trigger_event = my_event.1
	}
}
```

### on_end

Runs when the story ends. A story ends via `end_story = yes` (manually in script, or automatically on owner death).

### on_owner_death

Runs when the owner dies (while they're still alive, like `on_death` on_action). Common patterns:

- End the story: `end_story = yes` (also triggers `on_end`)
- Transfer to heir: `make_story_owner = story_owner.primary_heir`
- Copy variables to heir before ending

### effect_group

A repeating pulse that fires every X days/months/years.

- `days = 30` — fixed interval
- `days = { 30 60 }` — random range
- `chance = 50` — percentage chance of firing (1–100)
- `trigger = { }` — group-level condition
- `triggered_effect` — has its own trigger + effect. Multiple allowed.

### first_valid in effect_group

Pick the first triggered_effect whose trigger passes:

```
effect_group = {
	days = 30
	first_valid = {
		triggered_effect = {
			trigger = { }     # checked first
			effect = { }
		}
		triggered_effect = {
			trigger = { }     # checked if first fails
			effect = { }
		}
		triggered_effect = {  # fallback
			effect = { }
		}
	}
}
```

## Common Patterns

### Passing Variables to a Story

Variables can't be directly set on a story before it exists. Use a passthrough pattern:

```
# Before creating the story, set temp variables on the owner:
set_variable = { name = revealer_passthrough value = scope:revealer }
create_story = my_story

# In the story's on_setup:
on_setup = {
	set_variable = {
		name = revealer
		value = story_owner.var:revealer_passthrough
	}
	story_owner = { remove_variable = revealer_passthrough }
}
```

### Persistent Storage

Story cycles persist after character death if not explicitly ended. Useful for storing variables and lists that need to outlive a character. End with `end_story = yes` when no longer needed.

### AI Behavior Driver

Story cycles can drive complex AI behavior by periodically calling large scripted effects (see the conqueror AI pattern in `ai.md`).
