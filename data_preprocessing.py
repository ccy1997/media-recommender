import nltk
import string
import re
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup

##def remove_non_ascii_char(text):
##    printable = set(string.printable)
##    return ''.join(filter(lambda x: x in printable, text))

def extract_nouns_and_adjs(tokenized_text):
    tagged_text = nltk.pos_tag(tokenized_text)
    grammar = 'NOUN_OR_ADJ:{<NN>||<JJ>}'
    parse_result = nltk.RegexpParser(grammar).parse(tagged_text)
    nouns_and_adjs = []
    
    for elem in parse_result:
        if type(elem) == nltk.tree.Tree:
            nouns_and_adjs.append(' '.join([pair[0] for pair in elem.leaves()]))

    return nouns_and_adjs

def lemmatize_words(tokenized_text):
    lemmatizer = WordNetLemmatizer()
    lemmatized_text = []
    tagged_text = nltk.pos_tag(tokenized_text)
    
    for pair in tagged_text:
        if pair[1] == 'NN':
            lemmatized_text.append(lemmatizer.lemmatize(pair[0], pos='n'))
        elif pair[1] == 'JJ':
            lemmatized_text.append(lemmatizer.lemmatize(pair[0], pos='a'))

    return lemmatized_text

def remove_html_tags(text):
    soup = BeautifulSoup(text, 'lxml')
    return soup.get_text()

def preprocess_text(text):
    text_no_html_tags = remove_html_tags(text)
    text_simple_apostrophe = replace_simple_apostrophe(text_no_html_tags)
    text_alphabets_only = remove_non_alphabet_except_dash(text_simple_apostrophe)
    tokenized_text = nltk.word_tokenize(text_alphabets_only)
    nouns_and_adjs = extract_nouns_and_adjs(tokenized_text)
    lemmatized_text = lemmatize_words(nouns_and_adjs)
    return ' '.join(lemmatized_text)

def replace_simple_apostrophe(text):
    return re.sub(r'’+', '\'', text)

def remove_non_alphabet_except_dash(text):
    return re.sub(r'[^a-zA-Z-\'’]+', ' ', text)
