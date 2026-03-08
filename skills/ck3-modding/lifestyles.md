# Lifestyles Modding — Reference

Lifestyles are the progression trees characters can invest in. Three layers: **lifestyles** → **focuses** → **perks**.

See `reference/common/lifestyles/_lifestyles.info`, `reference/common/focuses/_focuses.info`, `reference/common/lifestyle_perks/_lifestyle_perks.info`.

## Lifestyles

Defined in `common/lifestyles/`.

```
learning_lifestyle = {
	is_highlighted = {
		has_trait = education_learning
	}
	is_valid = {
		has_dlc_feature = wandering_nobles
	}
	xp_per_level = 1000
	base_xp_gain = 25
}
```

| Attribute | Type | Description |
|-----------|------|-------------|
| `is_highlighted` | trigger | Highlight the lifestyle (e.g. matching education) |
| `is_valid` | trigger | Can this lifestyle be selected |
| `is_valid_showing_failures_only` | trigger | Same, but only shows failures |
| `xp_per_level` | number | XP needed per perk point |
| `base_xp_gain` | number | Monthly XP before modifiers |
| `icon` | string | Icon key (default: lifestyle key) |

**Trigger restriction**: Lifestyle triggers cannot use scripted triggers/effects/modifiers, or triggers generated from scripted content (e.g. `diplomacy_lifestyle_perk_points`, `has_relation_rival`).

### Localization
- `<LIFESTYLE>_name` — name
- `<LIFESTYLE>_desc` — description
- `<LIFESTYLE>_highlight_desc` — description when highlighted

### Graphics
Icons: `gfx/interface/icons/lifestyles/<KEY>.dds`

## Focuses

Defined in `common/focuses/`. Two types: `lifestyle` (adult) and `education` (children).

```
learning_scholarship_focus = {
	lifestyle = learning_lifestyle
	type = lifestyle              # or "education"

	is_shown = {
		NOT = { government_has_flag = government_is_landless_adventurer }
	}
	is_valid = { ... }

	desc = {
		desc = learning_scholarship_focus_desc
		desc = line_break
	}

	modifier = {
		learning = 3
		development_growth_factor = 0.15
	}

	auto_selection_weight = {
		value = 11
		if = {
			limit = { has_education_learning_trigger = yes }
			add = 1989
		}
	}
}
```

| Attribute | Type | Description |
|-----------|------|-------------|
| `type` | `lifestyle`/`education` | Education focuses are for children |
| `lifestyle` | key | Which lifestyle (required if type = lifestyle) |
| `is_shown` | trigger | Is focus visible |
| `is_valid` | trigger | Can character choose this |
| `is_valid_showing_failures_only` | trigger | Same, only failures shown |
| `is_good_for` | trigger | Good education focus for child (education type) |
| `is_bad_for` | trigger | Bad education focus for child (education type) |
| `is_default` | trigger | Default education focus (education type) |
| `on_change_to` | effect | Runs when changing to this focus |
| `on_change_from` | effect | Runs when changing away |
| `on_birthday` | effect | Runs on birthday if above min age |
| `modifier` | block | Modifiers applied to character with this focus |
| `skill` | enum | Related skill (education type) |
| `auto_selection_weight` | script value | AI selection weight / initial focus selection |
| `desc` | dynamic desc | Description in UI |
| `icon` | string | Override icon key |

### Localization
- `<KEY>` — focus name
- `<KEY>_modifier` — modifier name
- `<KEY>_desc` — description
- `<KEY>_effect_desc` — effect description

### Graphics
- Focus icons: `gfx/interface/icons/focuses/<KEY>.dds`
- Tree backgrounds: `gfx/interface/icons/lifestyle_tree_backgrounds/`

## Perks

Defined in `common/lifestyle_perks/`.

```
scholarly_circles_perk = {
	lifestyle = learning_lifestyle
	tree = scholarship
	position = { 2 2 }            # GUI position (multiplied by PERK_X/Y_OFFSET)
	icon = node_learning

	parent = planned_cultivation_perk    # required to unlock
	# parent = other_perk               # multiple parents allowed

	can_be_picked = { always = yes }

	trait = scholar                      # trait shown in hover tooltip

	effect = {
		add_trait_force_tooltip = scholar
	}

	character_modifier = {
		different_faith_opinion = 15
		faith_conversion_piety_cost_mult = -0.75
	}

	auto_selection_weight = { value = 1000 }
}
```

| Attribute | Type | Description |
|-----------|------|-------------|
| `lifestyle` | key | Which lifestyle |
| `tree` | key (focus) | Which tree (GUI layout only) |
| `position` | `{ x y }` | Position in tree (GUI only) |
| `icon` | string | Icon key (default: perk key) |
| `parent` | key | Parent perk(s) required. Multiple allowed |
| `can_be_picked` | trigger | Character scope |
| `can_be_auto_selected` | trigger | Additional check for auto-selection (campaign start, becoming landed) |
| `trait` | key | Trait shown in hover tooltip |
| `effect` | effect | Runs on unlock (character scope) |
| `character_modifier` | block | Applied to characters with this perk |
| `name` | dynamic desc | Override name (supports `first_valid`) |
| `auto_selection_weight` | script value | Weight for auto-selection (default: 1000) |

### Conditional Modifiers on Perks

**Doctrine-based**:
```
doctrine_character_modifier = {
	doctrine = doctrine_theocracy_temporal
	clergy_opinion = 10
}
```

**Culture-based**:
```
culture_character_modifier = {
	parameter = automatic_befriend_access
	befriend_scheme_phase_duration_add = medium_scheme_phase_duration_bonus_value
}
```

**Government-based**:
```
government_character_modifier = {
	flag = government_is_landless_adventurer
	invert_check = no          # yes = apply when government does NOT have flag
	enemy_terrain_advantage = -0.5
}
```

Multiple of each type can be defined on a single perk.

### Graphics

Perk icons: `gfx/interface/icons/lifestyles_perks/<KEY>.dds`

In vanilla, perks use a common node icon (e.g. `node_learning`) up to the final perk of a tree, which uses the trait icon given by that perk.
