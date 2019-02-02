import nltk
import pandas as pd
import re
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup


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


def replace_simple_apostrophe(text):
    return re.sub(r'’+', '\'', text)


def remove_non_alphabet_and_useless_symbols(text):
    return re.sub(r'[^a-zA-Z-\'’]+', ' ', text)


def preprocess_text(text):
    text_no_html_tags = remove_html_tags(text)
    text_simple_apostrophe = replace_simple_apostrophe(text_no_html_tags)
    text_alphabets_dash_apostrophe = remove_non_alphabet_and_useless_symbols(text_simple_apostrophe)
    tokenized_text = nltk.word_tokenize(text_alphabets_dash_apostrophe)
    nouns_and_adjs = extract_nouns_and_adjs(tokenized_text)
    lemmatized_text = lemmatize_words(nouns_and_adjs)
    return ' '.join(lemmatized_text)


def preprocess_item_documents(in_file_str, out_file_str):
    item_df = pd.read_csv('./' + in_file_str)
    item_df.set_index('id', inplace=True)
    item_remove_id = []
    print('Preprocessing ' + in_file_str + '...')
    
    for i, row in item_df.iterrows():
        item_df.at[i, 'title'] = remove_non_alphabet_and_useless_symbols(row['title'])
        documents = row['documents'].split('::')
        keywords = ' '.join([preprocess_text(d) for d in documents])
        item_df.at[i, 'documents'] = keywords

        if  pd.isna(item_df.at[i, 'title']) or pd.isna(item_df.at[i, 'documents']):
            item_remove_id.append(item_df.index[i])

    item_df.drop(item_remove_id, inplace=True)
    item_df.to_csv(out_file_str, sep=',', encoding='utf-8')


def main():
    preprocess_item_documents('unprocessed_movies.csv', 'preprocessed_movies.csv')
    preprocess_item_documents('unprocessed_games.csv', 'preprocessed_games.csv')
    preprocess_item_documents('unprocessed_books.csv', 'preprocessed_books.csv')


if __name__ == '__main__':
    main()