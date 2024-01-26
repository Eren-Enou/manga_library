
def process_search_results(results):
    if 'data' in results:
        for manga in results['data']:
            title = manga['attributes']['title'].get('en', 'No Title Available')
            print(title)

