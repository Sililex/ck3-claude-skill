# Regiments (Men-at-Arms) Modding — Reference

Defined in `common/men_at_arms_types/`. See `reference/common/men_at_arms_types/_men_at_arms_types.info`.

Use unique file names for compatibility.

## Structure

```
example_maa = {
	type = skirmishers          # unit type

	damage = 10
	toughness = 10
	pursuit = 10
	screen = 10

	terrain_bonus = {
		forest = { damage = 3 screen = 3 }
	}

	winter_bonus = {
		normal_winter = { damage = -10 toughness = -5 }
		harsh_winter = { damage = -20 toughness = -10 }
	}

	counters = {
		heavy_infantry = 1       # counter multiple types allowed
	}

	buy_cost = { gold = 150 }
	low_maintenance_cost = { gold = 1 }
	high_maintenance_cost = { gold = 5 }

	stack = 100                  # men per unit
	max_sub_regiments = 5
	hired_stack_size = 25        # sub-regiment size for hired troops (default: stack value)

	can_recruit = { }            # optional trigger (character scope). Empty/omitted = always recruitable

	siege_tier = 1               # fort-countering ability
	fights_in_main_phase = no    # no = only affects pursuit phase (handy for siege weapons)

	ai_quality = { value = culture_ai_weight_pikemen }

	icon = skirmishers           # .dds in gfx/interface/icons/regimenttypes/

	mercenary_fallback = yes
	holy_order_fallback = yes
	fallback_in_hired_troops_if_unlocked = yes
	allowed_in_hired_troops = no
}
```

## All Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | Unit type (skirmishers, heavy_infantry, etc.) |
| `can_recruit` | trigger | Character scope. Empty = always recruitable |
| `damage` | int | Damage value |
| `toughness` | int | Toughness value |
| `pursuit` | int | Pursuit value |
| `screen` | int | Screen value |
| `terrain_bonus` | block | Per-terrain stat bonuses |
| `winter_bonus` | block | `normal_winter` and/or `harsh_winter` bonuses |
| `counters` | block | Unit types this counters (can be multiple) |
| `buy_cost` | block | Purchase cost |
| `low_maintenance_cost` | block | Unraised maintenance |
| `high_maintenance_cost` | block | Raised maintenance |
| `stack` | int | Men per unit |
| `max_sub_regiments` | int | Max sub-regiments |
| `hired_stack_size` | int | Sub-regiment size for hired troops (default: `stack`) |
| `siege_tier` | int | Fort-countering effectiveness |
| `fights_in_main_phase` | bool | `no` = only pursuit phase |
| `ai_quality` | script value | AI weight |
| `icon` | string | Icon name (no `.dds`) in `gfx/interface/icons/regimenttypes/` |
| `mercenary_fallback` | bool | Fallback for mercenaries |
| `holy_order_fallback` | bool | Fallback for holy orders |
| `fallback_in_hired_troops_if_unlocked` | bool | Mercs/holy orders won't prefer this if unlocked |
| `allowed_in_hired_troops` | bool | Allowed in hired troops |

## Unlocking via Innovations

See `reference/common/culture/innovations/_culture_innovations.info`.

In an innovation definition:
```
unlock_maa = my_maa
```

Or provide stat bonuses to existing types:
```
maa_upgrade = {
	type = cavalry
	damage = 0.1
	toughness = 0.1
	pursue = 0.1
	screen = 0.1
	siege_value = 0.1
	max_size = 1
}
```

## Unlocking via Cultural Traditions

See `reference/common/culture/traditions/_traditions.info`.

In the tradition definition, add a `can_recruit` parameter block that checks for the tradition:

```
# In common/culture/traditions/my_traditions.txt:
tradition_example = {
	parameters = {
		unlock_maa_example = yes
	}
}
```

Then in the MaA definition:
```
example_maa = {
	can_recruit = {
		culture = {
			has_cultural_parameter = unlock_maa_example
		}
	}
}
```

## Localization

```yaml
l_english:
 example_maa:0 "Example Regiment"
 example_maa_flavor:0 "Flavor text describing the regiment."
```
