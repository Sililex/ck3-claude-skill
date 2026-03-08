# Decisions Modding — Reference

Decisions are optional actions for count+ rulers and adventurers. Files go in `common/decisions/` as `.txt`.

See also `reference/common/decisions/_decisions.info` for the full spec.

## Basic Structure

```
my_decision = {
	picture = { reference = "gfx/interface/illustrations/decisions/decision_smith.dds" }

	desc = my_decision_desc
	selection_tooltip = my_decision_tooltip

	is_shown = {
		# conditions for decision to appear
	}

	is_valid = {
		# conditions to take it (shown under Requirements)
	}

	is_valid_showing_failures_only = {
		# conditions to take it (only failures shown in tooltip)
	}

	cost = {
		gold = 100
		prestige = 50
		piety = 0        # default 0, can omit
	}

	effect = {
		add_gold = 100
	}

	ai_check_interval = 120   # months between AI checks (0 = AI never checks)
	ai_potential = { always = yes }
	ai_will_do = { base = 100 }  # % chance AI takes it
}
```

## All Keys/Blocks

| Key | Type | Description |
|-----|------|-------------|
| `picture` | block | Image + optional sound. Multiple with triggers for conditional display |
| `extra_picture` | string | Extra image (used by Struggle decisions) |
| `decision_group_type` | string | Foldable group type (defined in `common/decision_group_types/`, see `reference/common/decision_group_types/_decision_group_types.info`) |
| `sort_order` | int | Higher = appears higher in list |
| `is_invisible` | bool | Hidden decision |
| `cooldown` | block | `{ years = 5 }` / `{ months = 6 }` / `{ days = 30 }` |
| `confirm_click_sound` | string | Sound on confirm |
| `title` | loc key/block | Override decision title (default: decision name) |
| `desc` | loc key/block | Override description (default: `_desc` suffix) |
| `selection_tooltip` | loc key/block | Override tooltip (default: `_tooltip` suffix) |
| `confirm_text` | loc key/block | Override confirm button text (default: `_confirm` suffix) |
| `is_shown` | trigger | When decision appears |
| `is_valid` | trigger | Can take? Shown under Requirements |
| `is_valid_showing_failures_only` | trigger | Can take? Only failures shown |
| `cost` | block | `gold`, `prestige`, `piety` (values can be script values) |
| `minimum_cost` | block | Like cost, but not deducted — just checks affordability |
| `effect` | effect | What happens when taken |
| `ai_goal` | bool | AI budgets for this (ignores `ai_check_interval`) |
| `ai_check_interval` | int | Months between AI checks (0 = never). Required unless `ai_goal = yes` |
| `ai_potential` | trigger | Whether AI considers this |
| `ai_will_do` | block | % chance AI takes it (0–100) |
| `should_create_alert` | trigger | Suppress player notification when false |
| `widget` | block | Custom GUI widget (see below) |

## Localization

Four entries needed (using decision name as prefix):

```yaml
l_english:
 my_decision: "My Decision Name"
 my_decision_desc: "Description shown when opened"
 my_decision_tooltip: "Tooltip when hovering"
 my_decision_confirm: "Confirm button text"
```

Override defaults with `title`, `desc`, `selection_tooltip`, `confirm_text` keys in the decision.

## File-level Values

Define reusable constants at the top of the file with `@`:

```
@sale_of_titles_prestige_cost = 500

sale_of_titles_decision = {
	cost = {
		prestige = @sale_of_titles_prestige_cost
	}
}
```

## Custom Widgets

Add to `gui/decision_view_widgets/` (filename must match widget name).

```
widget = {
	gui = "decision_view_widget_commission_artifact"
	controller = decision_option_list_controller

	item = {
		value = option_name
		is_shown = { ... }
		is_valid = { ... }
		current_description = { desc = ... }
		localization = { desc = ... }
		icon = "gfx/interface/icons/artifact/kris.dds"
		ai_chance = { value = 5000 }
	}
}
```

**Important**: The `default` controller doesn't work. Use `create_holy_order` or `decision_option_list_controller`.

## Testing

Remove cooldown during testing:
```
effect remove_decision_cooldown = my_decision
```

## Finding Decision IDs

Search localization for the name → find the key. Convention: lowercase, spaces → `_`, append `_decision`.

Example: "Commission Artifact" → `commission_artifact_decision`

Some don't follow convention (e.g. "Call Hunt" → `start_hunt`, "Search for Physician" → `hire_physician`).
