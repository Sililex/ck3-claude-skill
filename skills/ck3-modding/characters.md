# Character Modding — Reference

## Changing Appearance Through Scripts

CK3 uses a DNA system for character appearance. Modify via `dna_modifiers` in `gfx/portraits/portrait_modifiers/`:

```
dna_change_example_modifier = {
	usage = game
	priority = 50    # mandatory for accessories. Higher = applied later (overwrites earlier). Default 0.
	dna_change_example_modifier = {
		dna_modifiers = {
			accessory = {
				mode = add
				gene = headgear
				template = western_imperial
				value = 1.0
			}
			color = {
				mode = modify
				gene = hair_color
				x = 0.5
				y = -0.5
			}
		}
		weight = {
			base = 0
			modifier = {
				add = 100
				has_character_flag = dna_change_example_modifier
			}
		}
	}
}
```

Activate with `add_character_flag = { flag = dna_change_example_modifier }`.

Same-priority groups apply in file order.

## Outfit Tags

Control character clothing in events/portraits.

**Do NOT apply armor through outfit tags.** Instead, set `single_combat_duel_armor` character flag in `immediate` and remove it in `after`.

### Using outfit_tags

Directly on portrait:
```
right_portrait = {
	character = scope:undercover_thief
	animation = scheme
	outfit_tags = {
		western_stealth_hood         # head
		sub_saharan_high_nobility    # torso and legs
		mena_war_legwear             # shoes
	}
}
```

Conditional with `triggered_outfit`:
```
right_portrait = {
	character = scope:merchant
	animation = personality_rational
	triggered_outfit = {
		trigger = { }                    # if fails, outfit not overridden
		outfit_tags = { }
		remove_default_outfit = no       # yes = disable unmatched categories entirely
		hide_info = no                   # yes = no CoA, tooltips, clicks
	}
}
```

Find valid tags by searching `game/events/` and `game/gfx/portraits/portrait_modifiers/` for `outfit_tags`.

### Creating outfit_tags

Use the portrait editor (green button in console menu) to preview genes/subgroups.

Clothing templates in `gfx/portraits/portrait_modifiers/`:
```
my_clothing = {
	dna_modifiers = {
		accessory = {
			mode = add
			gene = clothes
			template = my_subgroup_name    # refs to 3D models
			range = { 0 1 }
		}
	}
	outfit_tags = { my_subgroup_name }     # add this line if missing
	weight = {
		base = 200
	}
}
```

If the clothing doesn't have an `outfit_tags` line, just add one. Name the tag after the subgroup for consistency.

All genes are listed in `common/genes/`. See also `reference/common/genes/_genes.info`.

## Adding / Changing Characters

History characters go in `history/characters/` as `.txt` files. See also `reference/history/_characters.info`.

```
999001 = {                           # unique ID (900000+ is safe; strings like "modChar0" also work)
	name = "Henri"
	dna = lyon_twin_dna_entry        # from common/dna_data (see reference/common/dna_data/_dna_data.info) or portrait editor
	female = yes                     # omit for male
	dynasty = 2100001                # dynasty ID (use dynasty_house for houses)
	martial = 14
	diplomacy = 23
	intrigue = 10
	stewardship = 21
	learning = 15
	prowess = 8
	religion = catholic              # faith ID from common/religion
	culture = french                 # culture ID from common/culture
	trait = diligent
	trait = education_learning_4
	trait = just
	trait = twin
	disallow_random_traits = yes     # prevent random trait generation
	father = 999003                  # character ID
	mother = 999004
	sexuality = heterosexual         # asexual/heterosexual/homosexual/bisexual
	health = 5
	fertility = 0.8

	846.7.29 = {
		birth = yes
	}
	920.5.25 = {
		death = yes
	}
}
```

Key notes:
- Character ID is replaced by a dynamic one when a new game starts
- Attributes cap at 100, are additive (traits/modifiers change final value)
- If attributes/traits not assigned, game generates random ones
- Names may change based on culture in-game

### Date Blocks (Advanced)

Date blocks (`yyyy.mm.dd = { }`) support:

- `birth = yes` / `death = yes`
- `add_spouse = CHARACTER_ID` / `remove_spouse = CHARACTER_ID`
- `give_nickname = NICKNAME_ID` (later use replaces old nickname)
- `employer = CHARACTER_ID` — move character to that character's court
- `give_council_position = councillor_marshal` (also: `councillor_spymaster`, `councillor_chancellor`, `councillor_court_chaplain`, `councillor_steward`)
- `trait = TRAIT_ID` — add traits at a specific date
- `effect = { }` — run arbitrary effects:

```
1019.1.1 = {
	effect = {
		add_character_flag = has_scripted_appearance
		random_list = {
			50 = { set_sexuality = heterosexual }
			50 = { set_sexuality = bisexual }
		}
	}
}
```

## Hairstyles and Beards for Scripted Characters

Add entries to:
- `gfx/portraits/portrait_modifiers/99_beards_scripted_characters.txt`
- `gfx/portraits/portrait_modifiers/99_hairstyles_scripted_characters.txt`

See also `reference/gfx/portraits/portrait_animations/_animations.info` for available animations.

Under the desired hairstyle/beard entry:
```
modifier = {
	add = 200
	exists = character:<history_id>
	this = character:<history_id>
}
```

## Referencing Characters from Script

Use `character:<id>` to reference historical characters:
```
character:74025 = {
	if = {
		limit = {
			is_alive = yes
			is_landed = yes
		}
	}
	trigger_event = bookmark.0200
}
```

Non-historical characters (created at runtime) cannot be referenced by ID — use saved scopes or list-builders instead (see `scopes.md`).
