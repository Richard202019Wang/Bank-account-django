from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse,  HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.template.response import TemplateResponse

from django.core.validators import validate_email


def register(request):
    if request.method == "GET":
        return TemplateResponse(request, 'accounts/register.html')
    elif request.method == "POST":
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        errors = ["", "", "", "", "", "", "", ""]
        if password1 != password2:
            errors[0] = "The two password fields didn't match"
        if 0 < len(password1) < 8:
            errors[1] = "This password is too short. It must contain at least 8 characters"
        if 0 < len(password2) < 8:
            errors[2] = "This password is too short. It must contain at least 8 characters"
        if password1 == "":
            errors[3] = "This field is required"
        if password2 == "":
            errors[4] = "This field is required"
        if username == "":
            errors[5] = "This field is required"

        try:
            validate_email(email)
        except ValidationError:
            errors[6] = "Enter a valid email address"

        if errors[0] == "" and errors[1] == "" and errors[2] == ""\
                and errors[3] == "" and errors[4] == "" and errors[5] == "":
            try:
                User.objects.create_user(username=username, password=password1,
                                         last_name=last_name, first_name=first_name, email=email)
            except IntegrityError:
                errors[7] = "A user with that username already exists"
        if errors[0] != "" or errors[1] != "" or errors[2] != "" or errors[3] != "" or errors[4] != ""\
                or errors[5] != "" or errors[7] != "":
            return TemplateResponse(request, 'accounts/register.html', {'errors': errors})

        return HttpResponseRedirect("/accounts/login/")
    else:
        return HttpResponseNotFound()


def user_login(request):
    if request.method == "GET":
        return TemplateResponse(request, 'accounts/login.html')
    elif request.method == "POST":
        errors = [""]
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if not User.objects.filter(username=username).exists():
            errors[0] = "Username or password is invalid"
            return TemplateResponse(request, 'accounts/login.html', {'errors': errors})
        else:
            current_user = authenticate(request, username=username, password=password)
            if current_user is None:
                errors[0] = "Username or password is invalid"
                return TemplateResponse(request, 'accounts/login.html', {'errors': errors})
            else:
                login(request, current_user)
                return HttpResponseRedirect("/accounts/profile/view/")
    else:
        return HttpResponseNotFound()


def user_logout(request):
    if request.method == "GET":
        logout(request)
        return HttpResponseRedirect("/accounts/login/")
    else:
        return HttpResponseNotFound()


def profile_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            users = request.user
            users_dict = {
                "id": users.id,
                "username": users.username,
                "email": users.email,
                "first_name": users.first_name,
                "last_name": users.last_name
            }
            return JsonResponse(users_dict)
        else:
            return HttpResponse('UNAUTHORIZED', status=401)
    else:
        return HttpResponseNotFound()


def profile_edit(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return TemplateResponse(request, 'accounts/profile_edit.html', {'first_name': request.user.first_name,
                                                                            'last_name': request.user.last_name,
                                                                            'email': request.user.email})
        else:
            return HttpResponse('UNAUTHORIZED', status=401)

    elif request.method == "POST":
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        errors = ["", "", "", ""]
        if password1 != password2:
            errors[0] = "The two password fields didn't match"
        if 0 < len(password1) < 8:
            errors[1] = "This password is too short. It must contain at least 8 characters"
        if 0 < len(password2) < 8:
            errors[2] = "This password is too short. It must contain at least 8 characters"
        try:
            validate_email(email)
        except ValidationError:
            errors[3] = "Enter a valid email address"
        if errors[0] != "" or errors[1] != "" or errors[2] != "":
            return TemplateResponse(request, 'accounts/profile_edit.html', {'errors': errors,
                                                                            'first_name': first_name,
                                                                            'last_name': last_name,
                                                                            'email': email
                                                                            })
        if len(password1) > 0:
            request.user.set_password(password1)
        request.user.email = email
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()
        login(request, request.user)
        return HttpResponseRedirect("/accounts/profile/view/")
    else:
        return HttpResponseNotFound()

