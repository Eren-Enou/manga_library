import requests

class MangaDexAPI:
    BASE_URL = 'https://api.mangadex.org'
    
    def fetch_all_pages(self, included_tag_names=None, excluded_tag_names=None, order=None, **filters):
        limit = 15  # Maximum number of items per page
        offset = 0  # Start at the beginning
        all_results = []

        while True:
            try:
                response = self.search_manga(limit=limit, offset=offset, included_tag_names=included_tag_names, excluded_tag_names=excluded_tag_names, order=order, **filters)
                all_results.extend(response['data'])

            except Exception as e:
                print(f"An error occurred: {e}")
                break  # Exit the loop in case of error

        return all_results


    def fetch_tags(self):
        """Fetch and return all available tags from MangaDex."""
        response = requests.get(f"{self.BASE_URL}/manga/tag")
        if response.status_code == 200:
            return response.json()["data"]
        else:
            response.raise_for_status()

    def search_manga(self, limit=20, offset=0, included_tag_names=None, excluded_tag_names=None, order=None, **filters):
        """
        Search for manga with various filters, including tag inclusion/exclusion, ordering, and other filters.
        
        :param included_tag_names: List of tag names to include.
        :param excluded_tag_names: List of tag names to exclude.
        :param order: Dictionary specifying ordering of results.
        :param filters: Additional filters as keyword arguments.
        """
        # Fetch all tags to map names to IDs
        all_tags = self.fetch_tags()
        included_tag_ids = [
            tag["id"] for tag in all_tags if tag["attributes"]["name"]["en"] in included_tag_names
        ] if included_tag_names else []

        excluded_tag_ids = [
            tag["id"] for tag in all_tags if tag["attributes"]["name"]["en"] in excluded_tag_names
        ] if excluded_tag_names else []

        # Prepare parameters for the API request
        params = {
            "limit": limit,
            "offset": offset,
            **{f"order[{key}]": value for key, value in (order or {}).items()},
            **filters,  # This should correctly include publicationDemographic[], status[], and contentRating[] as arrays
            
        }
        

        # Make the request
        try:
            response = requests.get(f"{self.BASE_URL}/manga", params=params)
            response.raise_for_status()  # Checks for HTTP errors
            data = response.json()
            return data

        except requests.HTTPError as e:
            print(f"HTTPError: {e.response.status_code} - {e.response.text}")
            # Decide how to handle the error. Raising it will stop execution unless caught elsewhere.
            raise
        except requests.RequestException as e:
            # Handles other requests-related errors (e.g., network issues)
            print(f"RequestException: {e}")
            raise
        except Exception as e:
            # Generic catch-all for other errors
            print(f"An unexpected error occurred: {e}")
            raise
        