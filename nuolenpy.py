import subprocess
import argparse
import re

# Nuolenna seems to lose more info than needed:
#- Start and end of word info
# and it seems to interpret [...] as the circle character, where it appears to just mean unknown text

#So this is my attempt to recreate Nuolenna in python, though it might not be necessary
# Since this is a modified version of Nuolenna which uses something like GPL3, this script also needs to have the same license
# I take it?

#pseudo-code

#Load sign_list.txt (pairs of ASCII ATF encoding, and the corresponding unicode character)
#for each line
#	isolate the ASCII and the unicode to their own strings
#	trim whitespace
#	tolower
#	get rid of \. x X 	"change all combination signs to just signs following eac other"
#	if line.len > 0: 
#		add ASCII + sign to the map (dictionnary in python's case?)

sign_map = {}

def load_sign_list():
	f = open("sign_list.txt")
	for line in f:
		#we don't just use .split because some ASCII doesn't have a corresponding unicode char
		ascii = re.sub("\t.*","",line).lower().strip()
		sign = re.sub(".*\t","",line).replace("[Xx]","").replace("\\.","").strip()
		if len(ascii) > 0:
			sign_map[ascii] = sign
	f.close()
	
#Load the file to translate
#for each line
#	to lower case
#	split at spaces
#	for each word
#		is it kind of like this?: 5(disz), that is, a number followed by a word in parenthesis
#		This indicates in ATF that the word is duplicated, so we paste the corresponding character into our output x times

#		remove $ signs, since they just indicate that the reading of a sign is uncertain, not the sign itself
#		replace some other stuff

#		for each syllable in a word (split word by space):
#			remove annotation stuff (@ and ~ things)
#			all numbers are replaced with "1" >>> we likely want to disable this by default, or at least experiment with it
#			check if the syllable is in the sign map: print it
#			else if it has (x or .) but not &:
#				split by x and ., print the resulting subsyllables if they are in the sign map
#			else if the character is euro?: print a couple spaces
#		print new line

def toUnicode(atfName,label,doc_markers,spaces,word_boundaries,removeNums):
	atf = open(atfName)
	for line in atf:
		#perhaps if the first char of a line is '&', leave/skip it, as its a doc boundary
		for word in line.lower().split():
			# replace #repetitions(sign) with signsignsignsign....
			if re.search("^[1-90][1-90]*\\\(.*\\\)$",word):
				sign = re.sub("^[1-90][1-90]*\\\(","",word)
				sign = re.sub("\\\)$","",sign)
				repetitions = 
				word = sign
				
	
	atf.close()
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		prog='nuolenpy',
		description='converts ATF to unicode with optional formatting, prints to stdout',
	)
	
	parser.add_argument('atfFile',
		help='The input ATF file')
	parser.add_argument('label',
		help='The label to apply to the output files, ex. \'Akkadian\' \'Legal\'')
	parser.add_argument('-d','--docMarkers', action='store_true',
		help='ATF can store multiple documents per file, using this option preserves the document boundaries')
	parser.add_argument('-s','--spaces', action='store_true',
		help="keep spaces between words")
	parser.add_argument('-b','--wordSEchars',action='store_true',
		help="adds \'<\' and \'>\' to the start and end of words, as this can help n-gram models")
	parser.add_argument('-n','--removeNums',action='store_true',
		help="Reduces all numbers in the text to \'1\'")
	# potential future improvements: add lemmatization as an option
	# something like this: parser.add_argument('-l','--lemmatizer',choices=[None,'a','b'],
		#help="specify a lemmatizer to use on the words")
		
	args = parser.parse_args()

	load_sign_list()
	toUnicode(args.atfFile,args.label,args.docMarkers,args.spaces,args.wordSEchars,args.removeNums)

#Some changes we want to make
# >> make replacing numbers optional
# >> leave in start/end of document markers (by default)
# >> leave in spaces between words optionally (by default)
# >> add start and end of word characters '<' and '>' optionally
# >> add in genre label to the document
# ** splitting into dev,train,test should be a separate script that interleaves all the atf texts by category


#Terms used in original nuolenna

#nuolenpaa = "arrowhead" unicode mapped to
#transliterratio >> ASCII mapped from

#muutanuoliksi = to arrows
#merki = sign
#sana = word
#maara = amount
#tavu = syllable
#tavut = syllables
#alatavu = subsyllable
#alatavut = subsyllables
