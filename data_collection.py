from imdb import IMDb, IMDbError
from requests.exceptions import RequestException
from xml.sax._exceptions import SAXException
import random
import csv
import json
import time
import pandas as pd
import xml.sax
import requests
import untangle
import re
import time
import requests
import itertools
from lxml.html import fromstring
from bs4 import BeautifulSoup
from itertools import cycle
from parameters import Parameters
from exceptions import EmptyResults


def extract_movies(num_of_samples):
    movies_titles = read_sample_movies_titles()[0:num_of_samples]
    ia = IMDb()
    movie_df = pd.DataFrame(columns=['id', 'imdb_id', 'title', 'kind', 'url', 'documents'])
    
    for i, title in movies_titles.iteritems():
        try:
            print(f'Extracting movies and tv shows, title = {title}, iter = {i}')
            search_results = ia.search_movie(title)
            if search_results:
                movie = search_results[0]
                ia.update(movie, info=['main', 'synopsis', 'plot'])
                url = f'https://www.imdb.com/title/tt{movie.movieID}'
                reviews = scrap_movie_reviews(movie.movieID)
                summary_list = [summary.split('::')[0] for summary in movie['plot']]
                document_list = movie['synopsis'] + summary_list + reviews
                movie_df.loc[len(movie_df)] = [len(movie_df), movie.movieID, movie['title'], movie['kind'], url, '::'.join(document_list)]
            else:
                print('Imdb search fail')
        except IMDbError as e:
            print(e)

    movie_df.to_csv(Parameters.generated_data_path + Parameters.raw_movie_csv_name, index=False, sep=',', encoding='utf-8')  


def extract_games(num_of_samples):
    games_titles = read_sample_games_titles()[0:num_of_samples]
    game_df = pd.DataFrame(columns=['id', 'giantbomb_id', 'title', 'url', 'documents'])
    
    for i, title in enumerate(games_titles):
        print(f"Extracting games, title = {title}, iter = {i}")
        empty_results_retry_count = 0
        while True:
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
                api_key = '4b306930406dea7cece3c835916b9c9ac17c1082'
                giantbomb_game_id = None
                site_detail_url = ''
                game_deck = ''
                game_description = ''
                review_deck = ''
                review_description = ''

                # Search the game by the title text
                url = f'https://www.giantbomb.com/api/search/?api_key={api_key}&format=json&query={title}&field_list=id&resources=game'
                response = requests.get(url, headers=headers)
                results = response.json()['results']
                if results:
                    giantbomb_game_id = response.json()['results'][0]['id']
                else:
                    raise EmptyResults

                # Request info of the game by giantbomb id
                url = f'https://www.giantbomb.com/api/game/{giantbomb_game_id}/?api_key={api_key}&format=json&field_list=site_detail_url,deck,description,reviews'
                response = requests.get(url, headers=headers)
                results = response.json()['results']
                if results:
                    site_detail_url = results['site_detail_url']
                    if results['deck']:
                        game_deck = results['deck']
                    if results['description']:
                        game_description = results['description']
                else:
                    raise EmptyResults
            
                # Request first staff review of the game (if any)
                if 'reviews' in results:
                    url = results['reviews'][0]['api_detail_url']
                    response = requests.get(f'{url}?api_key={api_key}&format=json&field_list=deck,description', headers=headers)
                    results = response.json()['results']
                    if results:
                        results = response.json()['results']
                    else:
                        raise EmptyResults
                    review_deck = results['deck']
                    review_description = results['description']
                
                document = f'{game_deck}::{game_description}::{review_deck}::{review_description}'
                game_df.loc[len(game_df)] = [len(game_df), giantbomb_game_id, title, site_detail_url, document]
            except RequestException:
                print('Requests error, retrying...')
                time.sleep(2)
                continue
            except EmptyResults:
                print(f'Empty Results, retrying, count = {empty_results_retry_count}')
                empty_results_retry_count += 1
                time.sleep(2)
                if empty_results_retry_count < Parameters.empty_results_retry_limit:
                    continue
                else:
                    print('Empty results retry limit exceeded')
            break
        time.sleep(2)

    game_df.to_csv(Parameters.generated_data_path + Parameters.raw_game_csv_name, index=False, sep=',', encoding='utf-8')


def extract_books(num_of_samples):
    goodreads_books_ids = read_sample_books_goodreads_ids()[0:num_of_samples]
    book_df = pd.DataFrame(columns=['id', 'goodreads_id', 'title', 'url', 'documents'])

    for i, goodreads_book_id in goodreads_books_ids.iteritems():
        while True:
            try:
                print(f'Extracting books, id = {str(goodreads_book_id)}, iter = {i}')
                url = 'https://www.goodreads.com/book/show/?id=' + str(goodreads_book_id) + '&format=xml&key=CoBtO9PVTZqNZ5tDLr9yGQ'
                detail_url = 'https://www.goodreads.com/book/show/?id=' + str(goodreads_book_id)
                parsed_xml = untangle.parse(url)
                title = parsed_xml.GoodreadsResponse.book.title.cdata
                print(f'Book title: {title}')
                description = parsed_xml.GoodreadsResponse.book.description.cdata
                book_df.loc[len(book_df)] = [len(book_df), goodreads_book_id, title, detail_url, description]
            except RequestException:
                print('Requests error, retrying...')
                continue
            except SAXException:
                print('Non-xml response, skipping')
                break
            break

    book_df.to_csv(Parameters.generated_data_path + Parameters.raw_book_csv_name, index=False, sep=',', encoding='utf-8')


def scrap_movie_reviews(id):
    url = f'https://www.imdb.com/title/tt{id}/reviews'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    main = soup.find('div', attrs={'id': 'main'})
    review_divs = main.find_all('div', class_='text show-more__control')
    reviews = [rd.text for rd in review_divs]
    return reviews


def read_sample_movies_titles():
    movies_df = pd.read_csv(f'{Parameters.item_source_data_path}movies.dat', sep='::', encoding='utf-8', engine='python')
    movies_df.set_index('MovieID', inplace=True)
    return movies_df['Title']


def read_sample_games_titles():
    games_df = pd.read_csv(f'{Parameters.item_source_data_path}steam-200k.csv', encoding='utf-8')
    return list(dict.fromkeys(games_df['title'].values))


def read_sample_books_goodreads_ids():
    books_df = pd.read_csv(f'{Parameters.item_source_data_path}books.csv', encoding='utf-8')
    books_df.set_index('id', inplace=True)
    return books_df['book_id']


def main():
    # extract_movies(10681)
    # extract_games(5155)
    extract_books(5000)


if __name__ == '__main__':
    main()


# For testing stuff
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
# api_key = '4b306930406dea7cece3c835916b9c9ac17c1082'
# url = f'https://www.giantbomb.com/api/search/?api_key={api_key}&format=json&query=Pixel Heroes Byte & Magic&field_list=id&resources=game'
# response = requests.get(url, headers=headers)
# giantbomb_game_id = response.json()['results'][0]['id']
# print(giantbomb_game_id)


# ia = IMDb()
# print(ia.get_movie_infoset())
# print(ia.search_movie('Shanghai Triad (Yao a yao yao dao waipo qiao) (1995)'))
# ex1 = ia.get_movie('0120004', info=['main', 'synopsis', 'plot', 'vote details', 'reviews'])
# ex2 = ia.get_movie('0133093', info=['main', 'synopsis', 'plot'])
# print(ex1['synopsis'])
# print(ex1['summaries'])
# print(type(ex2['synopsis'][0]))
# print(ia.get_movie_infoset())
# print(ex1.infoset2keys)
# print(ex2['kind'])
# print(ex1['reviews'])

# reviews = extract_movie_reviews(4154756)
# print(reviews)
# reviews = extract_game_reviews('https://www.gamespot.com/soma/reviews/')
# print(reviews)
# reviews = extract_book_reviews(1)
# print(reviews)
# print(len(reviews))