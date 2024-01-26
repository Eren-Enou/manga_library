# def process_manga_details(manga_data):
#     # Example of processing a response from MangaDexAPI.fetch_manga_details
#     manga = Manga(
#         title=manga_data['data']['title'],
#         description=manga_data['data']['description'],
#         cover_image_url=manga_data['data']['coverImage']['large'],
#         # Add other fields as necessary
#     )
#     manga.save()

def process_search_results(results):
    if 'data' in results:
        for manga in results['data']:
            title = manga['attributes']['title'].get('en', 'No Title Available')
            print(title)

# Assuming 'results' contains the response from search_manga("Naruto")

