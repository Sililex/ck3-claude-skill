# Religions Modding — Reference

Hierarchy: **Religion Family** → **Religion** → **Faith**

Files in `common/religion/`. See `reference/common/religion/religions/_religions.info`.

## Religion Families

Defined in `common/religion/religion_families/`. See `reference/common/religion/religion_families/_religion_families.info`. The three vanilla families: Abrahamic, Eastern, Pagan.

```
rf_abrahamic = {
	graphical_faith = "orthodox_gfx"
	hostility_doctrine = abrahamic_hostility_doctrine
	doctrine_background_icon = core_tenet_banner_christian.dds
	is_pagan = no           # default: yes
}
```

| Attribute | Type | Description |
|-----------|------|-------------|
| `is_pagan` | bool | Default: yes |
| `graphical_faith` | gfx | 3D model (temple assets). Overridden by religion/faith |
| `piety_icon_group` | gfx | Piety icon set. Overridden by religion/faith |
| `doctrine_background_icon` | gfx | Overridden by religion/faith |
| `hostility_doctrine` | doctrine | Interface only: hostility display for family |

## Religions

Defined in `common/religion/religions/`. Each file contains one religion with its faiths.

```
sea_cults = {
	family = rf_pagan
	graphical_faith = pagan_gfx
	pagan_roots = yes          # unreformed/reformed distinction in UI

	# Doctrines applied to ALL faiths (game start only, for convenience)
	# Cannot define multi-pick doctrines at religion level
	# Must be defined BEFORE the faiths section
	doctrine = doctrine_spiritual_head
	doctrine = doctrine_gender_male_dominated
	doctrine = doctrine_pluralism_fundamentalist
	# ... (marriage, crimes, clerical doctrines)

	traits = {
		virtues = { brave lunatic_1 wrathful }
		sins = { patient content shy }
		# Optional scaling: virtues = { brave = 0.5 }
		# Custom modifier: sins = { stubborn = { monthly_prestige = -0.1 scale = 2 } }
	}

	reserved_male_names = { Lobbo Lobbeu Lobst }
	reserved_female_names = { Lobba Lobbelia Lobsta }

	holy_order_names = {
		{ name = "holy_order_claw_bearers" coat_of_arms = "coa_key" }
		{ name = "holy_order_clackers" }
	}
	holy_order_maa = { huscarl }

	custom_faith_icons = { custom_faith_1 lobbist lobbist_reformed }

	localization = {
		HighGodName = sea_cults_high_god
		# ... (see localization keys below)
	}

	faiths = {
		# ... (see Faiths section)
	}
}
```

### Virtues and Sins Notes

- Trait groups work (e.g. `lunatic_1` matches the group)
- Only the first trait in a group is shown in UI
- Virtues/sins affect opinion (viewer's faith matters) and give `virtue_owner_modifier`/`sin_owner_modifier`
- Optional scaling: `brave = 0.5` scales both opinion and modifier
- Custom modifier: `stubborn = { monthly_prestige = -0.1 scale = 2 }`

## Faiths

Defined inside the `faiths = { }` block of a religion:

```
faiths = {
	lobbist = {
		color = { 0.2 0.2 0.9 }
		icon = lobbist
		reformed_icon = lobbist_reformed

		holy_site = uppsala
		holy_site = lejre
		holy_site = paderborn
		holy_site = zeeland
		holy_site = ranaheim

		doctrine = unreformed_faith_doctrine
		doctrine = tenet_warmonger
		doctrine = tenet_human_sacrifice
		doctrine = tenet_ancestor_worship

		religious_head = d_lobbist_papacy    # optional

		localization = { ... }
	}
}
```

| Attribute | Type | Description |
|-----------|------|-------------|
| `color` | RGB | Faith color |
| `icon` | gfx | Faith icon (can use another faith's icon) |
| `reformed_icon` | gfx | Icon for reformed version |
| `graphical_faith` | gfx | 3D model override |
| `piety_icon_group` | gfx | Piety icons override |
| `religious_head` | title | Religious head title (if not set, no head unless created in script) |
| `holy_site` | key | Holy site (add multiple). Defined in `common/religion/holy_sites/` |
| `doctrine` | key | Overrides religion-level doctrines |
| `reserved_male_names` / `reserved_female_names` | list | Override religion-level names |

## Holy Sites

Defined in `common/religion/holy_sites/`. See `reference/common/religion/holy_sites/_holy_sites.info`.

```
jerusalem = {
	county = c_jerusalem
	barony = b_vaticano          # optional, more specific

	character_modifier = {
		monthly_piety_gain_mult = 0.2
	}
	flag = jerusalem_conversion_bonus
}
```

### Holy Site Localization

```yaml
l_english:
 holy_site_jerusalem_name:0 "Jerusalem"
 holy_site_jerusalem_effect_name:0 "From [holy_site|E] #weak ($holy_site_jerusalem_name$)#!"
 holy_site_jerusalem_effects:0 "County Conversion Speed: #P +20%#!"
```

## Localization

### Object Localization (required)

```yaml
l_english:
 sea_cults:0 "Sea Cults"
 sea_cults_adj:0 "Sea Cultist"
 sea_cults_adherent:0 "Sea Cultist"
 sea_cults_adherent_plural:0 "Sea Cultists"
 sea_cults_desc:0 "Description of the religion."
```

Same pattern for faiths: `<faith>`, `<faith>_adj`, `<faith>_adherent`, `<faith>_adherent_plural`, `<faith>_desc`.

### Localization Block Keys

These go in the `localization = { }` block inside the religion/faith. Extensive list of deity/terminology keys:

**Deities**: `HighGodName`, `HighGodNamePossessive`, `HighGodNameSheHe`, `HighGodHerselfHimself`, `HighGodHerHis`, `HighGodNameAlternate`, `CreatorName`, `HealthGodName`, `FertilityGodName`, `WealthGodName`, `HouseholdGodName`, `FateGodName`, `KnowledgeGodName`, `WarGodName`, `TricksterGodName`, `NightGodName`, `WaterGodName`, `DeathDeityName`, `WitchGodName`

Each deity has possessive/pronoun variants: `*Possessive`, `*SheHe`, `*HerHis`, `*HerHim`, `*HerselfHimself`

**Pantheon**: `PantheonTerm`, `PantheonTermHasHave`, `GoodGodNames`, `EvilGodNames`

**Devil**: `DevilName`, `DevilNamePossessive`, `DevilSheHe`, `DevilHerHis`, `DevilHerselfHimself`

**Terminology**: `HouseOfWorship`, `HouseOfWorshipPlural`, `ReligiousSymbol`, `ReligiousText`, `ReligiousHeadName`, `ReligiousHeadTitleName`

**People**: `DevoteeMale/Female/Neuter` (+Plural), `PriestMale/Female/Neuter` (+Plural), `BishopMale/Female/Neuter` (+Plural), `AltPriestTermPlural`

**Afterlife**: `DivineRealm`, `PositiveAfterLife`, `NegativeAfterLife`

**Holy War**: `GHWName`, `GHWNamePlural`

Not all keys are relevant to every religion — irrelevant ones can reference another key (e.g. `FertilityGodName = "$sea_cults_high_god_name$"`).

## Graphics

Faith icons: `gfx/interface/icons/faith/<icon_name>.dds` (100x100 DDS)

No custom graphics required — vanilla has many unused icons available for custom faiths.

## Tenet IDs

Convention: lowercase, spaces → `_`, prefix `tenet_`.

Notable exceptions:
| Name | ID |
|------|----|
| Auspicious Birthright | `tenet_mystical_birthright` |
| Ritual Suicide | `tenet_consolamentum` |
| Ecclesiarchy | `tenet_pentarchy` |
| Religious Law | `tenet_religious_legal_pronouncements` |
| Sacred Lies | `tenet_sacred_shadows` |
| Sanctioned False Conversions | `tenet_false_conversion_sanction` |
| Struggle and Submission | `tenet_struggle_submission` |
