# AI Modding — Reference

See also `reference/common/ai_war_stances/_ai_war_stances.info`.

Portions of AI are hardcoded (e.g. army behavior is entirely hardcoded). We can influence AI through:

1. **Defines** — values used in code
2. **Chance and triggers** — how likely AI is to choose options, based on situation
3. **AI personality values** — values influenced by traits/modifiers, checked in script
4. **Script** — custom events/story cycles for AI behavior

## Defines

`common/defines/ai/` contains values referenced by game code. Dev comments explain what the numbers affect:
```
BETROTHAL_MIN_AGE = 12 # The AI will not betrothe, nor seek betrothals with characters under this age.
```

Some AI defines also in `common/defines/00_defines.txt`.

## Chance

Many interactions have scripted AI chance. In events, AI picks the option with higher `ai_chance`:

```
ai_chance = {
	base = 10
	modifier = {
		add = 100
		has_trait = chaste
	}
	modifier = {
		factor = 0          # multiplication — 0 means never pick this
		has_trait = deviant
	}
	ai_value_modifier = {
		ai_zeal = 1         # each point of ai_zeal adds 1 to the score
	}
}
```

- `modifier` changes the base if its trigger is true. Can hold multiple conditions.
- `factor` means multiplication (not addition).
- `ai_value_modifier` adds/subtracts based on personality values, multiplied by the number.
- `trigger = { is_ai = no }` disables events/options entirely for AI.
- `limit = { is_ai = yes }` can make effects differ for AI vs players.

Other AI-relevant fields vary by system: `ai_will_do`, `ai_potential`, `ai_score`, etc. **Read the `.info` files** in the relevant game folders for available options.

## AI Personality Values

Traits and modifiers change these values, which are then checked throughout script:

| Value | What it influences |
|-------|-------------------|
| `ai_boldness` | Risk-taking, willingness to act |
| `ai_compassion` | Mercy, care for others |
| `ai_energy` | Activity level, initiative |
| `ai_greed` | Desire for wealth |
| `ai_honor` | Keeping promises, fairness |
| `ai_rationality` | Logical vs emotional decisions |
| `ai_sociability` | Social interactions |
| `ai_vengefulness` | Grudges, retaliation |
| `ai_zeal` | Religious fervor |
| `ai_war_chance` | Likelihood to declare wars |
| `ai_war_cooldown` | Time between wars |
| `ai_amenity_spending` | Court amenity budget |
| `ai_amenity_target_baseline` | Target amenity level |

View in-game: hover over the head icon at top of character window (requires `-debug_mode` launch option).

## Scripting Custom AI Behavior

Complex AI behavior is done through story cycles, events, and on_actions. See also `reference/common/story_cycles/_story_cycles.info`.

**Example: Conqueror AI**

1. Story cycle fires an effect every 1–2 months: `common/story_cycles/story_cycle_conqueror.txt`
2. That fires the scripted effect `ai_conqueror_yearly_effect`: `common/scripted_effects/00_ai_conqueror_effects.txt`
3. That effect (~2000 lines) manages schemes, budgeting, and declaring wars.

This pattern — story cycle as a periodic ticker, calling a large scripted effect — is the standard approach for complex AI behavior.
