import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import csv
import gensim
from gensim import corpora
from nltk.stem import PorterStemmer
from preprocess_text import lemmatized
from preprocess_text import stemmed
from preprocess_text import bag_lem
from preprocess_text import bag_stem
from preprocess_text import comments
from describe_csv import entry_list
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk

# --------------- VARIABLES TO EDIT ---------------

# output file name
# RESTRICTIONS: needs to have extension ".csv", String
fileoutput = r"CHANGE THIS"

# title of original dataset
# RESTRICTIONS: String
dataset = "Sample Dataset 1"

# lists of key words relating to certain topics/themes ("inclusive growth" in this case)
# RESTRICTIONS: list of Strings, keep variable names the same (else, change lines 96-111 and 221-226)
sustainable = ['green', 'energy', 'reuse', 'reduce', 'environment', 'clean']
shared = ['team', 'community', 'communicate', 'participate', 'local', 'public', 'collaborate']
strong = ['empower', 'steady', 'innovate', 'efficient', 'motivate']

# type of preprocessing approach to apply
# RESTRICTIONS: must be one of the following: "lemmatize" or "stem"
preprocess_type = "lemmatize"

# number of topics
# RESTRICTIONS: integer
topics = 5

# number of words per topic
# RESTRICTIONS: integer
words = 3

# sentiment lexicon
# RESTRICTIONS: CSV file of positive an negative words:
# two columns, no headers: 1st column is negative words and 2nd column is positive words
sentiment_lexicon = r'CHANGE THIS'

# --------------- END OF EDITING ---------------

# reading the sentiment lexicon file
with open(sentiment_lexicon, encoding='cp1252') as csvfile:
    negative_words = []
    positive_words = []
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if row[0] != "":
            negative_words.append(row[0])
        if row[1] != "":
            positive_words.append(row[1])

# stem the key words
def stemming(keywords):
    stemmer = PorterStemmer()
    output = []
    for word in keywords:
        output.append(stemmer.stem(word.lower()))
    return output

# lemmatize the keywords
def lemmatize(keywords):
    output = []

    def get_wordnet_pos(treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN
    wordnet_lem = WordNetLemmatizer()
    for word in keywords:
        output.append(wordnet_lem.lemmatize(word.lower(), get_wordnet_pos(nltk.pos_tag([word])[0][1])))
    return output


# to remove doubles from the list of keywords after it has been stemmed or lemmatized
def remove_doubles(data_list):
    a = list(set(data_list))
    return a

if preprocess_type == "lemmatize":
    all_data = lemmatized
    bag = bag_lem
    sustainable_ = remove_doubles(lemmatize(sustainable))
    shared_ = remove_doubles(lemmatize(shared))
    strong_ = remove_doubles(lemmatize(strong))
    positive_ = remove_doubles(lemmatize(positive_words))
    negative_ = remove_doubles(lemmatize(negative_words))
if preprocess_type == "stem":
    all_data = stemmed
    bag = bag_stem
    sustainable_ = remove_doubles(stemming(sustainable))
    shared_ = remove_doubles(stemming(shared))
    strong_ = remove_doubles(stemming(strong))
    positive_ = remove_doubles(stemming(positive_words))
    negative_ = remove_doubles(stemming(negative_words))


# create LDA model with gensim to look at the main topics present across the comments
def lda(data, topics, words):
    dictionary = corpora.Dictionary(data)
    corpus = [dictionary.doc2bow(word) for word in data]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=topics, id2word=dictionary, passes=30)
    return ldamodel.print_topics(num_topics=topics, num_words=words)


# calculate frequency of words across the entire corpus and returns a list of the top n words
def word_frequency(b):
    wordfreq = []
    # calculate the number of times each word occurs
    for word in b:
        wordfreq.append(b.count(word))
    # combine the words and their frequencies into a 2D list
    zipped = zip(b, wordfreq)
    backwards = sorted(zipped, key=lambda x: x[1])
    results = list(reversed(backwards))
    final = []
    for result in results:
        if result not in final:
            final.append(result)
    return final


# get the top n number of most frequently occurring words
# returns a list of tuple objects
def get_top(n, b):
    temp = word_frequency(b)
    new = []
    for i in range(0, n):
        new.append(temp[i])
    return new


# what if the keyword comes up more than once in one comment?
# returns a list of the entry_list objects that contain that word
# data input is a list of token lists
def keyword_search(keyword, data):
    indexes = []
    entries = []
    for i in range(0, len(data)):
        for word in data[i]:
            if keyword == word:
                indexes.append(i + 1)
    for i in indexes:
        entries.append(entry_list[i])
    return entries


# returns a list of entry object lists
# data = a preprocessed list of list of tokens
# words = a list of strings
def match_keywords(data, words):
    tmp = []
    for word in words:
        if len(keyword_search(word, data)) > 0:
            tmp.append(keyword_search(word, data))
    return tmp


# input is the output list of entry_lists from the match_keywords algorithm
def print_entries(data):
    for el in data:
        for entry in el:
            print(entry.comment)
            print(entry.id)
            print(entry.userinfo)
            print(entry.date)
            print(entry.event)


# calculates the total number of matches in match_keyword
# input is the output list of entry_lists from the match_keywords algorithm
def total_elements(data):
    count = 0
    for el in data:
        for entry in el:
            count = count + 1
    return count


# outputs a summary CSV file
def analyze():
    file = open(fileoutput, "w")
    file.write("This analysis is from the " + dataset + " dataset. \n")
    file.write("SAMPLE OUTPUT OF ANALYSIS\n\n")
    file.write("TEN MOST FREQUENTLY OCCURRING WORDS\n")
    top = get_top(15, bag)
    file.write("Word, Number of Occurrences\n")
    for i in top:
        file.write(i[0] + "," + str(i[1]) + "\n")
    file.write("\nTHREE PRIMARY TOPICS\n")
    topic_output = lda(all_data, topics, words)
    for i in range(0, len(topic_output)):
        file.write("Topic " + str(i + 1) + "\n")
        file.write("Value, Topic\n")
        first = topic_output[i][1].split("+")
        for i in first:
            second = i.split("*")
            file.write(second[0] + "," + second[1] + "\n")
    file.write("\n")
    file.write("INCLUSIVE GROWTH KEYWORD ANALYSIS\n")
    sustainable_words = match_keywords(all_data, sustainable_)
    shared_words = match_keywords(all_data, shared_)
    strong_words = match_keywords(all_data, strong_)
    file.write("Subtheme, Total Number of Comments, Percent of all Comments\n")
    file.write("Sustainable," + str(total_elements(sustainable_words)) + "," + str(
        total_elements(sustainable_words) / len(comments) * 100) + "\n")
    file.write("Shared," + str(total_elements(shared_words)) + "," + str(
        total_elements(shared_words) / len(comments) * 100) + "\n")
    file.write("Strong," + str(total_elements(strong_words)) + "," + str(
        total_elements(strong_words) / len(comments) * 100) + "\n\n")
    file.write("SENTIMENT KEYWORD ANALYSIS\n")
    negative_match = match_keywords(all_data, negative_)
    positive_match = match_keywords(all_data, positive_)
    file.write("Negative Total" + "," + "Positive Total\n")
    total_negative = total_elements(negative_match)
    total_positive = total_elements(positive_match)
    file.write(str(total_negative) + "," + str(total_positive) + "\n\n")
    difference = total_positive-total_negative
    if difference>0:
        sentiment = "positive"
    elif difference<0:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    file.write("The responses from this dataset are overall " + sentiment)
    file.close()

analyze()

