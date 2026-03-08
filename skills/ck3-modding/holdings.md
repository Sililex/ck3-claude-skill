# Holdings Modding — Reference

Defined in `common/holdings/`. See `reference/common/holdings/_holdings.info`, `reference/common/buildings/_buildings.info`.

## Structure

```
my_holding = {
	primary_building = my_01      # building generated at start

	buildings = {                  # available buildings for this holding type
		mychurch_01
		mycastle_01
		myarmoury_01
	}

	flag = myflag                  # optional flag
	can_be_inherited = yes         # optional
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `primary_building` | string | Building key generated at start |
| `buildings` | block | Buildings available for this holding type |
| `flag` | string | Optional flag assigned to holding type |
| `can_be_inherited` | bool | Can the holding be inherited |

## Auto-Generated Modifiers

When a holding type is loaded, modifiers are automatically generated. You can reference them in `common/modifiers/` without declaring them:

- `<holding_type>_build_speed`
- `<holding_type>_build_gold_cost`
- `<holding_type>_build_piety_cost`
- `<holding_type>_build_prestige_cost`
- `<holding_type>_holding_build_speed`
- `<holding_type>_holding_build_gold_cost`
- `<holding_type>_holding_build_piety_cost`
- `<holding_type>_holding_build_prestige_cost`

Example modifier using auto-generated names:
```
my_modifier = {
	icon = my_icon
	my_holding_build_speed = -0.25
}
```

## Game Concept Icon

Add a `.dds` icon in `common/game_concepts/`:

```
my_holding = {
	alias = { my mine mine_holding }
	parent = holding_type
	texture = "gfx/interface/icons/my_holding_icon.dds"
}
```
