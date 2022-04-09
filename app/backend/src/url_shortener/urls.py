from django.urls import path

from url_shortener.views import main_page_view, redirect_view

urlpatterns = [
    path('', main_page_view),
    path('<str:short>/', redirect_view)
]
