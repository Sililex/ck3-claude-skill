# Culture Modding — Reference

Files go in `common/culture/`. See also `reference/common/culture/cultures/_cultures.info`, `reference/common/culture/traditions/_traditions.info`, `reference/common/culture/pillars/_pillars.info`, `reference/common/culture/innovations/_culture_innovations.info`, `reference/common/culture/name_lists/_name_lists.info`, `reference/common/culture/eras/_culture_eras.info`.

## Culture Groups

Each culture belongs to a culture group, defined in `common/culture/`:

```
name_of_culture_group = {
	graphical_cultures = {
		steppe_coa_gfx
		steppe_building_gfx
		steppe_clothing_gfx
		steppe_unit_gfx
	}
	mercenary_names = {
		{ name = "mercenary_company_ghilman" coat_of_arms = "mc_ghilman" }
	}

	first_culture = { ... }
	second_culture = { ... }
}
```

- `graphical_cultures` — list of graphical culture IDs for CoA, buildings, clothing, units. Multiple per type allowed.
- `mercenary_names` — names and optional CoA for mercenary companies of this group.

### Culture Group ID Convention

From in-game name: lowercase → replace spaces/hyphens with `_` → append `_group`.

## Cultures

Defined inside their culture group block:

```
my_culture = {
	color = { 1 0.5 0.2 }             # decimal RGB, used on map
	heritage = heritage_north_germanic # heritage group

	character_modifier = {             # modifier on all characters of this culture
		diplomacy = 1
	}

	# --- Names ---
	male_names = {
		10 = {                         # weight (higher = more common)
			CommonName OtherName Jan_John    # Name_Base means variant of base name
		}
		1 = {
			RareName
		}
	}

	female_names = {                   # can also be a flat list without weights
		NameA_BaseB NameB NameC_BaseB
	}

	dynasty_names = {
		{ dynnp_von dynn_Pommern }     # prefix + name (braces required for prefix)
		{ dynn_Orsini }                 # no prefix
		dynn_Fournier                   # no braces needed without prefix
	}
	dynasty_of_location_prefix = "dynnp_von"   # cultural "of" (e.g. "de", "von")
	bastard_dynasty_prefix = "snow"             # optional

	cadet_dynasty_names = {
		"dynasty_loc_1"
		"dynasty_loc_2"
	}

	# --- Naming Chances (must not exceed 100 per gender) ---
	pat_grf_name_chance = 50   # male named after paternal grandfather
	mat_grf_name_chance = 5    # male named after maternal grandfather
	father_name_chance = 10    # male named after father

	pat_grm_name_chance = 10   # female named after paternal grandmother
	mat_grm_name_chance = 50   # female named after maternal grandmother
	mother_name_chance = 5     # female named after mother

	# --- Patronyms ---
	patronym_prefix_male = "dynnpat_pre_mac"
	patronym_prefix_male_vowel = "dynnpat_pre_vow_mag"    # when parent name starts with vowel
	patronym_suffix_male = "dynnpat_suf_son"
	patronym_prefix_female = "dynnpat_pre_nic"
	patronym_prefix_female_vowel = "dynnpat_pre_vow_nig"
	patronym_suffix_female = "dynnpat_suf_sdaughter"

	# Prefix and suffix can be used together ("McDavidson")
	# Patronyms display if:
	#   - culture has always_use_patronym = yes, OR
	#   - character's government has it, OR
	#   - character's liege's government has it
	always_use_patronym = yes   # default: no

	# --- Ethnicities ---
	ethnicities = {
		10 = german       # weight determines how common within culture
		10 = caucasian
	}

	# --- Optional Flags ---
	dynasty_title_names = yes      # default no — use dynasty name rather than title name
	founder_named_dynasties = yes  # default no
	dynasty_name_first = yes       # default no — surname before given name (East Asian style)

	# --- Graphical (overrides group) ---
	# graphical_cultures = { english_coa_gfx }

	# --- Mercenaries (overrides group) ---
	# mercenary_names = { ... }
}
```

### Culture ID Convention

From in-game name: lowercase → remove diacritics (á→a, ü→u).

Some notable exceptions:
| In-game | ID |
|---------|----|
| Scots | `scottish` |
| Oghuz | `turkish` |
| Mashriqi | `levantine` |
| Syriac | `assyrian` |
| Kannauji | `hindustani` |
| Permian | `komi` |

### Name Variants

Names can have base name variants using `_` separator:
- `Jan_John` means "Jan" is a variant of the base name "John"
- This links names across cultures (e.g. `John`, `Jan_John`, `Ian_John`, `Jean_John` are all variants)
- The game uses base names for naming-after-ancestors logic
