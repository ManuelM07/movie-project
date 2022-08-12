import requests
from werkzeug.wrappers import response

# Por medio de esta api obtenos la informacion de la pelicula que queremos mostrar
API_KEY = ""


class ApiMovie:

    def __init__(self) -> None:

        self.parameters_title = {
            "api_key": API_KEY,
        }

        self.parameters_datails = {
            "api_key": API_KEY,
        }

    def get_data(self, movie_title):
        self.parameters_title["query"] = movie_title
        response = requests.get(url="https://api.themoviedb.org/3/search/movie", params=self.parameters_title)
        response.raise_for_status()
        data = response.json()
        return data["results"]

    def get_data_details(self, movie_id):
        response = requests.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}", params=self.parameters_datails)
        response.raise_for_status()
        data = response.json()
        return data
    
