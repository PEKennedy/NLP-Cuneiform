import subprocess
import argparse
import re
import sys

# **** This is "good enough", but still has edge cases that don't work
# Known issues:
# incomplete sign list (no proto cuneiform among other missing word)
# _kun4!(|ID+LU|)_ misses ID and LU
# |šu₂.3xan| will make the 3 into a subscript
# some repetitions will be off due to preceding characters ex "ZUTA651xKA" might give 51 ka characters


# This is my attempt to recreate Nuolenna in python, though it might not be necessary
# Since this is a modified version of Nuolenna which uses something like GPL3, this script also needs to have the same license
# I take it?

sys.stdout.reconfigure(encoding='utf-16') #required on windows machines

sign_map = {}

def load_sign_list(ascii_debug=False):
	f = open("sign_list.txt",encoding="utf-8")
	for line in f:
		#we don't just use .split because some ASCII doesn't have a corresponding unicode char
		ascii = re.sub(r"\t.*","",line).lower().strip()
		sign = re.sub(r".*\t","",line) 
		sign = re.sub("[Xx]","",sign)
		sign = re.sub(r"\\.","",sign)
		sign = sign.strip()
		if len(ascii) > 0:
			if ascii_debug:
				sign_map[ascii] = ascii + "(" + sign + ")"
			else:
				sign_map[ascii] = sign
	f.close()
	

#TODO: These are the things medical_25 picks up
#[biṭ₂], line 38
#[enuru], lines 338, 347, 368, 396
#[sila₂], line 501
#[shar], line 952
#[kamad], line 954, 1005
#[šeriš], line 961

def toUnicode(atfName,label,doc_markers,spaces,reduceNums,ascii_debug=False): #word_boundaries,
	atf = open(atfName,encoding="utf-8")
	for line in atf:
		if re.search("^&",line): #& indicates a new document
			if doc_markers:
				print("NEWDOC " + label)
			else:
				print("\n",end='')
			continue

		#get rid of the line number (non-whitespace, then a period)
		

		if re.search("^[$#@]",line): #discard annotation lines
			print("\n",end='')
			continue

		line = re.sub("^[\S]*\.","",line)

		if re.search("^ \$ \(",line): #some more useless comments on broken lines
			print("\n",end='')
			continue

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
		#sign list doesn't use the funny h, convert them back
		line = re.sub("ḫ","h",line)
		line = re.sub("Ḫ","H",line)
		
		#get rid of markers for logograms '_', damaged signs '#', , and uncertain reading '?'
		#line = re.sub("[#_?]","",line)
		line = re.sub("[#?\[\]]","",line)
		line = re.sub("\.\.\.","",line)
		
		#phonetic complement
		#line = re.sub("\}(?!\w)","-",line)
		#line = re.sub("\}(?! )","",line)
		#line = re.sub("(?!\w)\{","-",line)
		#line = re.sub("(?! )\{","",line)

		#get rid of some sort of annotation after the line
		
		#replace things with a gram or word marker
		line = re.sub("[_\{\}\+<>–]","-",line)
		line = re.sub("[⌈⌉˹˺]","",line) #some symbols which I have no clue what they mean, ORACC doesn't say anything
		line = re.sub("( -)|(- )"," ",line) 
		
		#print("## " + line)

		#line = re.sub("(?![\-\s])x(?![\-\s])"," ",line) #get rid of 'x's which indicate unknowns
		
		

		#Remove modifier notations ("reflected", "slanted", "variant", etc., they don't matter to us)
		#line = re.sub("[@~].*(?:[ -])","",line)

		#print("### " + line)

		#Convert subscripts to Unicode-ATF
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


		"""line = re.sub(r"0(?=[\d₀-₉]*([-~!|\s\)]))","₀",line)
		line = re.sub(r"1(?=[\d₀-₉]*([-~!|\s\)]))","₁",line)
		line = re.sub(r"2(?=[\d₀-₉]*([-~!|\s\)]))","₂",line)
		line = re.sub(r"3(?=[\d₀-₉]*([-~!|\s\)]))","₃",line)
		line = re.sub(r"4(?=[\d₀-₉]*([-~!|\s\)]))","₄",line)
		line = re.sub(r"5(?=[\d₀-₉]*([-~!|\s\)]))","₅",line)		
		line = re.sub(r"6(?=[\d₀-₉]*([-~!|\s\)]))","₆",line)
		line = re.sub(r"7(?=[\d₀-₉]*([-~!|\s\)]))","₇",line)
		line = re.sub(r"8(?=[\d₀-₉]*([-~!|\s\)]))","₈",line)
		line = re.sub(r"9(?=[\d₀-₉]*([-~!|\s\)]))","₉",line)
		line = re.sub(r"[Xx](?=[-!|]|\s)","ₓ",line)"""

		# "blabla!" indicates that the word was corrected by the transcriber to "blabla", this can be followed by "(blavla)" to indicate original
		# discard the '!' and incorrect sign
		#print("^^ "+line)
		#line = re.sub("!(\([|\w]+\))?","",line)
		
		line = re.sub("!(\(\S+\))?","",line)
		#print("** "+line)
		#TODO: Handle compound graphemes (mostly by removing the information)
		#compound_repeats = re.findall(r"\|(\d+)[x×](\S)\|")
		#for repeat in compound_repeats:
		
		#TODO: make sure we still have nice gram boundaries (space btw words, - btw grams)
		#TODO: probably still want to replace compounds when its a contains, otherwise,
		#just use the sign lookup
		#\|\(?([^\s\|\dx×.+&%@\(\)]+)\)?[x×.+&%@]\(?([^\s\|\)\(]+)\)?\|
		#\|\(?([^\s\|\d]+)\)?[x×.+&%@]\(?([^\s\|]+)\)?\|
		#line = re.sub(r"\|\(?([^\s\|\dx×.+&%@\(\)]+)\)?[x×.+&%@]\(?([^\s\|\)\(]+)\)?\|",r"-\1-\2-",line)
		#TODO: need to handle multiplication x, and such before the subscript case
		
		#captures digits in \1, gram in \2
		#\|\(?([\d]+)\)?[x×]\(?([^\s\|\)\(]+)\)?\|
		
		#for pair in repeats:
		#	num = int(pair[0])
		#	temp = ""
		#	for x in range(num):
		#		temp += pair[1]+"-"
			
		#print("*" + line)

		#if we see a repetition style compound word ie. #xtype, represent as typetypetypetype
		repetitions = re.finditer(r"\(?([\d]+)\)?[x×]\(?([^\s\|\)\(]+)\)?",line)
		#print(repetitions)
		for repetition in repetitions:
			#word = ""
			#print(repetition)
			#print(repetition.groups())
			number = int(repetition.groups()[0])
			sign = repetition.groups()[1]
			replacement = sign.lower()
			for x in range(number-1):
				replacement += "-" + sign.lower()
			z = re.sub("\(","\\\(",repetition.group())
			z = re.sub("\)","\\\)",z)
			#print("*** ",replacement)
			#TODO: use exact match of group for the sub
			line = re.sub(z,replacement,line)


		# quantities are expressed as #(type), represent this as typetypetypetype....
		# fractional quantities like 1/3 will become 1
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
		#print("**" + line)

		#break up compound words, if there is a single sign we want to put back,
		#we can do that on a case by case basis
		line = re.sub(r"(\S)[x×.+&%@](\S)",r"\1-\2",line)
		line = re.sub(r"[\|;]","",line)
		#print("***" + line)

		for word in line.lower().strip().split():	
			#Convert x subscripts to Unicode-ATF
			#word = re.sub("[Xx](?=-|$)","ₓ",word)

			for gram in word.split("-"):


			
				#TODO Nov 6 |šu₂.3xan| seems main one that doesn't work


				# '$' == reading is uncertain, this annotation is unneeded
				gram = re.sub("[\$\(\)]","",gram)
			

				# replace combination characters with their own sign
				#TODO: Are these right or did Nuolenna forget something like the OR operator?
				#***no, but they're in the sign list, and so probably aren't needed
				#word = re.sub("gad\&gad\.gar\&gar","kinda",word)
				#word = re.sub("bu\&bu\.ab","sirsir",word)
				#word = re.sub("tur\&tur\.za\&za","zizna",word)
				#escape the . in \.gar
				#word = re.sub("še\&še\.tab\&tab\.gar\&gar","garadin₃",word)
		
				# subscript handling TODO: Do these regex capture group references work?
				#word = re.sub("(.*[\.-])([^\.-]*ₓ\()([^\)]*)(\))(.*)",r"\1\3\5",word)
				#word = re.sub("(.*ₓ\()([^\)]*)(\))(.*)",r"\2\4",word)
				
				# remove some precise reading anotations... TODO: check this works, or is even needed after my additions earlier
				#word = re.sub("(.*[^\|\&])(\(\|[^\|]*\|\))(.*)",r"\1\3",word)
				#word = re.sub("(.*\|[^\|]*\|)(\(.*\))(.*)",r"\1\3",word)
				#word = re.sub("(.*[\.-][^\.-]*[^\|\&])(\(.*\))(.*)",r"\1\3",word)
				#word = re.sub("(.*[^\|\&])(\([^\(\)]*\))(.*)",r"\1\3",word)	
		
				#more nasty regexes, make sure '-' remains the syllable separator
				# not space, as we want space to be a word boundary
				
				#word = re.sub("\|","",word)
				#TODO: check this works
				#Replace separator in . separated words (which are in () )
				#if not re.search(".*\(.*\..*\).*",word):
				#	word = re.sub("\.","-",word)
			
				#TODO: This stuff might only work on word level
				#get rid of phoenetic complements
				gram = re.sub("\{\+","-",gram)
				#separate joined characters
				gram = re.sub("\+","-",gram)
				gram = re.sub("[{}]","-",gram)
				
				#word = re.sub("lagaš","šir-bur-la",word)
				
				#TODO: what is this for?
				gram = re.sub("  *"," ",gram)
				
				#for gram in word.split("-"):
				#Remove modifier notations ("reflected", "slanted", "variant", etc., they don't matter to us)
				gram = re.sub("[@~].*","",gram)
							
				#number replacement
				#if reduceNums:
				gram = re.sub("^n[0-9₀-₉]+","n01",gram) #TODO: somehow this is overwriting {na4} with nan01
				#	gram = re.sub("1\/2\(iku\)","",gram)
				#get rid of '(' and ')'
				gram = re.sub("[\(\)]","",gram)
				
				#line 8410
				#strip_pipes = re.sub("\|","",gram)
						
				if gram in sign_map.keys():
					print(sign_map[gram],end='')
				#elif gram[0] == "n":
					"""gram = re.sub(r"0(?=[\d₀-₉]*([-!|\s\)]))","₀",gram)
					gram = re.sub(r"1(?=[\d₀-₉]*([-!|\s\)]))","₁",gram)
					gram = re.sub(r"2(?=[\d₀-₉]*([-!|\s\)]))","₂",gram)
					gram = re.sub(r"3(?=[\d₀-₉]*([-!|\s\)]))","₃",gram)
					gram = re.sub(r"4(?=[\d₀-₉]*([-!|\s\)]))","₄",gram)
					gram = re.sub(r"5(?=[\d₀-₉]*([-!|\s\)]))","₅",gram)		
					gram = re.sub(r"6(?=[\d₀-₉]*([-!|\s\)]))","₆",gram)
					gram = re.sub(r"7(?=[\d₀-₉]*([-!|\s\)]))","₇",gram)
					gram = re.sub(r"8(?=[\d₀-₉]*([-!|\s\)]))","₈",gram)
					gram = re.sub(r"9(?=[\d₀-₉]*([-!|\s\)]))","₉",gram)"""
				#elif strip_pipes in sign_map.keys():
				#	print(sign_map[strip_pipes],end='')
				#elif (("x" in gram or "." in gram) and "&" not in gram):
				#	gram = re.sub("[\.]","x",gram)
			#		subgrams = gram.split("x")
				#	for subgram in subgrams:
				#		if subgram in sign_map.keys():
				#			print(sign_map[subgram],end='')
						
				#TODO: dont know what this is for, and I don't see the character in the ORACC documentation
				elif gram == "€":
					print("  ",end='')
				elif ascii_debug and gram != "ₓ" and gram != "" and gram != ",":
					print("[" + gram + "]",end='')
				
			#Add spaces as word boundaries if that setting is present
			if spaces:
				print(" ",end='')
		print("\n",end='')
	atf.close()
	
#try this for debugging: python nuolenpy.py Medical_10.atf med -a -s -d -n > uni_test.txt
#this for final: python nuolenpy.py Medical_10.atf med -s -d > uni_test.txt
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
	#parser.add_argument('-b','--wordSEchars',action='store_true',
	#	help="adds \'<\' and \'>\' to the start and end of words, as this can help n-gram models")
	parser.add_argument('-n','--reduceNums',action='store_true',
		help="Reduces all numbers in the text to \'1\'")
	parser.add_argument('-a','--asciiDebug',action='store_true',
		help="instead of printing cuneiform's sign representation, print a combo ascii(sign) representation")
	# potential future improvements: add lemmatization as an option
	# something like this: parser.add_argument('-l','--lemmatizer',choices=[None,'a','b'],
		#help="specify a lemmatizer to use on the words")
		
	args = parser.parse_args()

	load_sign_list(args.asciiDebug)
	toUnicode(args.atfFile,args.label,args.docMarkers,args.spaces,args.reduceNums, args.asciiDebug) #args.wordSEchars,

#Some changes we want to make
# >> make replacing numbers optional
# >> leave in start/end of document markers (by default)
# >> leave in spaces between words optionally (by default)
# >> add start and end of word characters '<' and '>' optionally >>> nope, just do that in the model, spaces is fine
# >> add in genre label to the document
# ** splitting into dev,train,test should be a separate script that interleaves all the atf texts by category