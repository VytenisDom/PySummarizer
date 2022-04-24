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

	# Check if n is percentage
	if n < 1:
		n = int(round(n * sent_length))

	# Take best rated n amount of sentences
	bestSents = sents[-n:]
	# Sort again to keep the sentence order as in original text
	bestSents.sort(key=operator.itemgetter(2))

	# compile them into text
	summary_text = ""
	for sent in bestSents:
		summary_text += sent[0] + " "

	if output == 0:
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
	print(sys.argv[1]) # input
	print(sys.argv[2]) # output
	print(sys.argv[3]) # input (file or text)
	print(sys.argv[4]) # n
	if sys.argv[1] == '0':
		#Input from file
		f = open(sys.argv[3], "r")
		text = f.read()
		f.close()
	if sys.argv[1] == '1':
		#Input from arg
		text = sys.argv[3]

	output = int(sys.argv[2])
	n = float(sys.argv[4])
	summarize(text, output, n)
else:
	print("Please use the correct argument formatting.")