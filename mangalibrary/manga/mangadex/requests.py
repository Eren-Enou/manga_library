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
            
    def get_manga_feed(self, manga_id, limit=10, order={'chapter': 'asc'}):
        params = {
            "limit": limit,
            "translatedLanguage[]": ['en'],
            "order[chapter]": order['chapter']
        }
        
        response = requests.get(f"{self.BASE_URL}/manga/{manga_id}/feed", params=params)
        print(f"response url manga_feed :{response.url}") 
        if response.status_code == 200:
            chapters = response.json()['data']
            return chapters
        else:
            print("Failed to fetch manga feed")
            return []

        
    # Fetching chapter metadata
    def get_chapter_metadata(self, chapter_id):

        response = requests.get(f"{self.BASE_URL}/at-home/server/{chapter_id}")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch chapter metadata")

    def search_manga(self, limit=20, offset=0, title=None, included_tag_names=None, excluded_tag_names=None, sort_by=None, **filters):
        """
        Search for manga with various filters, including tag inclusion/exclusion, sorting, and other filters.
        
        :param included_tag_names: List of tag names to include.
        :param excluded_tag_names: List of tag names to exclude.
        :param order: Dictionary specifying ordering of results.
        :param filters: Additional filters as keyword arguments.
        """
        # Fetch all tags to map names to IDs
        all_tags = self.fetch_tags()
        # print(all_tags)
        included_tag_ids = [
            tag["id"]
            for tag in all_tags
            if tag["attributes"]["name"]["en"].lower() in [name.lower() for name in included_tag_names]
        ]

        # print(f"included tags ids: {included_tag_ids}")

        excluded_tag_ids = [
            tag
            for tag in all_tags
            if tag["attributes"]["name"]["en"].lower() in [name.lower() for name in excluded_tag_names]
        ]
        # print(f"included tags ids: {excluded_tag_ids}")
        
        print("All tag names from API:")
        for tag in all_tags:
            print(tag["attributes"]["name"]["en"])

        print("Looking for tags:", included_tag_names)

        
        # Prepare parameters for the API request
        params = {
            "limit": limit,
            "offset": offset,
            "includes[]": 'cover_art',
            "includedTags[]": included_tag_ids,
            "excludedTags[]": excluded_tag_ids,
            **filters,  # Other filters
        }
        
        # Split the sort_by into field and direction if it's not None
        if sort_by:
            field, direction = sort_by.rsplit('_', 1)  # This splits from the right at the first underscore
            params[f"order[{field}]"] = direction
            
        if title:
            params['title'] = title

        # Make the request
        try:
            response = requests.get(f"{self.BASE_URL}/manga", params=params)
            response.raise_for_status()  # Checks for HTTP errors
            data = response.json()
            
            print(f"response url search_manga:{response.url}")  # Debugging: Print the URL to see how it's constructed
            for manga in data['data']:
                self.get_manga_feed(manga['id'])
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
        

    def start_reading(self, manga_id):
        chapters = self.get_manga_feed(manga_id, limit=1)  # Fetch only the first chapter for simplicity
        if chapters:
            print('gottem chapters')
            first_chapter_id = chapters[0]['id']
            chapter_metadata = self.get_chapter_metadata(first_chapter_id)
            
            # Assuming we want to print the URLs for the first chapter's pages
            if chapter_metadata:
                base_url = chapter_metadata['baseUrl']
                chapter_hash = chapter_metadata['chapter']['hash']
                page_filenames = chapter_metadata['chapter']['data']  # Assuming data quality here
                
                # Generate page URLs
                page_urls = [f"{base_url}/data/{chapter_hash}/{filename}" for filename in page_filenames]
                print("Page URLs for the first chapter:")
                for url in page_urls:
                    print(url)
                
                return page_urls
        else:
            print("No chapters found or failed to fetch chapters.")
            return []
