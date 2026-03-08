##############################################################
# Overview
##############################################################
#
# Scripted illustrations are a system to select graphical assets for use in GUI files or game code, optionally based on
# script-scope information.
# There are currently two types of graphical assets that can be selected this way:
#  - Textures (`texture = `) for any GUI property that can take a texture
#  - 3D lighting environments (`environment = `) for any 3D scenes that can take them (currently portraits)
#
# The system will test the definitions within a Scripted Illustration type, and return the first one (top down) that
# is valid.
#
### Script & GUI examples
#
# Scripted Illustrations can use the GUI data system in combination with the script-scope system.
# Any GUI widget you want to use this system with needs a scope that it can use to select from as a base scope; for
# example for a Character:
#
#	datacontext = "[CharacterWindow.GetCharacter]"
#
# Then within that widget, or child widget of that widget, you can add an Illustration data-context targeting a specific
# Scripted Illustration type:
#
#	datacontext = "[GetIllustration( 'character_view_bg' )]"
#
# This will allow you then to use the 'Illustration' GUI data functions, to grab a specific graphical asset:
#
#	texture = "[Illustration.GetTexture( Character.Self )]"
#
# Note: The `Character` GUI data type was made available by the `datacontext = "[CharacterWindow.GetCharacter]"`
# statement above. You can use other data-contexts as well for base scopes.
#
### Error reporting
#
# If a graphical asset is requested, but none of the items in the type matches, an error is logged.
# Most usages have a 'fallback' item without any trigger to provide a base visual. But during development this can
# be commented out to detect when there are no assets found.
#
### Hard-coded Scripted Illustration types
#
# This system is also used from within the game code to fetch assets for specific purposes.
#
# 'front_end_random_background'
# A random texture will be selected from the available textures. (no script base scope is available, tested or used).
# Use for example in Multiplayer interface background illustrations.
# 'main_menu_background'
# The background illustration to of the main menu screen, based on the scope of the last savegame's Character.
#

##############################################################
# Structure
##############################################################

### Brief: key ( string )
# Defines a scripted illustration type with this name.
my_scripted_illustration_type_name = {
	### Brienf folder (string)
	# Defines the folder that the illustrations will be found in, defaults to gfx/interface/illustraionts
	# The texture can itself be a path relative to this base folder as well
	folder = "path/to/folder"

	### Brief: texture ( scripted value )
	# Define a texture that can be returned for this type. You can define any number of these per Scripted Illustration
	# type.
	# The first "texture" that has a valid 'trigger' will be returned.
	texture = {

		### Brief: reference ( string )
		# Location of the texture, relative to the 'gfx/interface/illustations' path.
		# (or more specifically: the "illustration" path defined in paths.settings)
		reference = "event_scene/alley.dds"

		### Brief: trigger ( trigger )
		# Tests if this a valid texture, using the base scope provided.
		# If you do not define a 'trigger', it is always valid.
		trigger = { ... }
	}

	### Brief: texture ( scripted value )
	# Define a 3D graphical environment that can be returned for this type. You can define any number of these per
	# Scripted Illustration type.
	# The first "environment" that has a valid 'trigger' will be returned.
	environment = {

		### Brief: reference ( string )
		# Name of an existing portrait environment, as defined in 'gfx/portraits/environments/*.txt' files.
		reference = "environment_cw_tavern_spouse"

		### Brief: trigger ( trigger )
		# Tests if this a valid environment, using the base scope provided.
		# If you do not define a 'trigger', it is always valid.
		trigger = { ... }
	}
}
