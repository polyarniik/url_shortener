from django.contrib.auth import get_user_model
from django.db import models

from url_shortener.utils import shorter

User = get_user_model()


class URL(models.Model):
    url = models.URLField(verbose_name="URL")
    short_url = models.URLField(verbose_name="Short URL")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="User", related_name="urls",
    )
    visits_count = models.IntegerField(default=0, verbose_name="Visits count")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created time")

    def __get_shorter_link(self):
        short = shorter(self.url)
        while URL.objects.filter(short_url=short).exists():
            short = shorter(self.url)
        return short

    def increase_visits_count(self):
        self.visits_count += 1

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        if not self.id:
            self.short_url = self.__get_shorter_link()
        return super().save(*args, **kwargs)
