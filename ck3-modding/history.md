# History Modding — Reference

History modding applies changes to data in `game/history/`. Subfolders: characters, cultures, provinces, titles, wars. Character history is covered in `characters.md`.

History modding is verbose, but simple to understand once you get your head around it — it's about changing the **history** of existing objects, not defining the objects themselves. See also `reference/history/_history.info`, `reference/history/_characters.info`, `reference/history/_provinces.info`.

## Title History

Files in `history/titles/`, organized by de jure kingdom. Each file contains the kingdom and all its de jure duchies and counties.

### Structure

```
c_lyon = {
	867.1.1 = { change_development_level = 8 }
	1066.1.1 = { change_development_level = 10 }

	855.8.23 = {
		liege = "k_burgundy"
		holder = 144998
	}
	863.1.1 = {
		holder = 168238    # Guilhem I de Forez
	}
	863.1.25 = {
		liege = d_dauphine
	}
	871.1.1 = {
		holder = 168239    # Guilhem II de Forez
	}
}
```

### Key Rules

- **Holder**: `holder = CHARACTER_ID` — sets who holds the title at that date
- **Liege**: `liege = "k_burgundy"` — sets the liege (NOT de jure, just actual control). `liege = 0` makes independent
- **Government**: `government = feudal_government` — change government type at date
- **Development**: `change_development_level = 8`
- Changes persist until the next date entry overrides them
- Missing liege = independent holder
- Character IDs from `history/characters/` files

See also `reference/common/governments/_governments.info`.

### Government Types in History

```
866.1.1 = { government = theocracy_government }
867.1.1 = { government = republic_government }
868.1.1 = { government = feudal_government }
869.1.1 = { government = clan_government }
870.1.1 = { government = tribal_government }
871.1.1 = { government = mercenary_government }
872.1.1 = { government = holy_order_government }
```

### Practical Tips

- When adding characters as holders, align their death dates with when a successor takes over. Otherwise the predecessor loses the title before death and won't show as "Count of X" in the dynasty tree — they'll just be "X of Dynasty Y".
- Date format is always `yyyy.mm.dd`

## Culture History

Files in `history/cultures/`, one per culture group. Controls which innovations are discovered at game start for each bookmark date.

```
867.1.1 = {
	discover_innovation = innovation_bannus
	discover_innovation = innovation_catapult
	discover_innovation = innovation_quilted_armor
	discover_innovation = innovation_development_01
}

950.1.1 = {
	discover_innovation = innovation_motte
	discover_innovation = innovation_barracks
	join_era = culture_era_early_medieval
}

1066 = {
	discover_innovation = innovation_horseshoes
	discover_innovation = innovation_hereditary_rule
}
```

### How Date Blocks Work

Innovations are only **preset** for the specific start date. Example:
- Starting in 867: catapults are discovered, but barracks (listed under 950) depend on the cultural head's fascination during gameplay
- Starting in 950: all innovations from 867 AND 950 blocks are discovered at game start

Innovation IDs are in `common/culture/innovations/`. Culture-to-group mapping in `common/culture/cultures/`. See also `reference/common/culture/innovations/_culture_innovations.info`.

## Effects in History

History scripts can call effects, just like dynamic scripts. The `ROOT` scope depends on the history type (e.g. for title history, root is the title).

```
k_england = {
	1066.1.5 = {
		holder = 122    # Harold Godwinson
		effect = {
			set_capital_county = title:c_middlesex
		}
	}
}
```

This allows complex setup logic at specific historical dates.
