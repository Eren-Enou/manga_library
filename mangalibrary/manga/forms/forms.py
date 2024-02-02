from django import forms

class MangaSearchForm(forms.# In this code, `Form` is a class provided by Django that is used to
# define a form. It allows you to define fields and their properties, such
# as required or optional, choices, and widgets. The `Form` class provides
# methods to validate and process the form data. In this specific example,
# the `MangaSearchForm` class is a subclass of `Form` and defines various
# fields for searching manga, such as included and excluded tag names,
# order by rating or followed count, publication demographic, status,
# content rating, and limit.
Form):
    
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('hiatus', 'Hiatus'), 
        ('cancelled', 'Cancelled')
    ]
    DEMOGRAPHIC_CHOICES = [
        ('shounen', 'Shounen'),
        ('shoujo', 'Shoujo'), 
        ('seinen', 'Seinen'), 
        ('josei', 'Josei')

    ]
    CONTENT_RATING_CHOICES = [
        ('safe', 'Safe'),
        ('suggestive', 'Suggestive'), 
        ('erotica', 'Erotica'), 
        ('pornographic', 'Pornographic')
    ]
    SORT_CHOICES = [
        ('relevance_desc', 'Best Match'),  # Assuming relevance is the default sort option
        ('latestUploadedChapter_desc', 'Latest Upload'),
        ('latestUploadedChapter_asc', 'Oldest Upload'),
        ('title_asc', 'Title Ascending'),
        ('title_desc', 'Title Descending'),
        ('rating_desc', 'Highest Rating'),  # Assuming rating is the correct field name
        ('rating_asc', 'Lowest Rating'),
        ('followedCount_desc', 'Most Follows'),
        ('followedCount_asc', 'Fewest Follows'),
        ('createdAt_desc', 'Recently Added'),
        ('createdAt_asc', 'Oldest Added'),
        ('year_asc', 'Year Ascending'),
        ('year_desc', 'Year Descending'),
    ]

    
    included_tag_names = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Separate with ,'}))
    excluded_tag_names = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Separate with ,'}))
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, label="Sort by")
    publication_demographic = forms.MultipleChoiceField(choices=DEMOGRAPHIC_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    status = forms.MultipleChoiceField(choices=STATUS_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    content_rating = forms.MultipleChoiceField(choices=CONTENT_RATING_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    limit = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Number of results'}), min_value=1, max_value=100)
    title_query = forms.CharField(required=False, label="Title", widget=forms.TextInput(attrs={'placeholder': 'Search by title...'}))