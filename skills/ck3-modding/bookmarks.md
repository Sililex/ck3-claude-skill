# Bookmark Modding — Reference

Bookmarks highlight interesting characters/scenarios on the Select Start Date screen.

## Creating a Bookmark

Files go in `common/bookmarks/`. See also `reference/common/bookmarks/bookmarks/_bookmarks.info`, `reference/common/bookmarks/groups/_bookmark_groups.info`.

Basic structure:
```
bm_my_bookmark = {
	start_date = 3000.5.12       # year.month.day
	is_playable = yes

	character = {
		name = "bookmark_my_char_name"          # must be localized
		dynasty = 7514                          # dynasty ID
		dynasty_splendor_level = 1
		type = male                             # male/female
		birth = 828.1.1                         # defines displayed age
		title = d_york                          # primary title
		government = feudal_government
		culture = norse
		religion = norse_pagan
		difficulty = "BOOKMARK_CHARACTER_DIFFICULTY_EASY"
		history_id = 163112                     # character ID from history
		position = { 765 590 }                  # position on bookmark map image
		animation = disapproval                 # portrait pose

		# Nested characters shown as relations
		character = {
			name = "bookmark_my_char_alt_son"
			relation = "BOOKMARK_RELATION_SON"
			dynasty = 7514
			type = male
			birth = 844.1.1
			culture = norse
			religion = norse_pagan
			history_id = 168336
			animation = personality_greedy
		}
	}
}
```

Character stats/traits come from history files, not the bookmark definition.

## Portraits

Bookmark portraits are auto-generated. Use console command:
```
dump_bookmark_portraits
```

Output goes to: `Documents/Paradox Interactive/Crusader Kings III/common/bookmark_portraits/`

## Bookmark Screen

The selection screen uses a **custom map image** (not auto-generated): `gfx/interface/bookmarks/`.

- Format: `.dds` with mipmaps and BC3 encoding
- Size: `1920 x 1200` (defined in `gui/frontend_bookmarks.gui`)
- The `position` values in the bookmark file correspond to pixel positions on this image
- You also need per-character highlight versions showing only that character's realm

**Testing positions**: use debug mode, edit positions, flip back to the bookmark screen. Crash-prone.

**Making the map image**:
1. Screenshot the game map or use a blank CK3 map template
2. Overlay `provinces.png` from the CK3 directory
3. Use magic wand to select baronies in each character's realm
4. Fill with color at ~50% opacity
5. Add borders/visual effects
6. Save as `.dds` (mipmaps, BC3 encoding)

## Coat of Arms

Pre-defined CoAs display correctly. Procedurally generated ones will be blank.

Fix: add a CoA definition in `common/coat_of_arms/` (see also `reference/common/coat_of_arms/dynamic_definitions/_dynamic_definitions.info`). Easiest method:
1. Customize the CoA in-game
2. Click "copy to clipboard"
3. Paste into your CoA file
4. Remove the `custom` field

## Buttons

- Start button: `gfx/interface/bookmarks/start_buttons/` — copying a vanilla one is acceptable
- Stained glass banner: `gfx/interface/icons/bookmark_buttons/`

## Important Notes

- A bookmark **will not load** if it has any character/title history errors
- All `name` fields must have localization entries
- Keep IDs coherent across files (e.g. `bm_3000_wotr` referenced consistently)
