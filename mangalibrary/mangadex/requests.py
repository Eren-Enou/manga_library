import requests

class MangaDexAPI:
    BASE_URL = 'https://api.mangadex.org'

    def search_manga(self, title, limit=10):
        """Search for manga by title."""
        url = f"{self.BASE_URL}/manga"
        params = {
            'title': title,
            'limit': limit  # Limits the number of results returned
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

