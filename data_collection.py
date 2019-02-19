from imdb import IMDb, IMDbError
import csv
import json
import urllib.request
import urllib.error
import pandas as pd
import xml.sax
import requests
import untangle
from parameters import Parameters


def extract_movies_and_tv_shows(start_id, end_id):
    imdb_ids = range(start_id, end_id)
    prepended_imda_ids = [str(i).zfill(7) for i in imdb_ids]
    ia = IMDb()
    movie_df = pd.DataFrame(columns=['id', 'imdb_id', 'title', 'kind', 'votes', 'documents'])
    
    for imdb_id in prepended_imda_ids:
        try:
            print('Extracting movies and tv shows, id = ' + imdb_id)
            movie = ia.get_movie(imdb_id, info=['main', 'synopsis', 'plot'])
            
            if 'title' in movie and 'kind' in movie and 'synopsis' in movie and 'plot' in movie and 'votes' in movie:
                summary_list = [summary.split('::')[0] for summary in movie['plot']]
                document_list = [movie['synopsis'][0]] + summary_list
                movie_df.loc[len(movie_df)] = [len(movie_df), imdb_id, movie['title'], movie['kind'], movie['votes'], '::'.join(document_list)]
                
        except IMDbError as e:
            print(e)
        except urllib.error.HTTPError as e:
            print(e)

    movie_df.to_csv(Parameters.data_folder_path + Parameters.raw_movie_csv_name, index=False, sep=',', encoding='utf-8')  


def extract_games(start_offset, end_offset):
    game_df = pd.DataFrame(columns=['id', 'gamespot_id', 'title', 'documents'])
    
    for i in range(start_offset, end_offset, 100):
        print('Extracting games, offset = ' + str(i))
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        url = 'https://www.gamespot.com/api/games/?api_key=8478350e6908059abd12fd068ef96925f6bfc1c3&offset=' + str(i) + '&field_list=id,name,deck,description&sort=id:asc&format=json'
        response = requests.get(url, headers=headers)
        game_list = response.json()['results']
        
        for game in game_list:
            if game['id'] != '' and game['name'] != '' and game['description'] != '' and game['deck'] != '':
                documents = game['description'] + '::' + game['deck']
                game_df.loc[len(game_df)] = [len(game_df), game['id'], game['name'], documents]

    game_df.to_csv(Parameters.data_folder_path + Parameters.raw_game_csv_name, index=False, sep=',', encoding='utf-8')


def extract_books(start_id, end_id):
    goodreads_ids = range(start_id, end_id)
    book_df = pd.DataFrame(columns=['id', 'goodreads_id', 'title', 'isbn', 'isbn13', 'documents'])

    for goodreads_id in goodreads_ids:
        try:
            print('Extracting books, id = ' + str(goodreads_id))
            url = 'https://www.goodreads.com/book/show/?id=' + str(goodreads_id) + '&format=xml&key=CoBtO9PVTZqNZ5tDLr9yGQ'
            parsed_xml = untangle.parse(url)
            title = parsed_xml.GoodreadsResponse.book.title.cdata
            isbn = str(parsed_xml.GoodreadsResponse.book.isbn.cdata)
            isbn13 = str(parsed_xml.GoodreadsResponse.book.isbn13.cdata)
            description = parsed_xml.GoodreadsResponse.book.description.cdata
            
            if title != '' and (isbn != '' or isbn13 != '') and description != '':
                book_df.loc[len(book_df)] = [len(book_df), goodreads_id, title, isbn, isbn13, description]
                
        except urllib.error.HTTPError as e:
            print(e)
        except xml.sax.SAXParseException as e:
            print(e)

    book_df.to_csv(Parameters.data_folder_path + Parameters.raw_book_csv_name, index=False, sep=',', encoding='utf-8')

def main():
    extract_movies_and_tv_shows(120000, 120200)
    extract_games(0, 500)
    extract_books(1, 50)


if __name__ == '__main__':
    main()


# For debugging
# ia = IMDb()
# print(ia.get_movie_infoset())
# ex1 = ia.get_movie('0120004', info=['main', 'synopsis', 'plot', 'vote details'])
# ex2 = ia.get_movie('0133093', info=['main', 'synopsis', 'plot'])
# print(ex1['synopsis'])
# print(ex1['summaries'])
# print(type(ex2['synopsis'][0]))
# print(ia.get_movie_infoset())
# print(ex1.infoset2keys)
# print(ex2['kind'])