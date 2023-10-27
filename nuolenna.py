import subprocess

# Nuolenna seems to lose more info than needed:
#- Start and end of word info
# and it seems to interpret [...] as the circle character, where it appears to just mean unknown text
#So this is my attempt to recreate Nuolenna in python, though it might not be necessary

#pseudo-code

#Load sign_list.txt (pairs of ASCII ATF encoding, and the corresponding unicode character)
#	for each line
#		isolate the ASCII and the unicode to their own strings
#		trim whitespace
#		tolower
#		get rid of \. x X 	"change all combination signs to just signs following eacother
#		if line.len > 0: ASCII + sign to the map (dictionnary in python's case?)

#Load the file to translate
#for each line
#	
