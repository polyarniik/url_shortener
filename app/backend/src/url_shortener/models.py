from django.db import models

from url_shortener.utils import shorter


class ShortLink(models.Model):
    link = models.URLField(verbose_name='link')
    short_link = models.URLField(verbose_name='short_link')

    def get_shorter_link(self):
        short = shorter(self.link)
        while ShortLink.objects.filter(short_link=short).exists():
            short = shorter(self.link)

        return short

    def __str__(self):
        return self.link

    def save(self, *args, **kwargs):
        if not self.id:
            self.short_link = self.get_shorter_link()
        return super().save(*args, **kwargs)
