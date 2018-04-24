# text preprocessing functions to do before the analysis
# tokenizes, removes punctuation, converts to lower case, and stems or lemmatizes

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
from describe_csv import entry_list
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import wordnet

stopWords = set(stopwords.words('english'))

# tokenized list of comments --> 2D list
tokenized = []

# list of all the comments from the CSV dataset
comments = []

# fill comments list from the "entry_list" variable
for entry in entry_list:
    comments.append(entry.comment)

# do not include the CSV file header in the analysis
del comments[0]


# splits strings into tokens and removes punctuation
def tokenize():
    tokenizer = RegexpTokenizer(r'\w+')
    words_filtered = [tokenizer.tokenize(i) for i in comments]
    for i in words_filtered:
        tokenized.append(i)
    return tokenized


# converts to lower case, removes stop words, and converts words to lemma
# includes POS tagging
# need to tokenize first!
# default POS tag is NOUN
def lemmatize():
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
    lemmatized = []
    for i in tokenized:
        t = []
        for word in i:
            if word not in stopWords:
                if word != "I":
                    t.append(wordnet_lem.lemmatize(word.lower(), get_wordnet_pos(nltk.pos_tag([word])[0][1])))
        lemmatized.append(t)
    return lemmatized


# converts to lower case, removes stop words, and converts words to their stems
# need to tokenize first!
def stemming():
    stemmer = PorterStemmer()
    combine = []
    for i in tokenized:
        t = []
        for word in i:
            if word not in stopWords:
                if word != "I":
                    t.append(stemmer.stem(word.lower()))
        combine.append(t)
    return combine


# creates a single list with all the words
def bag_of_words(data):
    combined = []
    for i in data:
        for word in i:
            combined.append(word)
    return combined


tokenize()
lemmatized = lemmatize()
stemmed = stemming()
bag_lem = bag_of_words(lemmatized)
bag_stem = bag_of_words(stemmed)


def testing():
    print(entry_list[4].comment)
    print(comments[3])
    print(tokenized[3])
    print(stemmed[3])
    print(lemmatized[3])
    print(bag_lem)
    print(bag_stem)
# testing()
