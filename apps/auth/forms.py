from django import forms
from django.conf import settings
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import int_to_base36
# from django.template import Context, loader
# from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from disposable_email_checker import DisposableEmailChecker

from apps.users.models import User


class SignUpForm(forms.ModelForm):

    error_messages = {
        'duplicate_email': ('There is already a user with this email.'),
        'bad_email_provider': _('Your email address provider is not valid. Please use a different email address provider.')
    }

    name = forms.CharField(min_length=4, max_length=64)
    email = forms.EmailField()
    password = forms.CharField(min_length=4, max_length=128,
                               widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'email', 'password')

    def name(self):
        name = self.cleaned_data['name']
        return name

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
#        if password1 != password2:
#            raise forms.ValidationError(
#                self.error_messages['password_mismatch'])
        return password

    def clean_email(self):
        email = self.data['email']

        if settings.DEBUG is False:
            email_checker = DisposableEmailChecker()
            if email_checker.is_disposable(email):
                raise forms.ValidationError(self.error_messages['bad_email_provider'])

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = True
        if commit:
            user.save()
        # Send confirmation link
        # t = loader.get_template('accounts/signup_email.html')
        # c = {
        #     'uid': int_to_base36(user.id),
        #     'token': default_token_generator.make_token(user),
        #     'BASE_URL': settings.BASE_URL,
        # }
        # send_mail('Confirmation link sent on Yougrups',
        #           t.render(Context(c)), '', [user.email])
        return user


class ChangePasswordForm(forms.Form):
    password = forms.CharField(min_length=4, max_length=128,
                               widget=forms.PasswordInput)
    new_password = forms.CharField(min_length=4, max_length=128,
                               widget=forms.PasswordInput)


class ResetPasswordForm(forms.Form):
    email = forms.EmailField()
