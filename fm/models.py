from django.db import models
from django.utils.text import slugify


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug


class Data(models.Model):
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    path = models.TextField(blank=True)
    name = models.TextField(blank=True)
    type = models.TextField(blank=True)
    size = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.path)
        super().save(*args, **kwargs)

    #class Meta:
    #    ordering = ['name']

    def __str__(self):
        return self.name



