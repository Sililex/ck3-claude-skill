Supported unit state names:

idle			- The default idle animation
gather			- The unit is gathering
spawn			- The unit was just raised (can still be gathering) or hired (should not be looped, the code will make it swtich to the gather/idle animation)
besiege			- The unit is besieging a holding
combat_won		- The unit is celebrating after winning in combat (should not be looped)
siege_won		- The unit is celebrating after successful siege (should not be looped)
move_retreat	- The unit is retreating
move_attack		- The unit is moving into a province with an enemy unit
move_start		- The unit got a movement order and is walking towards the edge of the province (can be looped or just switch to move_continue after being done)
move_continue	- The unit is on the move, after it left the original province
move			- If there's no move_start or move_continue, this is used as a fallback

Supported combat state names:
attacker_winning	- The attacking army is winning
defender_winning	- The defending army is winning
even				- The armies are (roughly) even
pursuit_attacker_winning	- The attacker is winning in the pursuit phase
pursuit_defender_winning	- The defender is winning in the pursuit phase
