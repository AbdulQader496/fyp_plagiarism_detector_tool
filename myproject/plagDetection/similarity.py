from re import match
import nltk
from nltk import data
from nltk.tokenize import punkt
from nltk.translate.bleu_score import sentence_bleu
from ..plagDetection import webSearch
from difflib import SequenceMatcher
import pandas as pd

nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('english'))


def purifyTxt(textFromFile):
    words = nltk.word_tokenize(textFromFile)
    return (" ".join([word for word in words if word not in stop_words]))


def webVerify(textFromFile, result_per_sentence):
    sentencess = nltk.sent_tokenize(textFromFile)
    matching_sites = []
    for url in webSearch.searchBing(query = textFromFile, num = result_per_sentence):
        matching_sites.append(url)

    for sentence in sentencess:
        for url in webSearch.searchBing(query = sentence, num = result_per_sentence):
            matching_sites.append(url)

    print(matching_sites)
    return (list(set(matching_sites)))


def similarity(st1,st2):
    return (SequenceMatcher(None,st1,st2).ratio())*100


def report(textFromFile):
    matching_sites = webVerify(purifyTxt(textFromFile), 2)
    matches = {}

    for i in range(len(matching_sites)):
        matches[matching_sites[i]] = similarity(textFromFile, webSearch.extractText(matching_sites[i]))
    
    matches = {a: b for a, b in sorted(matches.items(), key=lambda item: item[1], reverse=True)}
    return matches


def returnTableWithURL(dictionary):

    df = pd.DataFrame({'Similarity (%)': dictionary})
    print(dictionary)
    return df.to_html()

if __name__ == '__main__':
    report('test')
