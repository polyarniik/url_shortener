from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render

from url_shortener.forms import LinkForm
from url_shortener.models import ShortLink


def main_page_view(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = ShortLink(
                link=form.cleaned_data['link']
            )
            link.save()
            return render(request, "url_shortener/main.html", {
                'form': form,
                'short_link': str('http://' + request.get_host()) + '/' + str(link.short_link)
            })

    if request.method == 'GET':
        form = LinkForm()
        return render(request, 'url_shortener/main.html', {
            'form': form,
        })


def redirect_view(request, short):
    short_link = ShortLink.objects.filter(short_link=short)
    if short_link is not None:
        return HttpResponseRedirect(short_link[0].link)
    else:
        return HttpResponseNotFound('<h1> Link not found <h1>')
