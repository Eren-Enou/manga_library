from mangadex.requests import MangaDexAPI 
from data_processing.process_response import process_search_results

manga_dex_api = MangaDexAPI()
results = manga_dex_api.search_manga("Naruto")

process_search_results(results)