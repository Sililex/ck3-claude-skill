This folder is loaded before any other files, it does not read anything itself but lets you run reader actions with their result data being exported to all other files being read.

You can run all the actions locally to an individual file as well.

NOTE: Where possible use specialized versions of this system, this operates on the token stream as we parse a file meaning it knows NOTHING about the logic or potential optimizations of parsing. It will never be worse than if you had manually done the copy pasting, but if a specialized alternative exists such as scripted triggers and effects then ALWAYS prefer using those.

All reader actions are in the form of @:<action_name> <tokens>
Variable loading and registering have backwards compatible syntaxes.

The reader actions you can perform currently are:

@:register_variable <name> = <value>
@<name> = <value>

Creates a variable with the given name and the right hand side value. Right side can itself reference other constants.
eg: @cool_constant = 123

#####

@:load_variable <name>
@<name>

Loads the value for the variable called <name>, can be used as the right hand side of an expression.
To use as the left hand side do @@<name>.

Variable loading can also perform a math expression if in the form of @[<expression>]
You can perform operations by doing +, -, *, /, (), values, and names of variables.
eg: @[constant_1 * constant_2 + constant_3]

#####

@:define <name> = {
	<tokens>
}

Defines a block called <name> which is a stream of tokens which can be inserted when parsing a file.
Supports argument replacement when tokens in the list are surrounded by $$.

eg: @:define cool_block = {
	color = { 1 0 1 }
	is_valid = {
		always = true
	}
	is_shown = {
		has_trait = $trait$
	}
}

#####

@:insert <name>
@:insert <name> = {
	<argument_name> = <value>
}

Insert the block called <name> into the file and parse its tokens.
If the block requires arguments then they must be provided. If an argument is missing or one not named in the define then an error will occur.

eg: @:insert cool_block = {
	trait = lunatic
}

#####

@:assert

Triggers and assert to happen when parsed, useful for coders to debug parsing issues

#####

@:log "Text"

Outputs the given text to the debug log.
