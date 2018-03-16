# text preprocessing functions to do before the analysis
# tokenizes, removes punctuation, converts to lower case, and stems or lemmatizes

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
from describe_csv import entry_list
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import nltk
# nltk.download('averaged_perceptron_tagger')
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
    wordsFiltered = [tokenizer.tokenize(i) for i in comments]
    for i in wordsFiltered:
        tokenized.append(i)
    return tokenized

# TO DO: add the POS to lemmatization
def pos_tag():
    tagged = []
    for word in comments:
        tagged.append(nltk.pos_tag(word))
    return tagged

# converts to lower case, removes stop words, and converts words to lemma
# need to tokenize first!
def lemmatize():
    wordnet_lem = WordNetLemmatizer()
    lemmatized = []
    for i in tokenized:
        t = []
        for word in i:
            if word not in stopWords:
                t.append(wordnet_lem.lemmatize(word.lower()))
        lemmatized.append(t)
    return lemmatized

#c onverts to lower case, removes stop words, and converts words to their stems
#need to tokenize first!
def stemming():
    stemmer = PorterStemmer()
    combine = []
    for i in tokenized:
        t = []
        for word in i:
            if word not in stopWords:
                if word not in string.punctuation[16]:
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
stemmed = stemming()
lemmatized = lemmatize()
bag = bag_of_words(lemmatized)

def testing():
    print(entry_list[4].comment)
    print(comments[3])
    print(tokenized[3])
    print(stemmed[3])
    print(lemmatized[3])
    print(bag)
#testing()