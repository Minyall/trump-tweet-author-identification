from nltk.tokenize import PunktSentenceTokenizer
from nltk import word_tokenize, pos_tag
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import preprocessor as p


def pos_tagging(text):
    '''
    Takes a string of words and returns a string with parts-of-speech of words
    INPUT: string
    OUTPUT: string
    '''
    pos = pos_tag(word_tokenize(text))
    string = ""
    for item in pos:
        string += item[1] + " "
    return string


def ner_tagging(text):
    '''
    Takes a string of words and uses the Stanford NER Tagger to replace names,
    places, and organizations with a standard thunderstorm
    INPUT: string
    OUTPUT: string
    '''
    st = StanfordNERTagger('stanford-ner/classifiers/english.all.3class.'
                           'distsim.crf.ser.gz', 'stanford-ner/stanford-ner.'
                           'jar', encoding='utf-8')
    ner = st.tag(word_tokenize(text))
    string = ""
    for item in ner:
        if item[1] != 'O':
            string += item[1] + ' '
        else:
            string += item[0] + ' '
    return string