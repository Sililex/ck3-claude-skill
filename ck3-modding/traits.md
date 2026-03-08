# Traits Modding — Reference

Traits are possessed by characters and modify attributes, opinions, personality, and other parameters.

Defined in `common/traits/` as `.txt` files. See `reference/common/traits/_traits.info`.

## Structure

```
my_trait = {
	category = personality

	# Validation
	valid_sex = all
	minimum_age = 16
	potential = { <triggers> }

	# Flags
	genetic = no
	physical = no
	immortal = no
	incapacitating = no
	disables_combat_leadership = no
	can_have_children = yes
	good = no

	# Generation
	birth = 0
	random_creation = 0
	inherit_chance = 0
	both_parent_has_trait_inherit_chance = 0

	# Modifiers (any unknown property is read as a modifier)
	diplomacy = 2
	monthly_prestige = 0.5

	# Opinion
	same_opinion = 10
	opposite_opinion = -10

	# Relations
	opposites = { lazy }
	compatibility = {
		diligent = 10
		lazy = -10
	}

	# Groups
	group = my_trait_group
	level = 1

	# Ruler designer
	ruler_designer_cost = 50
}
```

## Categories

| Category | Description |
|----------|-------------|
| `personality` | Core personality, auto-generated on characters |
| `education` | Education trait, only one at a time, auto-generated |
| `childhood` | Child personality, grows into adult personality trait |
| `commander` | Combat trait, auto-added if required |
| `winter_commander` | Commander trait, only added in areas with winter |
| `lifestyle` | Lifestyle progress trait |
| `court_type` | Trait from a court type |
| `fame` | Fame or infamy trait |
| `health` | Health condition trait |

## Validation

| Property | Description |
|----------|-------------|
| `valid_sex` | `all`/`male`/`female` (default: `all`) |
| `minimum_age` | Min age required to have this trait |
| `maximum_age` | Max age allowed to have this trait |
| `potential` | Triggers required to get this trait. Not re-checked after applied. Not run in ruler designer. Non-potential traits purged on game start |

## Special Flags

| Flag | Description |
|------|-------------|
| `genetic` | Genetic inheritance rules: trait can be inactive. Active parent = 100% inherit, inactive = 50%. Both parents = active, one parent = inactive. Mutually exclusive with `inherit_chance` |
| `good` | Marks as a "good" genetic trait |
| `physical` | Physical aspect of the character's body |
| `immortal` | Stops visual aging, immune to natural death. Can still be killed by script. Fertility matches visual age. Use `set_immortal_age` to change visual age |
| `incapacitating` | Character requires a regent |
| `disables_combat_leadership` | Blocked from being a commander |
| `can_have_children` | Default: yes |
| `inheritance_blocker` | `none`/`dynasty`/`all` — blocks inheritance |
| `claim_inheritance_blocker` | `none`/`dynasty`/`all` — blocks claim inheritance |
| `enables_inbred` | Children can be considered for inbred trait (only if parents share common ancestors) |
| `bastard` | `none`/`illegitimate`/`legitimate` |
| `shown_in_encyclopedia` | Default: yes |
| `shown_in_ruler_designer` | Default: yes |
| `add_commander_trait` | Auto-generated characters add commander traits |

## Generation

| Property | Description |
|----------|-------------|
| `birth` | 0–100, % of characters born with this trait (if not inherited). Supports decimals |
| `random_creation` | 0–100, % chance on character creation (generated/script characters, not birth). Only for inheritable/genetic traits |
| `random_creation_weight` | Positive value (default: 1). Weight-based random selection for personality/education/childhood categories. Higher = more common |
| `inherit_chance` | 0–100, % chance to inherit. Cannot be set on genetic traits |
| `both_parent_has_trait_inherit_chance` | 0–100, inherit chance when both parents have the trait |
| `parent_inheritance_sex` | `male`/`female`/`all` (default: `all`) — which parent can pass it on |
| `child_inheritance_sex` | `male`/`female`/`all` (default: `all`) — which children can inherit it |
| `inherit_from_real_father` | Inherit from biological father (default: yes). Only matters for genetic/inheritable traits |
| `inherit_from_real_mother` | Inherit from biological mother (default: yes) |

## Groups

Traits can be grouped for inheritance and equivalence:

```
lunatic_1 = {
	group = lunatic
	level = 1
}
lunatic_genetic = {
	group_equivalence = lunatic
}
```

- `group` — groups for both inheritance and equivalence
- `group_equivalence` — groups only for equivalence (e.g. `has_trait = lunatic` checks all)
- `group_inheritance` — groups only for inheritance
- `level` — what level in the group (for tiered traits like `beauty_good_1`/`2`/`3`)

## Opinions

```
same_opinion = 10                  # Opinion if both characters share the trait
same_opinion_if_same_faith = 10    # Opinion if shared trait + same faith
opposite_opinion = -10             # Opinion if characters have opposite traits
```

### Triggered Opinion

```
triggered_opinion = {
	opinion_modifier = opinion_modifier_key
	# All below optional:
	parameter = doctrine_parameter_key   # Boolean doctrine parameter to check
	check_missing = yes                  # Check parameter is NOT set
	same_faith = yes
	same_dynasty = yes
	ignore_opinion_value_if_same_trait = yes
	male_only = yes
	female_only = yes                    # Mutually exclusive with male_only
}
```

## Compatibility

Not an opinion modifier — used by `compatibility_modifier` and `trait_compatibility` trigger:

```
compatibility = {
	gluttonous = 20
	drunkard = @pos_compat_low
}
```

## Portrait Impacts

| Property | Description |
|----------|-------------|
| `genetic_constraint_all` | Genetic constraint applied when gaining trait |
| `genetic_constraint_men` | Constraint for men only |
| `genetic_constraint_women` | Constraint for women only |
| `portrait_extremity_shift` | Shift morph genes toward extremes (0 or 1) by this % |
| `ugliness_portrait_extremity_shift` | Shift the most extreme morph gene feature |
| `forced_portrait_age_index` | Force specific portrait age index (can specify multiple) |

## Conditional Modifiers

```
# Applied if character's culture has the parameter
culture_modifier = {
	parameter = can_blind_prisoners
	diplomacy = 5
}

# Applied if character's faith has a doctrine with the parameter
faith_modifier = {
	parameter = great_holy_wars_active
	stewardship = 1
}
```

Any other unknown property is read as a modifier applied to anyone holding the trait. See `reference/common/modifiers/_modifiers.info`.

## Level Tracks

Traits can gain XP and provide different bonuses at thresholds:

```
my_trait = {
	# Single track (shorthand, named after the trait):
	track = {
		20 = { diplomacy = 1 }
		50 = { diplomacy = 2 }
		90 = { diplomacy = 3 }
	}

	# Or multiple named tracks:
	tracks = {
		combat_skill = {
			20 = { prowess = 1 }
			50 = { prowess = 2 }
		}
		leadership = {
			30 = { monthly_prestige = 0.1 }
		}
	}

	# Optional degradation
	monthly_track_xp_degradation = { min = 20 change = 5 }
}
```

- Use `add_trait_xp` effect and `has_trait_xp` trigger
- Localize with `trait_track_<key>` and `trait_track_<key>_desc`
- XP thresholds must be in ascending order (0–100)

## Commander Terrain

```
trait_exclusive_if_realm_contains = { desert oasis }
```

Commander traits with this are only assigned if the commander's culture has a province with one of these terrain types.

## Misc

| Property | Description |
|----------|-------------|
| `ruler_designer_cost` | Cost in ruler designer (default: 0) |
| `flag` | Flag marker, can add multiple. Localized as `TRAIT_FLAG_DESC_<name>` |
| `culture_succession_prio` | If culture has this flag, children with this trait are considered oldest/youngest for succession ordering |

## Localization

```yaml
l_english:
 trait_my_trait:0 "My Trait"
 trait_my_trait_desc:0 "Description of the trait."
```

### Dynamic Names/Descriptions/Icons

Override with `first_valid` + `triggered_desc`:

```
name = {
	first_valid = {
		triggered_desc = {
			trigger = { NOT = { exists = this } }   # REQUIRED fallback
			desc = trait_my_trait_fallback
		}
		triggered_desc = {
			trigger = { has_trait = brave }
			desc = trait_my_trait_brave_variant
		}
		desc = trait_my_trait                         # default
	}
}
```

Works for `name`, `desc`, and `icon`. The `NOT = { exists = this }` fallback is **required** because there isn't always a root scope (e.g. encyclopedia, tooltips).

For icons, `desc` points to the DDS path:
```
icon = {
	first_valid = {
		triggered_desc = {
			trigger = { NOT = { exists = this } }
			desc = "gfx/interface/icons/traits/diligent.dds"
		}
		triggered_desc = {
			trigger = { gold > 1000 }
			desc = "gfx/interface/icons/traits/diligent.dds"
		}
		desc = "gfx/interface/icons/traits/deceitful.dds"
	}
}
```

## Icon Files

Default path: `gfx/interface/icons/traits/<trait>.dds`

## Trait Index (Obsolete)

Traits no longer use numerical indexes. They appear in ruler designer by order of appearance in code.
