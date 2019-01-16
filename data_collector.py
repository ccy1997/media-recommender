from imdb import IMDb
import csv
import json
import urllib.request
import urllib.error
import requests
import untangle

def extract_movies_and_tv_shows(start_id, end_id):
    ids = range(start_id, end_id)
    prepended_ids = [str(i).zfill(7) for i in ids]
    ##print(prepended_ids)
    ia = IMDb()
    writer = csv.writer(open("movies.csv", mode="w", newline=''), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['id', 'title', 'kind', 'synopsis', 'summaries', 'votes'])
    
    for i in prepended_ids:
        print('Extracting movies and tv shows, id = ' + i)
        movie = ia.get_movie(i, info=['main', 'synopsis', 'plot'])
        if 'title' in movie and 'kind' in movie and 'synopsis' in movie and 'plot' in movie and 'votes' in movie:
            summaries = '::'.join([summary.split('::')[0] for summary in movie['plot']])
            writer.writerow([i, movie['title'], movie['kind'], movie['synopsis'][0], summaries, movie['votes']])

def extract_games(start_offset, end_offset):
    writer = csv.writer(open("games.csv", mode="w", newline=''), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["id", "name", "description", "deck"])
    
    for i in range(start_offset, end_offset, 100):
        print('Extracting games, offset = ' + str(i))
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        url = 'https://www.gamespot.com/api/games/?api_key=8478350e6908059abd12fd068ef96925f6bfc1c3&offset=' + str(i) + '&field_list=id,name,deck,description&sort=id:asc&format=json'
        response = requests.get(url, headers=headers)
        games = response.json()['results']
        
        for game in games:
            if game['name'] != '' and game['description'] != '' and game['deck'] != '':
                writer.writerow([game['id'], game['name'], game['description'].replace('\r', '').replace('\n', ''), game['deck'].replace('\r', '').replace('\n', '')])

def extract_books(start_id, end_id):
    ids = range(start_id, end_id)
    writer = csv.writer(open("books.csv", mode="w", newline=''), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["id", "title", "isbn", "isbn13", "description"])

    for i in ids:
        try:
            print('Extracting books, id = ' + str(i))
            url = 'https://www.goodreads.com/book/show/?id=' + str(i) + '&format=xml&key=CoBtO9PVTZqNZ5tDLr9yGQ'
            parsed_xml = untangle.parse(url)
            id_ = parsed_xml.GoodreadsResponse.book.id.cdata
            title = parsed_xml.GoodreadsResponse.book.title.cdata
            isbn = str(parsed_xml.GoodreadsResponse.book.isbn.cdata)
            isbn13 = str(parsed_xml.GoodreadsResponse.book.isbn13.cdata)
            description = parsed_xml.GoodreadsResponse.book.description.cdata.encode('utf8')
            writer.writerow([id_, title, isbn, isbn13, description])
        except urllib.error.HTTPError as e:
            print(str(e))

##Test things
##ia = IMDb()
##print(ia.get_movie_infoset())
##ex1 = ia.get_movie('0100000', info=['main', 'synopsis', 'plot', 'vote details'])
##ex2 = ia.get_movie('0133093', info=['main', 'synopsis', 'plot'])
##print('synopsis' in ex1)
##print(type(ex2['synopsis'][0]))
##print(ia.get_movie_infoset())
##print(ex2.infoset2keys)
##print(ex2['kind'])

extract_movies_and_tv_shows(100000, 110000)
extract_games(0, 10000)
extract_books(1, 10000)
