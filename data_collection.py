from imdb import IMDb, IMDbError
import csv
import json
import urllib.request
import urllib.error
import pandas as pd
import xml.sax
import requests
import untangle
import re
import time
import requests
from lxml.html import fromstring
from bs4 import BeautifulSoup
from itertools import cycle
from parameters import Parameters


def extract_movies_and_tv_shows(start_id, end_id):
    imdb_ids = range(start_id, end_id)
    prepended_imda_ids = [str(i).zfill(7) for i in imdb_ids]
    ia = IMDb()
    movie_df = pd.DataFrame(columns=['id', 'imdb_id', 'title', 'kind', 'documents'])
    
    for imdb_id in prepended_imda_ids:
        try:
            print('Extracting movies and tv shows, id = ' + imdb_id)
            movie = ia.get_movie(imdb_id, info=['main', 'synopsis', 'plot'])
            
            if 'title' in movie and 'kind' in movie and 'synopsis' in movie and 'plot' in movie:
                reviews = extract_movie_and_tv_reviews(imdb_id)
                summary_list = [summary.split('::')[0] for summary in movie['plot']]
                document_list = movie['synopsis'] + summary_list + reviews
                movie_df.loc[len(movie_df)] = [len(movie_df), imdb_id, movie['title'], movie['kind'], '::'.join(document_list)]
                
        except IMDbError as e:
            print(e)
        except urllib.error.HTTPError as e:
            print(e)

    movie_df.to_csv(Parameters.data_folder_path + Parameters.raw_movie_csv_name, index=False, sep=',', encoding='utf-8')  


def extract_games(start_offset, end_offset):
    game_df = pd.DataFrame(columns=['id', 'gamespot_id', 'title', 'url', 'documents'])
    
    for i in range(start_offset, end_offset, 100):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
        url = 'https://www.gamespot.com/api/games/?api_key=8478350e6908059abd12fd068ef96925f6bfc1c3&offset=' + str(i) + '&field_list=id,name,site_detail_url,deck,description&sort=id:asc&format=json'
        response = requests.get(url, headers=headers)
        game_list = response.json()['results']
        
        for game in game_list:
            if game['id'] != '' and game['name'] != '' and game['description'] != '' and game['deck'] != '':
                print('Extracting games, id = ' + str(game['id']))
                reviews = extract_game_reviews(game['site_detail_url'] + 'reviews')
                document_list = [game['description'], game['deck']] + reviews
                game_df.loc[len(game_df)] = [len(game_df), game['id'], game['name'], game['site_detail_url'], '::'.join(document_list)]

    game_df.to_csv(Parameters.data_folder_path + Parameters.raw_game_csv_name, index=False, sep=',', encoding='utf-8')


def extract_books(start_id, end_id):
    goodreads_ids = range(start_id, end_id)
    book_df = pd.DataFrame(columns=['id', 'goodreads_id', 'title', 'isbn', 'isbn13', 'documents'])

    for goodreads_id in goodreads_ids:
        try:
            url = 'https://www.goodreads.com/book/show/?id=' + str(goodreads_id) + '&format=xml&key=CoBtO9PVTZqNZ5tDLr9yGQ'
            parsed_xml = untangle.parse(url)
            title = parsed_xml.GoodreadsResponse.book.title.cdata
            isbn = str(parsed_xml.GoodreadsResponse.book.isbn.cdata)
            isbn13 = str(parsed_xml.GoodreadsResponse.book.isbn13.cdata)
            description = parsed_xml.GoodreadsResponse.book.description.cdata
            
            if title != '' and (isbn != '' or isbn13 != '') and description != '':
                print('Extracting books, id = ' + str(goodreads_id))
                book_df.loc[len(book_df)] = [len(book_df), goodreads_id, title, isbn, isbn13, description]
                
        except:
            print('Untangle HTTP connection error')

    book_df.to_csv(Parameters.data_folder_path + Parameters.raw_book_csv_name, index=False, sep=',', encoding='utf-8')


def extract_movie_and_tv_reviews(id):
    url = 'https://www.imdb.com/title/tt' + id + '/reviews'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    main = soup.find('div', attrs={'id': 'main'})
    review_divs = main.find_all('div', class_='text show-more__control')
    reviews = [rd.text for rd in review_divs]
    return reviews


def extract_game_reviews(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    site_main = soup.find('div', attrs={'id': 'site-main'})
    review_title_divs = site_main.find_all('h3', class_='media-title')
    review_content_divs = site_main.find_all('p', class_='userReview-list__deck')
    reviews = []

    for rtd in review_title_divs:
        reviews.append(rtd.text)

    for rcd in review_content_divs:
        reviews.append(rcd.text.strip('Read Full Review'))

    return reviews


def extract_book_reviews(id, proxy):
    url = 'https://www.goodreads.com/book/show/' + str(id)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    review_texts = []

    while True:
        try:
            html = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy}).text
            soup = BeautifulSoup(html, 'html.parser')
            book_reviews_div = soup.find('div', attrs={'id': 'bookReviews'})
            review_containers = book_reviews_div.find_all('div', class_='friendReviews elementListBrown')

            for rc in review_containers:
                span = rc.find('span', id=re.compile(r'^freeText\d+'))
                
                if (span):                          # Long review
                    review_texts.append(span.text)
                else:                               # Short review
                    span = rc.find('span', id=re.compile(r'^freeTextContainer\d+'))
                    review_texts.append(span.text)
        except:
            print('Retry (' + str(id) + ')')
            continue
        break

    return review_texts


def main():
    extract_movies_and_tv_shows(120000, 125000)
    extract_games(0, 5000)
    extract_books(1, 5000)


if __name__ == '__main__':
    main()


# For testing stuff

# ia = IMDb()
# print(ia.get_movie_infoset())
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