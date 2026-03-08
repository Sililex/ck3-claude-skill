# Event Modding — Reference

Events are the core of most mods. See also `reference/events/_events.info` and `reference/common/on_action/_on_actions.info`.

## Checklist

Events must:
1. Be in `your_mod/events/` folder (subdirectories allowed)
2. Have a `.txt` extension
3. Have a `namespace` on the first line
4. Use `namespace.number` as their ID (e.g. `my_events.1`)
5. Be fired from script (on_action, decision, interaction, story cycle, etc.)

**Events do NOT fire automatically.** They must be triggered.

**Max ID per namespace: 9999** — beyond this the event calling system becomes buggy.

## Minimal Event

```
namespace = example

example.1 = {
	desc = example.1.desc

	option = {
		name = example.1.a
	}
}
```

Test with console: `event example.1`

## Flags (Top-Level)

| Flag | Values | Description |
|------|--------|-------------|
| `type` | `character_event`, `letter_event`, `duel_event`, `none`, `empty` | Scope type of root. `empty` for characterless events. Default: `character_event` |
| `hidden` | `true`/`false` | Hidden events run in background, no window shown |

## Portraits

### Positions

| Position | Description |
|----------|-------------|
| `left_portrait` | Left side |
| `right_portrait` | Right side |
| `lower_left_portrait` | Lower left |
| `lower_center_portrait` | Lower center |
| `lower_right_portrait` | Lower right |

### Portrait Parameters

```
left_portrait = {
	character = scope:target
	animation = fear
	triggered_animation = {
		trigger = { has_trait = brave }
		animation = anger
	}
	triggered_outfit = {
		trigger = { }
		outfit_tags = { western_stealth_hood }
		remove_default_outfit = no    # yes = disable unmatched categories
		hide_info = no                # yes = no CoA/tooltips/clicks
	}
	hide_info = yes/no
}
```

Short form: `left_portrait = root`

**Warning**: Characters with certain genetic traits (gigantism, dwarfism) have different models. Assigning their animations to normal characters may crash.

### Animation IDs

Common animations:
- Emotions: `idle`, `anger`, `rage`, `fear`, `sadness`, `shame`, `shock`, `worry`, `grief`, `happiness`, `ecstasy`, `love`, `stress`, `boredom`
- Reactions: `disapproval`, `disbelief`, `disgust`, `dismissal`, `admiration`, `schadenfreude`, `paranoia`
- Social: `flirtation`, `flirtation_left`, `beg`, `laugh`, `eyeroll`, `eavesdrop`
- Physical: `pain`, `poison`, `sick`, `severelywounded`, `pregnant`, `incapable`, `dead`, `crying`
- Combat: `aggressive_sword`, `aggressive_axe`, `aggressive_mace`, `aggressive_dagger`, `aggressive_spear`, `aggressive_hammer`, `celebrate_sword`, etc.
- Personality: `personality_honorable`, `personality_dishonorable`, `personality_bold`, `personality_coward`, `personality_greedy`, `personality_content`, `personality_vengeful`, `personality_forgiving`, `personality_rational`, `personality_irrational`, `personality_compassionate`, `personality_callous`, `personality_zealous`, `personality_cynical`
- Council: `chancellor`, `steward`, `marshal`, `spymaster`, `chaplain`
- Activities: `scheme`, `toast`, `drink`, `feast`, `prayer`, `dancing`, `reading`, `writing`, `thinking`
- Throne room: `throne_room_ruler`, `throne_room_kneel_1`, `throne_room_bow_1`, `throne_room_curtsey_1`, etc.

## Themes

Themes bundle background, lighting, and sound. Defined in `common/event_themes/`. See `reference/common/event_themes/_event_themes.info`.

Common themes: `diplomacy`, `intrigue`, `martial`, `stewardship`, `learning`, `family`, `war`, `death`, `marriage`, `love`, `seduction`, `dread`, `faith`, `realm`, `dungeon`, `prison`, `feast_activity`, `hunt_activity`, `medicine`, `mental_break`, `mental_health`, `physical_health`, `secret`, `dynasty`, `culture_change`, `party`, `pet`, `skull`, `witchcraft`

Override individual elements: `override_background`, `override_icon`, `override_sound`, `override_environment`.

### Backgrounds

See `reference/common/event_backgrounds/_event_backgrounds.info` for the full list.

Common: `alley_day`, `alley_night`, `armory`, `army_camp`, `battlefield`, `bedchamber`, `corridor_day`, `corridor_night`, `council_chamber`, `courtyard`, `docks`, `dungeon`, `farmland`, `feast`, `gallows`, `garden`, `market`, `physicians_study`, `sitting_room`, `study`, `tavern`, `temple`, `throne_room`, `wilderness`, `wilderness_desert`, `wilderness_forest`, `wilderness_mountains`, `wilderness_steppe`

## Trigger

Checked before the event fires. **Cannot use scopes created in `immediate`** — those don't exist yet.

```
trigger = {
	any_held_county = {
		any_county_province = {
			has_building_or_higher = blacksmiths_01
		}
	}
	trigger_if = {
		limit = { has_trait = greedy }
		gold > 500
	}
	trigger_else = {
		piety > 50
		gold > 10
	}
}
```

To check against specific characters, use list-builders in the trigger:
```
trigger = {
	any_knight = {
		has_trait = brave
	}
}
```

### on_trigger_fail

Effect block that runs when a queued event's trigger fails (not for on_action failures).

## Description

Can be literal text (produces error log warning) or localization keys.

### Dynamic Descriptions

**`first_valid`** — picks first matching desc:
```
desc = {
	first_valid = {
		triggered_desc = {
			trigger = { has_trait = drunkard }
			desc = my_event.0001.desc.drunkard
		}
		desc = my_event.0001.desc.fallback    # always valid
	}
}
```

**`random_valid`** — picks random matching desc:
```
desc = {
	random_valid = {
		desc = my_event.0001.random_1
		desc = my_event.0001.random_2
		triggered_desc = {
			trigger = { is_female = yes }
			desc = my_event.0001.random_3
		}
	}
}
```

**Combining** — nest `random_valid` inside `first_valid` for curated randomization.

**Concatenation** — multiple `desc` blocks outside `first_valid`/`random_valid` are concatenated with a space between them. Watch for misplaced spaces (e.g. `"word ,"` vs `"word,"`). Use en-dash (` – `) instead of em-dash (`—`) to hide join points.

### Dynamic Option Names

Options use `text` wrapper between `name` and `first_valid`:
```
option = {
	name = {
		text = {
			first_valid = {
				triggered_desc = {
					trigger = { is_female = yes }
					desc = my_event.0001.a.female
				}
				desc = my_event.0001.a.fallback
			}
		}
	}
}
```

Alternative simpler syntax:
```
name = {
	trigger = { has_trait = brave }
	text = my_event.0001.a.brave
}
```

### Flavor Text

Uses same desc syntax directly (no `text` wrapper needed):
```
flavor = {
	first_valid = {
		triggered_desc = {
			trigger = { is_female = yes }
			desc = my_event.0001.a.flavor.female
		}
		desc = my_event.0001.a.flavor.fallback
	}
}
```

## Immediate

Effect block that runs **before** the event window is rendered. Used for:
- Saving scopes needed by descriptions/portraits
- Setting variables
- Effects that should happen regardless of option chosen

```
immediate = {
	random_courtier = {
		limit = { is_adult = yes }
		save_scope_as = chosen_courtier
	}
}
```

## Options

Each option is an effect block with additional keys:

| Key | Required | Description |
|-----|----------|-------------|
| `name` | Yes | Localization key for button text |
| (effects) | No | Effects written directly in the option block |
| `trigger` | No | Option only available if true |
| `show_as_unavailable` | No | Show disabled option if this trigger passes |
| `trait` | No | Show trait icon on option (flavor only) |
| `skill` | No | Show skill icon on option (flavor only) |
| `add_internal_flag` | No | `special` = yellow highlight, `dangerous` = red highlight (flavor only) |
| `highlight_portrait` | No | Highlight a portrait on hover |
| `fallback` | No | Show this option if no other options meet triggers |
| `exclusive` | No | If true and triggers met, only this option (and other passing exclusives) shown |
| `flavor` | No | Flavor text in tooltip (loc key or dynamic desc) |
| `ai_chance` | No | AI weighting (see `ai.md`) |

```
option = {
	name = my_event.1.a
	trigger = { has_trait = brave }
	add_internal_flag = dangerous
	trait = brave
	add_gold = -100
	ai_chance = {
		base = 50
		modifier = { add = 50 has_trait = brave }
	}
}
```

## After

Effect block that runs **after** an option is chosen. Same syntax as `immediate`. Does nothing for hidden events (no options). Commonly used for cleanup:

```
after = {
	if = {
		limit = { NOT = { exists = scope:keep_character } }
		scope:temp_character = { silent_disappearance_effect = yes }
	}
}
```

## On Actions

Defined in `common/on_action/` (singular, NOT `on_actions`). See `reference/common/on_action/_on_actions.info`.

### Firing Events from On Actions

```
on_birth_child = {
	events = {
		my_event.1
	}
}
```

### Appending Safely

**Effects and triggers cannot be appended directly** — only events and on_actions. To add effects without overwriting vanilla:

```
# In your own file:
on_birth_child = {
	on_actions = {
		my_custom_on_action
	}
}

my_custom_on_action = {
	trigger = { ... }
	effect = { ... }
}
```

**This overwrites vanilla** (DON'T do this):
```
on_birth_child = {
	trigger = { ... }    # OVERWRITES vanilla trigger
	effect = { ... }     # OVERWRITES vanilla effect
}
```

### Common On Actions

| On Action | When | Root Scope |
|-----------|------|------------|
| `on_birth_child` | Child born | Character |
| `on_16th_birthday` | Becomes adult | Character |
| `on_death` | Before character dies | Character |
| `on_game_start` | Game start (before char select) | None |
| `on_game_start_after_lobby` | After char select | None |
| `random_yearly_playable_pulse` | Once/year, random date, count+ | Character |
| `quarterly_playable_pulse` | Every 3 months, count+ | None |
| `yearly_playable_pulse` | Every year on birthday, count+ | Character |
| `yearly_global_pulse` | Every Jan 1st | None |
| `random_yearly_everyone_pulse` | Once/year, all characters | Character |
| `five_year_everyone_pulse` | Every 5 years, all characters | Character |
| `three_year_pool_pulse` | Every 3 years, pool characters | Character |

**No monthly on_action exists** (performance). Workaround: use `quarterly_playable_pulse` with delays:
```
on_actions = {
	my_on_action
	delay = { months = 1 }
	my_on_action
	delay = { months = 2 }
	my_on_action
}
```

### Scope Warnings

- `on_game_start` has no root — use global effects like `every_ruler`
- `yearly_playable_pulse` already fires for every playable character — **do NOT use `every_living_character` inside it** (20000² operations = massive lag)
- Always check comments in on_action files for available scopes

### On Action Properties

| Property | Description |
|----------|-------------|
| `trigger` | Must be true for on_action to fire |
| `weight_multiplier` | Weight in `random_on_actions` lists |
| `events` | Events that always fire (supports `delay`) |
| `random_events` | Pick one weighted event (`chance_to_happen`, `chance_of_no_event`, weights) |
| `first_valid` | First event whose trigger passes |
| `on_actions` | Fire other on_actions |
| `random_on_actions` | Pick one weighted on_action |
| `first_valid_on_action` | First on_action whose trigger passes |
| `effect` | Run effects (concurrent with events, NOT before — separate chain) |
| `fallback` | On_action to call if nothing fires (avoid infinite loops!) |

### Calling On Actions from Script

```
trigger_event = { on_action = my_on_action }
```

## Strategy

### Triggering Events

Events must be explicitly fired. Common methods:
- **On actions** — respond to game events
- **Decisions** — player-initiated
- **Character interactions** — between characters
- **Story cycles** — periodic/conditional firing
- **Other events** — `trigger_event = { id = my_event.2 days = { 7 14 } }`
- **Console** — `event my_event.1` (testing)
