# Struggles Modding — Reference

Struggles are multi-phase regional systems with involved cultures/faiths, catalysts that drive phase transitions, and per-phase modifiers/parameters.

Defined in `common/struggle/struggles/`. Catalysts in `common/struggle/catalysts/`. See `reference/common/struggle/struggles/_struggles.info`, `reference/common/struggle/catalysts/_catalysts.info`.

## Setup

### Cultures and Faiths

Specify which cultures/faiths are involved (not interlopers):

```
cultures = {
	persian
	kurdish
	bedouin
}
faiths = {
	ashari
	zayidi
	mazdayasna
}
```

### Regions

```
regions = {
	world_persian_empire
	ghw_region_kurdistan
}
```

### Involvement Prerequisite

How cultures/faiths not in the initial list can become involved:

```
involvement_prerequisite_percentage = 0.8
```

A culture/faith becomes involved if 80% of its total counties are inside the struggle region. This is currently the **only** automatic involvement mechanism (others require decisions/events).

**Implication**: if a culture/faith has more than `(1 - percentage) × total_struggle_counties` counties outside the region, it can never auto-involve.

### Graphics

- Phase backgrounds: `gfx/interface/illustrations/struggle_backgrounds/` — auto-load if named `custom_struggle_phase_bg.dds`
- Phase icons: set in `gui/texticons.gui` and game concepts

Game concept example:
```
struggle_phase_custom_1 = {
	texture = "gfx/interface/icons/struggle_types/struggle_custom_phase_1.dds"
	parent = custom_struggle
	requires_dlc_flag = the_fate_of_iberia
}
```

Texticon example:
```
texticon = {
	icon = struggle_custom_phase_1
	iconsize = {
		texture = "gfx/interface/icons/struggle_types/struggle_custom_phase_1.dds"
		size = { 25 25 }
		offset = { 0 6 }
		fontsize = 16
	}
}
```

## Starting the Struggle

### on_start / on_join

```
on_start = {
	trigger_event = neutral_struggle.0001
	trigger_event = {
		id = fp3_struggle.0001
		years = { 1 5 }
	}
}

on_join = {
	# root = character joining the struggle
	if = {
		limit = { ... }
		add_trait = fp3_struggle_supporter
	}
	else_if = {
		limit = { ... }
		add_trait = fp3_struggle_detractor
	}
}
```

### Triggering at Game Start

The `on_start` section in the struggle script often doesn't work reliably. Many modders trigger starting events via a scripted effect instead:

```
enable_custom_struggle_effect = {
	start_struggle = {
		struggle_type = custom_struggle
		start_phase = struggle_custom_phase_1
	}
	struggle:custom_struggle ?= {
		trigger_event = { on_action = custom_struggle_starting_events }
	}
}
```

Call from `on_game_start` on_action:
```
on_game_start = {
	effect = {
		enable_custom_struggle_effect = yes
	}
}
```

## Phases

Every struggle needs at least one phase plus ending phase(s).

```
phase_list = {
	struggle_phase_1 = {
		duration = { points = 500 }

		future_phases = {
			struggle_phase_2 = {
				catalysts = {
					catalyst_key_1 = major_struggle_catalyst_gain
					catalyst_key_2 = minor_struggle_catalyst_gain
				}
			}
			struggle_ending_phase = {
				catalysts = {
					catalyst_passing_of_time = catalyst_yearly_time_out_value
				}
			}
		}

		war_effects = { ... }
		faith_effects = { ... }
		culture_effects = { ... }
		other_effects = { ... }

		ending_decisions = {
			my_ending_decision_1
			my_ending_decision_2
		}
	}
}
```

### Phase Effects

Four categories: `war_effects`, `culture_effects`, `faith_effects`, `other_effects`. Each can have:

| Attribute | Description |
|-----------|-------------|
| `name` | Localization key for tooltip grouping |
| `common_parameters` | Affects everyone in the struggle |
| `involved_parameters` | Affects involved characters |
| `interloper_parameters` | Affects interlopers |
| `uninvolved_parameters` | Affects uninvolved |
| `involved_character_modifier` | Character modifiers on involved |
| `interloper_character_modifier` | Character modifiers on interlopers |
| `involved_doctrine_character_modifier` | Modifier if involved + has doctrine |
| `interloper_doctrine_character_modifier` | Modifier if interloper + has doctrine |
| `all_county_modifier` | County modifiers on all involved counties |
| `involved_county_modifier` | County modifiers on involved counties held by involved chars |
| `interloper_county_modifier` | County modifiers on involved counties held by interlopers |
| `uninvolved_county_modifier` | County modifiers on involved counties held by uninvolved chars |

Example:
```
war_effects = {
	name = WAR_EFFECTS_NAME
	common_parameters = {
		invasion_conquest_war_cannot_be_declared = yes
	}
	involved_character_modifier = {
		men_at_arms_recruitment_cost = -0.5
		men_at_arms_maintenance = -0.25
	}
	interloper_character_modifier = {
		men_at_arms_recruitment_cost = -0.25
	}
}
```

**Note on parameters**: Some parameters (like `caliph_cant_be_dissolutioned`) don't do anything themselves — they're just for tooltips. The actual logic must be handled separately (e.g. manually setting/clearing variables on titles). This is done for performance.

## Catalysts

Defined in `common/struggle/catalysts/`. Drive phase transitions by accumulating points.

### Defining Catalysts

Catalysts are referenced in `future_phases` with a script value for their point contribution:

```
future_phases = {
	next_phase = {
		catalysts = {
			catalyst_passing_of_time = minor_struggle_catalyst_gain
			catalyst_war_ends_white_peace = major_struggle_catalyst_gain
		}
	}
}
```

### Localization

```yaml
l_english:
 catalyst_passing_of_time:1 "Yearly Drift [struggle_catalyst_catalyst|E]"
 catalyst_passing_of_time_desc:2 "Yearly Drift: natural flow towards this [struggle_phase|E]"
```

### Catalyst Values

Typically defined as script values in `common/script_values/`. Vanilla examples use tiered values (minimal, minor, medium, major).
