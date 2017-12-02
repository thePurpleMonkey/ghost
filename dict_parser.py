import string, sys

# Eliminate one letter "words" that appear in dictionary
encountered_words = {"b", "c", "d", "e", "f", "g", "h", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}

translator=str.maketrans('','',string.digits)
print("string.ascii_lowercase =", string.ascii_lowercase)

with open("Oxford English Dictionary.txt", "r") as f:
	with open(sys.argv[1] if len(sys.argv) > 1 else "result.txt", "w") as output:
		for line in f:
			try:
				# Empty line
				if len(line.strip()) < 2:
					continue

				# Remove abbreviations, symbols, and old english words
				if "abbr." in line or \
				   "Abbr." in line or \
				   "[abbreviation" in line or \
				   "symb." in line or \
				   "[old english" in line:
					continue

				word = line.split()[0].lower()
				
				# Discard any words containing non-alphabetic characters
				for letter in word:
					if letter not in string.ascii_lowercase:
						# Pretend we've seen this word before. It will get thrown out in later processing. 
						encountered_words.add(word)
						break

				# Remove numbers
				word=word.translate(translator)

				# Remove duplicates
				if word in encountered_words:
					continue
				else:
					encountered_words.add(word)
			
				# Output word in dictionary
				output.write(word + "\n")

			except Exception as e:
				print("Error processing line {}".format(repr(line)))
				print("Error message was:", e)