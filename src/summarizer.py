import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import operator
import sys
nlp = spacy.load("en_core_web_sm")
# extractive summary by word count
#text = """This is an example text. We will use seven sentences and we will return 3. This blog is written by Yujian Tang. Yujian is the best software content creator. This is a software content blog focused on Python, your software career, and Machine Learning. Yujian's favorite ML subcategory is Natural Language Processing. This is the end of our example."""
# n = 3;
# text = """Russia has for the first time admitted losses of personnel on the Moskva, the flagship of its Black Sea Fleet, which sank last week.

# The defence ministry said one crew member had died and 27 were missing after the sinking, while the remaining 396 had been rescued. Previously it had made no mention of casualties.

# The BBC cannot independently verify these figures.

# The sinking of the missile cruiser is one of the defining events of the war in Ukraine so far. Russia says the ship went down because of a fire on board, but Ukraine says it sank it with missiles.

# And now, the wreckage of the pride of Russia's fleet has been declared an item of Ukrainian underwater cultural heritage, under the category of rare scientific or technical equipment.

# As the BBC's Joe Inwood reports, Ukraine's Ministry of Defence says the wreck can be admired "without much diving"."""

def summarize(text, output, n):
	# tokenize
	doc = nlp(text)

	# create dictionary
	word_scores = {}

	# Add all words, that aren't stop words or punctuation to the word_scores object 
	for word in doc:
		word_scores[word.text.lower()] = 0


	# loop through every sentence and give it a weight
	for word in doc:
		word = word.text.lower()
		if word in word_scores and word not in STOP_WORDS and word not in punctuation and "\n" not in word:
			word_scores[word] += 1

	# create a list of tuple (sentence text, score, index)
	sents = []
	# score sentences
	sent_score = 0
	#print(word_scores)
	for index, sent in enumerate(doc.sents):
		for word in sent:
			sent_score += word_scores[word.text.lower()]
			#print(word_scores[word.text.lower()])
		sents.append((sent.text.replace("\n", " "), sent_score / (len(sent) / 2), index))
		#print(sent.text.replace("\n", " "), sent_score ,len(sent), sent_score / (len(sent) / 2))
		sent_score = 0;


	# sort the sentences by word occurance(tuple index 1)
	#print("----- \n", sents)
	sents.sort(key=operator.itemgetter(1))
	#print("----- \n", sents)
	# return best rated n amount of sentences
	bestSents = sents[-n:]
	# keep the sentence order as in original text
	bestSents.sort(key=operator.itemgetter(2))

	# compile them into text
	summary_text = ""
	for sent in bestSents:
		summary_text += sent[0] + " "
		#print(sent[1])

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
	n = int(sys.argv[4])
	summarize(text, output, n)
else:
	print("Please use the correct argument formatting.")