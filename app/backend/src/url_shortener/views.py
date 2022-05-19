from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404

from url_shortener.forms import LinkForm
from url_shortener.models import URL


def register_request(request):
    """
    Регистрация пользователя
    :param request:
    :return:
    """
    if request.method == "POST":
        """
        Обработка формы
        """
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "Registration successful.",
            )
            return redirect("main:home")
        messages.error(
            request,
            "Unsuccessful registration. Invalid information.",
        )
    if request.user.is_authenticated:
        """
        Если пользователь авторизован, то он перенаправляется на домашнюю страницу
        """
        redirect("main:home")
    form = UserCreationForm()
    return render(
        request=request,
        template_name="url_shortener/sign_up.html",
        context={"register_form": form},
    )


def login_request(request):
    """
    Авторизация пользователя
    :param request:
    :return:
    """
    if request.method == "POST":
        """
        Обработка формы
        """
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    elif request.user.is_authenticated:
        """
        Если пользователь авторизован, то он перенаправляется на домашнюю страницу
        """
        redirect("main:home")
    else:
        form = AuthenticationForm()
        return render(
            request=request,
            template_name="url_shortener/sign_in.html",
            context={"login_form": form},
        )


def logout_request(request):
    """
    Выход пользователя из своего аккаунта
    :param request:
    :return:
    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main:home")


@login_required()
def main_page_view(request):
    """
    Страница с формой для укорачивания ссылки
    :param request:
    :return:
    """
    if request.method == "POST":
        """
        Обработка формы
        """
        form = LinkForm(request.POST)
        data = {}
        if form.is_valid():
            url = URL(
                url=form.cleaned_data["url"],
                user=request.user,
            )

            url.save()
            request.session["last_url"] = url.short_url
        return redirect("main:home")

    if request.method == "GET":
        """
        Рендеринг страницы с формой
        """
        form = LinkForm()
        urls = request.user.urls.all()
        return render(
            request,
            "url_shortener/main.html",
            {
                "form": form,
                "urls": urls,
            },
        )


def redirect_view(request, short):
    """
    Перенаправление пользователя на ссылку, которая была укорочена
    :param request:
    :param short:
    :return:
    """
    short_link = get_object_or_404(URL, short_url=short)
    short_link.increase_visits_count()
    short_link.save()
    return HttpResponseRedirect(short_link.url)


def delete_link(request):
    if request.method == "POST":
        ...
        # todo delete
        # request.POST
    else:
        redirect("main:home")
