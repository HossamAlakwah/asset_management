from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, blank=True, db_index=True)
    created_at = models.DateTimeField(default=timezone.now)
    choosable = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Branch"
        verbose_name_plural = "Branches"

    def save(self, *args, **kwargs):
        if self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
