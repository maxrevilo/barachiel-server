# -*- coding: utf-8 -*-
import json
import random
import string

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseNotFound
from django.core.mail import send_mail
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.views.generic import View
from django.forms.util import ErrorList
from django.conf import settings

from apps.users.models import User
from apps.auth.signals import user_with_new_email
from forms import SignUpForm, ChangePasswordForm, ResetPasswordForm
from libs.helpers import PUT_dict


@never_cache
def login(request):
    if request.method == "POST":
        user = None
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Okay, security checks complete. Log the user in.
            user = form.get_user()
            auth_login(request, user)
        else:
            return HttpResponseForbidden(json.dumps(form.errors), mimetype='application/json')

        response = user.serialize(user)

        httpResponse = HttpResponse(json.dumps(response), mimetype='application/json')

        return httpResponse
    else:
        return HttpResponseNotAllowed(['POST'])


@never_cache
def logout(request):
    auth_logout(request)
    return HttpResponse('Ok')


@never_cache
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user_with_new_email.send(sender=signup, user=new_user, user_just_created=True)
            new_user = authenticate(username=request.POST['email'],
                                    password=request.POST['password'])
            auth_login(request, new_user)
            return HttpResponse(json.dumps(new_user.serialize(new_user)), mimetype='application/json')
        else:
            return HttpResponseBadRequest(json.dumps(form.errors), mimetype='application/json')
    else:
        return HttpResponseNotAllowed()


class ResetPasswordView(View):

    def post(self, request, *args, **kwargs):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email_address = request.POST['email']
            user = get_object_or_404(User, email=email_address)
            N = 8  # Logitud del password
            newPassword = ''.join(random.choice(string.ascii_uppercase +
                string.ascii_lowercase + string.digits) for x in range(N))
            user.set_password(newPassword)
            user.save()
            email = 'You have asked for a new password, since you forgot your old one. Please take note of the new one, and change it, as soon as possible, for one easier for you to remember.\n\nUser: %s\nE-Mail: %s\nPassword: %s\n\n--\nThe Waving team.' % (user.name, user.email, newPassword)
            send_mail(settings.EMAIL_SUBJECT_PREFIX + 'Password reset', email, settings.DEFAULT_FROM_EMAIL, [email_address])
            return HttpResponse()
        else:
            return HttpResponseBadRequest(json.dumps(form.errors), mimetype='application/json')

reset_password = ResetPasswordView.as_view()


class ChangePasswordView(View):

    def put(self, request, *args, **kwargs):
        request.PUT = PUT_dict(request, ['password', 'new_password'])
        user = request.user
        form = ChangePasswordForm(request.PUT)
        if form.is_valid():
            print "form is valid"
            password = request.PUT["password"]
            new_password = request.PUT["new_password"]

            if not user.check_password(password):
                errors = form._errors.setdefault("password", ErrorList())
                errors.append(u"The entered password is not correct.")
                return HttpResponseBadRequest(json.dumps(form.errors), mimetype='application/json')
            print "password is correct"
            if password == new_password:
                errors = form.NON_FIELD_ERRORS.setdefault("__all__", ErrorList())
                errors.append(u"The old password equals new password.")
                return HttpResponseBadRequest(json.dumps(form.errors), mimetype='application/json')
            print "password equals new password"

            user.set_password(new_password)
            user.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest(json.dumps(form.errors), mimetype='application/json')

change_password = ChangePasswordView.as_view()


class EmailConfirmView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            request.user.send_confirmation_reminder_mail()
            return HttpResponse()
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        # check if user needs confirmation
        user = request.user
        if user.email_is_confirmed:
            return HttpResponseNotAllowed()

        # Check if user is active
        if not user.is_active:
            return HttpResponseNotFound()

        code = request.POST.get('confirmation-code', None)
        # Check for a well formed request
        if code is None:
            return HttpResponseBadRequest()
        # Check for well formed confirmation code
        from apps.auth.models import Confirmation
        import operator

        VALID_CHARS = Confirmation.VALID_CHARS

        if not reduce(operator.and_, map(lambda x: x in VALID_CHARS, code), True) or len(code) != 8:
            return HttpResponseBadRequest()

        status = user.confirm_email(code)

        responses = {
            200: HttpResponse,
            403: HttpResponseForbidden,
            404: HttpResponseNotFound,
            405: HttpResponseNotAllowed
        }

        param = ''
        if status == 405:
            param = ['GET', 'POST']

        return responses[status](param)

email_confirm = EmailConfirmView.as_view()
