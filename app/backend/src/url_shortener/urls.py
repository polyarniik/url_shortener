from django.urls import path

from url_shortener import views

urlpatterns = [
    path("", views.main_page_view, name="home"),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("my", views.urls_list, name="urls"),
    path("delete/<int:pk>", views.delete_url, name="delete"),
    path("<str:short>/", views.redirect_view, name="short_url"),
]
