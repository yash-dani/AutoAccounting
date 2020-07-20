from os import system, name # built in packages
from time import sleep


# clear screen (for readability when interacting with bot)
def clear():
	# windows
	if name == 'nt':
		_ = system('cls')

	# posix (mac & linux)
	else:
		_ = system('clear')