import subprocess
import argparse
import re
import sys

# Based on the nuolenna tool made for the Vardial 2019 CLI challenge 

sys.stdout.reconfigure(encoding='utf-16') #required on windows machines


sign_map = {} # dictionnary of ascii:unicode pairs

# open the sign_list.txt file which contains the ascii:unicode pair data, load it into our dictionnary
def load_sign_list(ascii_debug=False):
	f = open("sign_list.txt",encoding="utf-8")
	for line in f:
		#we don't just use .split because some ASCII doesn't have a corresponding unicode char
		ascii = re.sub(r"\t.*","",line).lower().strip()
		sign = re.sub(r".*\t","",line) 
		sign = re.sub("[Xx]","",sign)
		sign = re.sub(r"\\.","",sign)
		sign = sign.strip()
		#with the debug -a option, make the "unicode" be the ascii_rep(unicode_rep)
		#so we can see if things are printing correctly
		if len(ascii) > 0:
			if ascii_debug:
				sign_map[ascii] = ascii + "(" + sign + ")"
			else:
				sign_map[ascii] = sign
	f.close()
	


# Main conversion code from ATF transliteration to unicode
#removed options: word_boundaries,reduceNums,
def toUnicode(atfName,label,doc_markers,spaces,ascii_debug=False): 
	atf = open(atfName,encoding="utf-8")
	for line in atf:
		if re.search("^&",line): #& indicates a new document, split here
			if doc_markers:
				print("NEWDOC " + label)
			else:
				print("\n",end='')
			continue

		if re.search("^[$#@]",line): #discard annotation lines
			print("\n",end='')
			continue

		#get rid of the line number (non-whitespace, then a period)
		line = re.sub("^[\S]*\.","",line)

		if re.search("^ \$ \(",line): #some more useless comments on broken lines
			print("\n",end='')
			continue

		#TODO:???
		line = re.sub("\s\+\s.*\d'","",line)

		#There are 2 ATF conventions for characters: ASCII-ATF and Unicode-ATF,
		# our sign list is in Unicode-ATF, so convert characters to it
		line = re.sub("sz","š",line)
		line = re.sub("SZ","Š",line)
		line = re.sub("s,","ṣ",line)
		line = re.sub("S,","Ṣ",line)
		line = re.sub("t,","ṭ",line)
		line = re.sub("T,","Ṭ",line)
		line = re.sub("s'","ś",line)
		line = re.sub("S'","Ś",line)
		line = re.sub(r"\'","ʾ",line)
		line = re.sub("j","ŋ",line)
		line = re.sub("J","Ŋ",line)
		#sign list doesn't use the funny h of Unicode-ATF, convert them back to ASCII-ATF
		line = re.sub("ḫ","h",line)
		line = re.sub("Ḫ","H",line)
		
		#get rid of markers for damaged signs '#', , and uncertain reading '?', so on
		line = re.sub("[#?\[\]]","",line)
		#remove "..."
		line = re.sub("\.\.\.","",line)
		
		
		#replace various characters that only ever come between grams with a gram or word boundary marker
		line = re.sub("[_\{\}\+<>–]","-",line)
		line = re.sub("[⌈⌉˹˺]","",line) #some symbols which I have no clue what they mean, ORACC documentation doesn't say anything
		line = re.sub("( -)|(- )"," ",line) 

		#Convert subscripts to Unicode-ATF, which is what the sign-list uses
		#regex backref doesn't seem to work, so just brute force these substitutions 
		#it'll already have converted some chars to subscript, so they are no longer digits
		line = re.sub(r"(?=[^\W])0(?=[\d₀-₉]*([-~x!|\s\)]))","₀",line)
		line = re.sub(r"(?=[^\W])1(?=[\d₀-₉]*([-~x!|\s\)]))","₁",line)
		line = re.sub(r"(?=[^\W])2(?=[\d₀-₉]*([-~x!|\s\)]))","₂",line)
		line = re.sub(r"(?=[^\W])3(?=[\d₀-₉]*([-~x!|\s\)]))","₃",line)
		line = re.sub(r"(?=[^\W])4(?=[\d₀-₉]*([-~x!|\s\)]))","₄",line)
		line = re.sub(r"(?=[^\W])5(?=[\d₀-₉]*([-~x!|\s\)]))","₅",line)		
		line = re.sub(r"(?=[^\W])6(?=[\d₀-₉]*([-~x!|\s\)]))","₆",line)
		line = re.sub(r"(?=[^\W])7(?=[\d₀-₉]*([-~x!|\s\)]))","₇",line)
		line = re.sub(r"(?=[^\W])8(?=[\d₀-₉]*([-~x!|\s\)]))","₈",line)
		line = re.sub(r"(?=[^\W])9(?=[\d₀-₉]*([-~x!|\s\)]))","₉",line)
		line = re.sub(r"[Xx](?=[-~x!|\s\)]|\s)","ₓ",line)


		# "blabla!" indicates that the word was corrected by the transcriber to "blabla",
		# this can be followed by "(blavla)" to indicate original
		# discard the '!' and incorrect sign
		line = re.sub("!(\(\S+\))?","",line)


		#if we see a repetition style compound word ie. #xtype, represent as typetypetypetype
		#This can still repeat some grams eroneously, see documentation
		repetitions = re.finditer(r"\(?([\d]+)\)?[x×]\(?([^\s\|\)\(]+)\)?",line)
		for repetition in repetitions:
			#find the number of repetitions and the symbol
			number = int(repetition.groups()[0])
			sign = repetition.groups()[1]
			replacement = sign.lower()
			#sub-in the character x times
			for x in range(number-1):
				replacement += "-" + sign.lower()
			#if parenthesis () are part of the characters to be repeated, escape them
			z = re.sub("\(","\\\(",repetition.group())
			z = re.sub("\)","\\\)",z)
			line = re.sub(z,replacement,line)


		# quantities are expressed as #(type), represent this as typetypetypetype....
		# fractional quantities like 1/3 will become 1
		# very similar to the above repetitions, but for measurement quantities
		quantities = re.finditer("(?:\d/)?(\d+)\(([^\s\(]*)\)",line)
		for quantity in quantities:
			number = int(quantity.groups()[0])
			sign = quantity.groups()[1]
			replacement = sign.lower()
			for x in range(number-1):
				replacement += "-" + sign.lower()
			#stop regex from matching () as a capture group
			z = re.sub("\(","\\\(",quantity.group())
			z = re.sub("\)","\\\)",z)

			line = re.sub(z,replacement,line)

		#break up compound words, if there is a single sign we want to put back,
		#we can do that on a case by case basis
		line = re.sub(r"(\S)[x×.+&%@](\S)",r"\1-\2",line)
		line = re.sub(r"[\|;]","",line)
		#print("***" + line)

		for word in line.lower().strip().split():	
			for gram in word.split("-"):

				# '$' == reading is uncertain, this annotation is unneeded
				gram = re.sub("[\$\(\)]","",gram)
			
				#get rid of phoenetic complements
				gram = re.sub("\{\+","-",gram)
				#separate joined characters
				gram = re.sub("\+","-",gram)
				gram = re.sub("[{}]","-",gram)
				
				#Something the original Nuolenna did, not needed since the sign list replaces it
				#the same way anyways
				#word = re.sub("lagaš","šir-bur-la",word)
				
				#TODO: Nuolenna did this, what is it for?
				gram = re.sub("  *"," ",gram)
				
				#Remove modifier notations ("reflected", "slanted", "variant", etc., they don't matter to us)
				gram = re.sub("[@~].*","",gram)
							
				#Proto-Cuneiform quantity characters aren't part of unicode yet, just substitute
				#them with the circle character
				gram = re.sub("^n[0-9₀-₉]+","n01",gram) #TODO: somehow this is overwriting {na4} with nan01
				#	gram = re.sub("1\/2\(iku\)","",gram) #nuolenna gets rid of the 1/2(iku), we don't need to
				#get rid of remaining '(' and ')'
				gram = re.sub("[\(\)]","",gram)
				
				#do the character look up and print the unicode character
				if gram in sign_map.keys():
					print(sign_map[gram],end='')

						
				#TODO: nuolenna does this, dont know what this is for
				# and I don't see the character in the ORACC documentation of ATF
				elif gram == "€":
					print("  ",end='')
				elif ascii_debug and gram != "ₓ" and gram != "" and gram != ",":
					print("[" + gram + "]",end='')
				
			#Add spaces as word boundaries if that setting is present
			if spaces:
				print(" ",end='')
		print("\n",end='')
	atf.close()

# 	
#try this for debugging: python nuolenpy.py Example.atf Ex -a -s -d > Example_test.txt
#this for final: python nuolenpy.py Example.atf Ex -s -d > Example.txt

if __name__ == "__main__":
	#parse command line argument
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
	
	#Some obsolete options
	#parser.add_argument('-b','--wordSEchars',action='store_true',
	#	help="adds \'<\' and \'>\' to the start and end of words, as this can help n-gram models")
	#parser.add_argument('-n','--reduceNums',action='store_true',
	#	help="Reduces all numbers in the text to \'1\'")

	parser.add_argument('-a','--asciiDebug',action='store_true',
		help="instead of printing cuneiform's sign representation, print a combo ascii(sign) representation")
	
	# potential future improvements: add lemmatization as an option
	# something like this: parser.add_argument('-l','--lemmatizer',choices=[None,'a','b'],
		#help="specify a lemmatizer to use on the words")

	#get the user arguments and run the converter	
	args = parser.parse_args()

	load_sign_list(args.asciiDebug)
	toUnicode(args.atfFile,args.label,args.docMarkers,args.spaces,args.asciiDebug) #args.wordSEchars,args.reduceNums, 
