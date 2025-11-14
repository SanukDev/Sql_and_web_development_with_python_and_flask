TOKEN ="Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZDNiZTc2ZDhiMGU3YzVkYTM3NDgzYTBmYzQ1MDU4OCIsIm5iZiI6MTc1Mjk3MzQzMS43OTUsInN1YiI6IjY4N2M0MDc3Yjk0ZTY2N2Y4YjUyODhhZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.9QKc6gz2tOqR5yA_GxpC3XoeKK4YWPZBpPHNbeOw-d8"
KEY = "ed3be76d8b0e7c5da37483a0fc450588"
headers = {
            "accept": "application/json",
            "Authorization": TOKEN
        }
import requests
class CollectMovies:

    def __init__(self, query):
        self.query = query

    def collect(self):
        url = f"https://api.themoviedb.org/3/search/movie?query={self.query}&include_adult=true&language=en-US&page=1"
        titles_movies = []
        response = requests.get(url, headers=headers)
        datas = response.json()
        data_movies = datas['results']
        for data in data_movies:
            titles_movies.append({
                'title': data['original_title'],
                'id': data['id'],
                'date':data['release_date'],
                'overview':data['overview'],
            })

        return titles_movies

    def found_movie_by_id(self, id):
        data_movies = []
        data = self.collect()
        for title in data:
            if title['id'] == id:
                data_movies.append({
                    'title': title['title'],
                    'id': title['id'],
                    'date': title['date'],
                    'overview': title['overview'],
                })
        return data_movies

movie = CollectMovies("the matrix")
data = movie.collect()
datas = movie.found_movie_by_id(603)


class CollectImage:
    def __init__(self, id_img):
        self.id_img = id_img

    def collect(self):
        url = f"https://api.themoviedb.org/3/movie/{self.id_img}?language=en-US"

        response = requests.get(url, headers=headers)
        data = response.json()
        return data['poster_path']

