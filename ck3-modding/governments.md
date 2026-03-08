# Governments Modding — Reference

Defined in `common/governments/`. See `reference/common/governments/_governments.info`.

**Warning**: Government modding involves opaque rulesets around compatible rules, laws, rights, and registration. Expect pain if you go down this route.

## Structure

```
feudal_government = {
	create_cadet_branches = yes
	rulers_should_have_dynasty = yes
	dynasty_named_realms = yes
	council = yes                        # council available; default: yes
	regiments_prestige_as_gold = no      # use prestige for MaA purchase/reinforce (maintenance still gold); default: no
	fallback = 1

	# Primary holding type for this government
	primary_holding = castle_holding

	# Additional holdings usable without penalty
	valid_holdings = { city_holding }

	# Holdings required in counties
	required_county_holdings = { castle_holding city_holding church_holding }

	# Vassal contract types available
	vassal_contract = {
		feudal_government_taxes
		feudal_government_levies
		special_contract
		religious_rights
		fortification_rights
		coinage_rights
		succession_rights
		war_declaration_rights
		council_rights
		title_revocation_rights
	}

	# Disable AI features (all enabled by default)
	# Some may be disabled by other factors (independence, tier, etc.)
	ai = {
		use_lifestyle = yes
		imprison = yes        # imprison & release
	}
}
```

## Key Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `create_cadet_branches` | bool | Can create cadet dynasty branches |
| `rulers_should_have_dynasty` | bool | Rulers expected to have dynasties |
| `dynasty_named_realms` | bool | Realms named after dynasty |
| `council` | bool | Council available (default: yes) |
| `regiments_prestige_as_gold` | bool | Prestige for MaA buy/reinforce (default: no) |
| `fallback` | int | Fallback priority |
| `primary_holding` | key | Primary holding type |
| `valid_holdings` | list | Additional valid holding types |
| `required_county_holdings` | list | Required holdings in counties |
| `vassal_contract` | list | Available vassal contract types |
| `always_use_patronym` | bool | Force patronym display for this government |
| `ai` | block | Toggle AI features |
