from django import forms

class MangaSearchForm(forms.Form):
    
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
    order_rating = forms.ChoiceField(choices=[('desc', 'Descending'), ('asc', 'Ascending')], required=False)
    order_followedCount = forms.ChoiceField(choices=[('desc', 'Descending'), ('asc', 'Ascending')], required=False)
    publication_demographic = forms.MultipleChoiceField(choices=DEMOGRAPHIC_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    status = forms.MultipleChoiceField(choices=STATUS_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    content_rating = forms.MultipleChoiceField(choices=CONTENT_RATING_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    limit = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Number of results'}), min_value=1, max_value=100)