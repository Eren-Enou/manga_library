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
    
    included_tag_names = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Separate with ,'}))
    excluded_tag_names = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Separate with ,'}))
    order_rating = forms.ChoiceField(choices=[('desc', 'Descending'), ('asc', 'Ascending')], required=False, initial='desc')
    order_followedCount = forms.ChoiceField(choices=[('desc', 'Descending'), ('asc', 'Ascending')], required=False, initial='desc')
    publication_demographic = forms.MultipleChoiceField(choices=DEMOGRAPHIC_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    status = forms.MultipleChoiceField(choices=STATUS_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    content_rating = forms.MultipleChoiceField(choices=CONTENT_RATING_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    limit = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Number of results'}), min_value=1, max_value=100)