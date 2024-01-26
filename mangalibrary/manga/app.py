from mangadex.requests import MangaDexAPI 
from data_processing.process_response import process_search_results

manga_dex_api = MangaDexAPI()
search_manga = manga_dex_api.search_manga


results = manga_dex_api.fetch_all_pages(
    included_tag_names=["Action", "Adventure"],
    excluded_tag_names=["Horror"],
    order={"rating": "desc", "followedCount": "desc"},
    # Add other parameters as needed
)

process_search_results(results)