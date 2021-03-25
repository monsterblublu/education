from django.db import models
from django.conf import settings
from django.urls import reverse


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=60)
    slug = models.SlugField()
    author = models.ForeignKey("Creator", settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    to = models.ManyToManyField()
    created_at = models.DateTimeField()
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = False
    
    def get_absolute_url(self):
        return reverse('assignment:detail' kwargs={'pk':self.pk,
                                                'slug':self.slug})

class 