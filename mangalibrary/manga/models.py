from django.db import models

class Manga(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True, null=True)  # Optional
    genres = models.CharField(max_length=255)  # Consider a ManyToManyField for a more normalized approach
    status = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)  # Optional
    cover_image_url = models.URLField(blank=True, null=True)  # Optional

    def __str__(self):
        return self.title
    
class Chapter(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='chapters')
    number = models.FloatField()  # Using FloatField to accommodate chapters like "10.5"
    title = models.CharField(max_length=255, blank=True, null=True)  # Optional
    url = models.URLField()  # URL to read the chapter
    release_date = models.DateField()

    class Meta:
        ordering = ['number']  # Ensures chapters are ordered by their number by default

    def __str__(self):
        return f"{self.manga.title} - Chapter {self.number}"