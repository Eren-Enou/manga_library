from django.shortcuts import render
from manga.forms.forms import MangaSearchForm
from manga.mangadex.requests import MangaDexAPI

def home_view(request):
    return render(request, 'manga/home.html')

def search_manga_view(request):
    if request.method == 'POST':
        form = MangaSearchForm(request.POST)
        if form.is_valid():
            manga_dex_api = MangaDexAPI()
            included_tags = form.cleaned_data.get('included_tag_names').split(',')
            excluded_tags = form.cleaned_data.get('excluded_tag_names').split(',')
            order = {
                "rating": form.cleaned_data.get('order_rating'),
                "followedCount": form.cleaned_data.get('order_followedCount'),
            }
            
            publication_demographic = form.cleaned_data.get('publication_demographic', [])
            status = form.cleaned_data.get('status', [])
            content_rating = form.cleaned_data.get('content_rating', [])
            
            limit = form.cleaned_data.get('limit')
            
            # Prepare filters for the API call
            filters = {}
            if publication_demographic:
                filters["publicationDemographic[]"] = publication_demographic
            if status:
                filters["status[]"] = status
            if content_rating:
                filters["contentRating[]"] = content_rating
                
            results = manga_dex_api.search_manga(
                limit=limit,
                included_tag_names=included_tags,
                excluded_tag_names=excluded_tags,
                order=order,
                **filters
            )
            return render(request, 'manga/manga_search_results.html', {'results': results})
    else:
        form = MangaSearchForm()
    return render(request, 'manga/manga_search_form.html', {'form': form})
