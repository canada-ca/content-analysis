# functions to do basic analysis of the text content
# basic analysis based on keywords

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from gensim import corpora
from preprocess_text import lemmatized
from preprocess_text import stemmed
from preprocess_text import bag
from preprocess_text import comments
from describe_csv import entry_list
from textblob import TextBlob
from nltk.collocations import *
import nltk

# output file name
fileoutput = "OG_ActionPlan_Analyze_8.csv"
# title of original dataset
dataset = "Open Government Action Plan (Individual Comments)"

# create LDA model with gensim to look at the main topics present across the comments
def lda(data, topics, words):
    dictionary = corpora.Dictionary(data)
    corpus = [dictionary.doc2bow(word) for word in data]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=topics, id2word=dictionary, passes=20)
    return ldamodel.print_topics(num_topics=topics, num_words=words)

# calculate frequency of words across the entire corpus and returns a list of the top n words
def word_frequency():
    wordfreq = []
    # calculate the number of times each word occurs
    for word in bag:
        wordfreq.append(bag.count(word))
    # combine the words and their frequencies into a 2D list
    zipped = zip(bag, wordfreq)
    backwards = sorted(zipped, key = lambda x: x[1])
    results = list(reversed(backwards))
    final = []
    for result in results:
        if result not in final:
            final.append(result)
    return final

# get the top n number of most frequently occurring words
# returns a list of tuple objects
def get_top(n):
    list = word_frequency()
    new = []
    for i in range(0,n):
        new.append(list[i])
    return new

# word_frequency()
# print(get_top(5))

# what if the keyword comes up more than once in one comment?
# returns a list of the entry_list objects that contain that word
# data input is a list of token lists
def keyword_search(keyword, data):
    indexes = []
    entries = []
    for i in range (0, len(data)):
        for word in data[i]:
            if keyword in word:
                indexes.append(i+1)
    for i in indexes:
        entries.append(entry_list[i])
    return entries

# what is the theory behind this? It doesn't seem super effective...
# input a single string (sentence or comment)
def sentiment(comment):
    sentence = TextBlob(comment)
    return sentence.sentiment

# lists of key words relating to certain topics ("inclusive growth" in this case)
# STEM THESE IF YOU ARE COMPARING WITH STEMS
sustainable = ['green', 'energy', 'reuse', 'reduce', 'environment', 'clean']
shared = ['team', 'community', 'communicate', 'participate', 'local', 'public', 'collaborate']
strong = ['empower', 'steady', 'innovate', 'efficient', 'motivate']

# returns a list of entry object lists
# data = a preprocessed list of list of tokens
# words = a list of strings
def match_keywords(data, words):
    all = []
    for word in words:
        if len(keyword_search(word, data))>0:
            all.append(keyword_search(word, data))
    return all

# NOT WORKING YET
def phrases():
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(bag)
    finder.apply_freq_filter(2)
    print(finder.nbest(bigram_measures.pmi,2))

# input is the output list of entry_lists from the match_keywords algorithm
def print_entries(data):
    for entry_list in data:
        for entry in entry_list:
            print(entry.comment)
            print(entry.id)
            print(entry.userinfo)
            print(entry.date)
            print(entry.event)

# input is the output list of entry_lists from the match_keywords algorithm
def total_elements(data):
    count = 0
    for entry_list in data:
        for entry in entry_list:
            count = count + 1
    return count


def analyze():
    file = open(fileoutput, "w")
    file.write("This analysis is from the " + dataset + " dataset. \n")
    file.write("SAMPLE OUTPUT OF ANALYSIS\n\n")
    file.write("TEN MOST FREQUENTLY OCCURRING WORDS\n")
    top = get_top(10)
    file.write("Word, Number of Occurrences\n")
    for i in top:
        file.write(i[0] + "," + str(i[1]) + "\n")
    file.write("\nTHREE PRIMARY TOPICS\n")
    topics = lda(lemmatized, 3, 3)
    for i in range(0, len(topics)):
        file.write("Topic " + str(i+1) + "\n")
        file.write("Value, Topic\n")
        first = topics[i][1].split("+")
        for i in first:
            second = i.split("*")
            file.write(second[0] + "," + second[1] + "\n")
    file.write("\n")
    file.write("INCLUSIVE GROWTH KEYWORD ANALYSIS\n")
    sustainable_words = match_keywords(lemmatized, sustainable)
    shared_words = match_keywords(lemmatized, shared)
    strong_words = match_keywords(lemmatized, strong)
    file.write("Subtheme, Total Number of Comments, Percent of all Comments\n")
    file.write("Sustainable," + str(total_elements(sustainable_words)) + "," + str(total_elements(sustainable_words)/len(comments)*100)+ "\n")
    file.write("Shared," + str(total_elements(shared_words)) + "," + str(total_elements(shared_words)/len(comments)*100) + "\n")
    file.write("Strong," + str(total_elements(strong_words)) + "," + str(total_elements(strong_words)/len(comments)*100) + "\n\n")
    file.write("1. SUSTAINABLE \n\n")
    for entry_list in sustainable_words:
        for entry in entry_list:
            file.write("Comment," + entry.comment + "\n")
            file.write("ID," + entry.id + "\n")
            file.write("User Info, " + entry.userinfo + "\n")
            file.write("Date," + entry.date + "\n")
            file.write("Event," + entry.event + "\n\n")
    file.write("2. SHARED \n\n")
    for entry_list in shared_words:
        for entry in entry_list:
            file.write("Comment," + entry.comment + "\n")
            file.write("ID," + entry.id + "\n")
            file.write("User Info," + entry.userinfo + "\n")
            file.write("Date," + entry.date + "\n")
            file.write("Event," + entry.event + "\n\n")
    file.write("3. STRONG \n\n")
    for entry_list in strong_words:
        for entry in entry_list:
            file.write("Comment," + entry.comment + "\n")
            file.write("ID," + entry.id + "\n")
            file.write("User Info," + entry.userinfo + "\n")
            file.write("Date," + entry.date + "\n")
            file.write("Event," + entry.event + "\n\n")

    file.close()


analyze()

