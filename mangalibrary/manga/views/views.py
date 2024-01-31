from django.shortcuts import render
from manga.forms.forms import MangaSearchForm
from manga.mangadex.requests import MangaDexAPI

def home_view(request):
    return render(request, 'manga/home.html')

def manga_search_view(request):
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
            
            mangas_with_cover_art = []
            for manga in results['data']:
                # Skip if manga is not a dictionary
                if not isinstance(manga, dict):
                    continue

                cover_art_id = None
                for relationship in manga.get('relationships', []):
                    if isinstance(relationship, dict) and relationship.get('type') == 'cover_art':
                        cover_art_id = relationship.get('attributes').get('fileName')
                        break
                # Ensure manga can be modified (it should be a dict)
                if isinstance(manga, dict):
                    manga['cover_art_id'] = cover_art_id
                    mangas_with_cover_art.append(manga)
                
            context = {'mangas': mangas_with_cover_art}
            
            
            return render(request, 'manga/manga_search_results.html', {'results': results, 'context':context})
    else:
        form = MangaSearchForm()
    return render(request, 'manga/manga_search_form.html', {'form': form})

def manga_search_form(request):
    form = MangaSearchForm()
    return render(request, 'manga/manga_search_form.html', {'form': form})