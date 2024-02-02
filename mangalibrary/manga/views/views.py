from django.shortcuts import render
from django.core.paginator import Paginator

from manga.forms.forms import MangaSearchForm
from manga.mangadex.requests import MangaDexAPI

def home_view(request):
    return render(request, 'manga/home.html')

def manga_search_view(request):
    if request.method == 'POST':
        form = MangaSearchForm(request.POST)
        if form.is_valid():
            manga_dex_api = MangaDexAPI()
            title_query = form.cleaned_data.get('title_query')
            included_tags = form.cleaned_data.get('included_tag_names').split(',')
            excluded_tags = form.cleaned_data.get('excluded_tag_names').split(',')
            # print(included_tags)
            # print(excluded_tags)
            # This assumes that 'sort_by' is the name of your field in the form
            # and the value is a string like 'title_descending'
            sort_by = form.cleaned_data.get('sort_by')
            
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
                title=title_query,
                limit=limit,
                included_tag_names=included_tags,
                excluded_tag_names=excluded_tags,
                sort_by=sort_by,
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
            
            # chapters = manga_dex_api.start_reading()
            
            return render(request, 'manga/manga_search_results.html', {'results': results, 'context':context})
    else:
        form = MangaSearchForm()
    return render(request, 'manga/manga_search_form.html', {'form': form})

def manga_search_form(request):
    form = MangaSearchForm()
    return render(request, 'manga/manga_search_form.html', {'form': form})

def start_reading_view(request, manga_id):
    manga_dex_api = MangaDexAPI()
    page_urls = manga_dex_api.start_reading(manga_id)
    
    if not page_urls:
        # Handle the case where no chapters/pages are found
        return render(request, 'manga/no_chapters_found.html')
    
    # Render a template showing the manga's pages or redirect to a dedicated reader view
    return render(request, 'manga/manga_reader.html', {'page_urls': page_urls})