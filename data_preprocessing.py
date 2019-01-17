import nltk
import string

def remove_non_ascii_char(text):
    printable = set(string.printable)
    return ''.join(filter(lambda x: x in printable, text))

def extract_nouns_and_adjs(tokenized_text):
    tagged_text = nltk.pos_tag(tokenized_text)
    grammar = 'NOUN_OR_ADJ:{<NN>||<JJ>}'
    parse_result = nltk.RegexpParser(grammar).parse(tagged_text)
    nouns_and_adjs = []
    
    for elem in parse_result:
        if type(elem) == nltk.tree.Tree:
            nouns_and_adjs.append(' '.join([pair[0] for pair in elem.leaves()]))

    return ' '.join(nouns_and_adjs)

def preprocess_text(text):
    text_ascii_char_only = remove_non_ascii_char(text)
    tokenized_text = nltk.word_tokenize(text_ascii_char_only)
    return extract_nouns_and_adjs(tokenized_text)
