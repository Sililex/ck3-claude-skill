# Dynasties Modding — Reference

Dynasties can have limitless houses. Four folders are involved in creating a new dynasty. See also `reference/common/dynasty_house_mottos/_mottos.info`, `reference/common/coat_of_arms/dynamic_definitions/_dynamic_definitions.info`, and `reference/common/dynasty_legacies/_dynasty_legacies.info`.

## Creating a Dynasty

### 1. Dynasty definition — `common/dynasties/`

```
2100001 = {
	prefix = "dynnp_de"     # optional prefix (e.g. "de", "von")
	name = "dynn_Lyon"      # localization key, not the actual name
	culture = "french"
	motto = "dynn_Lyon_motto"  # optional, needs localization
}
```

### 2. Localization — `localization/english/`

```yaml
l_english:
 dynn_Lyon:0 "Lyon"
 dynn_Lyon_motto:0 "Through valor we endure"
```

### 3. Coat of Arms — `common/coat_of_arms/coat_of_arms/`

```
2100001 = {    # same ID as dynasty
	pattern = "pattern_solid.dds"
	color1 = "blue"
	color2 = "white"
	colored_emblem = {
		texture = "ce_lion_rampant_crown.dds"
		color1 = "white"
		color2 = "yellow"
		instance = { position = { 0.5 0.5 } scale = { 1.0 1.0 } }
	}
}
```

### 4. Founding House (optional) — `common/dynasty_houses/`

If omitted, the game auto-creates a founding house from dynasty details.

```
house_lyon = {
	prefix = "dynnp_de"
	name = "dynn_Lyon"
	dynasty = 2100001
}
```

## Prefixes

Prefixes add cultural particles before the dynasty name (e.g. "de Lyon", "von Habsburg").

Existing prefixes are in `localization/english/dynasty_names_l_english.yml`, starting with `dynnp_`.

**Important**: Include trailing space in the localization string where needed:

```yaml
l_english:
 dynnp_de:0 "de "     # space after "de"
 dynnp_d-:0 "d'"      # no space (apostrophe style)
```

Results: "de Lyon", "d'Oeuvre"

## Mottos

Can be added to dynasties, houses, or both. Just add `motto = "loc_key"` and localize it.

## Referencing Dynasties and Houses in Script

**Dynasties** can be referenced directly: `dynasty:dynn_Hapsburg`

**Houses cannot be directly scoped.** There is no `house:von_Wien` syntax. If you must reference a specific house, the workaround is to find a historical character you know belongs to that house and chain through them:

```
character:12345.house
```

This is brittle — avoid where possible, but it's the best option when you need a specific house scope and do not have access to it otherwise in the scope context.

## Assigning Characters to Dynasties

In history files, use `dynasty = DYNASTY_ID` (for dynasties without houses) or `dynasty_house = HOUSE_ID` (for specific houses). See `characters.md`.
