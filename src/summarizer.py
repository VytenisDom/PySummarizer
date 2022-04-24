import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import operator
import sys
nlp = spacy.load("en_core_web_sm")

def summarize(text, output, n):
	doc = nlp(text)

	word_scores = {}

	# Add all words
	for word in doc:
		word_scores[word.text.lower()] = 0


	# Score every word, that isn't a stop worda or punctuation and add to the word_scores object 
	for word in doc:
		word = word.text.lower()
		if word in word_scores and word not in STOP_WORDS and word not in punctuation and "\n" not in word:
			word_scores[word] += 1

	# Create a list of tuple (sentence text, score, index)
	sents = []
	sent_length = 0;
	
	sent_score = 0
	# Score sentences based by word scores (use enumerate to get index)
	for index, sent in enumerate(doc.sents):
		sent_length += 1;
		for word in sent:
			sent_score += word_scores[word.text.lower()]
		sents.append((sent.text.replace("\n", " "), sent_score / (len(sent) / 2), index))
		sent_score = 0;

	# Sort the sentences by sentence score (tuple index 1)
	sents.sort(key=operator.itemgetter(1))

	# If n is a percentage, calculate it and cast to int
	if n < 1:
		n = int(round(n * sent_length))
	else:
		n = int(n)
	# Take best rated n amount of sentences
	bestSents = sents[-n:]
	# Sort again to keep the sentence order as in original text
	bestSents.sort(key=operator.itemgetter(2))

	# Compile into text
	summary_text = ""
	for sent in bestSents:
		summary_text += sent[0] + " "

	if output == 0:
		print("Writing to file output.txt")
		f = open("output.txt", "w")
		f.write(summary_text)
		f.close()
		print("Done.")
	elif output == 1:
		print(summary_text)

	print("Length of original text   : ", len(text))
	print("Length of summarized text : ", len(summary_text))
	print("Summarized % of text      : ", round(((len(text) - len(summary_text)) / len(text)) * 100, 2), "%")


# Read from cmd args
if (len(sys.argv) == 5):
	# print(sys.argv[1]) # inputMode
	# print(sys.argv[2]) # outputMode
	# print(sys.argv[3]) # input (file or text)
	# print(sys.argv[4]) # n

	errors_present = False

	# Handling errors on inputMode parameter
	if sys.argv[1] == '0':
		# Input from file
		text = ""
		# Handling errors on input parameter
		try:
			f = open(sys.argv[3], "r")
			print("Reading from file", sys.argv[3])
			text = f.read()
			f.close()
		except IOError:
			print("File does not exist.")
			errors_present = True
	elif sys.argv[1] == '1':
		# Input from arg
		text = sys.argv[3]
	else:
		print("Input parameter formatting is not correct.")
		errors_present = True

	# Handling errors on outputMode parameter
	if sys.argv[2] != "0" and sys.argv[2] != "1":
		print("Output parameter formatting is not correct.")
		errors_present = True
	else:
		output = int(sys.argv[2])

	# Handling errors on n parameter
	try: 
		n = float(sys.argv[4])
		if (n < 0):
			print("N parameter must be a positive integer or a fraction.")
			errors_present = True
	except:
		print("N parameter must be a number")
		errors_present = True
	

	# If no errors are present - start the summarization with given parameters
	if not errors_present:
		summarize(text, output, n)
else:
	print("Please use correct argument formatting.")