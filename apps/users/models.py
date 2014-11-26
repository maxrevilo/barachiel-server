#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from django import forms
from django.db import models
from django.conf import settings
from django.template import loader
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager

from apps.auth.models import Confirmation


class UserManager(BaseUserManager):

    def create_user(self, email, name, password=None):
        # validación:
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have a name')
        try:
            User.objects.get(email=email)
            raise forms.ValidationError(self.error_messages['duplicate_email'])
        except User.DoesNotExist:
            pass

        user = User()

        user.email_wtc = BaseUserManager.normalize_email(email),
        user.name = name
        if password is None:
            user.set_password(self.make_random_password())
        else:
            user.set_password(password)

        user.is_superuser = False
        user.save(using=self._db)

        #Send confirmation link
        #t = loader.get_template('accounts/signup_email.html')
        #c = {
        #    'uid': int_to_base36(user.id),
        #    'token': default_token_generator.make_token(user),
        #    'BASE_URL': settings.BASE_URL,
        #}
        #send_mail('Confirmation link sent on Yougrups',
        #          t.render(Context(c)), '', [user.email_wtc])

    def create_superuser(self, email, name, password):
        raise "Not implemented"


class User(AbstractBaseUser):

    SEX_UNKNOWN = 'U'
    SEX_FEMALE  = 'F'
    SEX_MALE    = 'M'
    SEXS = (
        (SEX_UNKNOWN, 'Unknown'),
        (SEX_FEMALE , 'Female'),
        (SEX_MALE   , 'Male'),
    )

    R_INTEREST_UNKNOWN = 'U'
    R_INTEREST_FEMALE  = 'F'
    R_INTEREST_MALE    = 'M'
    R_INTEREST_BOTH    = 'B'
    R_INTEREST_FRIENDS = 'R'
    R_INTERESTS = (
        (R_INTEREST_UNKNOWN, 'Unknown'),
        (R_INTEREST_FEMALE , 'Female'),
        (R_INTEREST_MALE   , 'Male'),
        (R_INTEREST_BOTH   , 'Both'),
        (R_INTEREST_FRIENDS, 'Friends'),
    )

    SSTATUS_DONTSAY        = 'U'
    SSTATUS_SINGLE         = 'S'
    SSTATUS_MARRIED        = 'M'
    SSTATUS_INRELATIONSHIP = 'R'
    SSTATUS = (
        (SSTATUS_DONTSAY,        'DontSay'),
        (SSTATUS_SINGLE,         'Single'),
        (SSTATUS_MARRIED,        'Married'),
        (SSTATUS_INRELATIONSHIP, 'InRelationShip'),
    )

    WHO_USER_NEAR   = 'E'
    WHO_USER_LIKED  = 'L'
    WHO_USER_NOBODY = 'N'
    WHO_USER = (
        (WHO_USER_NEAR,   'Near people'),
        (WHO_USER_LIKED,  'Only who I Waved'),
        (WHO_USER_NOBODY, 'Nobody'),
    )

    name       = models.CharField(max_length=128)
    email      = models.EmailField(unique=True)
    tel        = models.CharField(max_length=32, blank=True, default="")
    picture    = models.ForeignKey('multimedia.Media', blank=True, null=True, related_name='user', on_delete=models.SET_NULL)
    sex        = models.CharField(choices=SEXS, max_length=1, default=SEX_UNKNOWN)
    r_interest = models.CharField(choices=R_INTERESTS, max_length=1, default=R_INTEREST_UNKNOWN)
    bio        = models.TextField(blank=True, default="")
    birthday   = models.DateField(null=True, blank=True)
    age        = models.IntegerField(default=0)
    sentimental_status = models.CharField(choices=SSTATUS, max_length=1, default=SSTATUS_DONTSAY)
    #Geolocalization
    geo_lat    = models.FloatField(default=0)
    geo_lon    = models.FloatField(default=0)
    geo_time   = models.DateTimeField(auto_now_add=True)
    #Relations:
    likes      = models.ManyToManyField('self', through='likes.Like', symmetrical=False, related_name='liked')
    #Calculated
    likes_number = models.IntegerField(default=0)
    liked_number = models.IntegerField(default=0)

    ##### Privacy #####
    how_can_see_name    = models.CharField(choices=WHO_USER, max_length=1, default=WHO_USER_NEAR)
    how_can_see_bio     = models.CharField(choices=WHO_USER, max_length=1, default=WHO_USER_NEAR)
    how_can_see_picture = models.CharField(choices=WHO_USER, max_length=1, default=WHO_USER_NEAR)
    how_can_see_age     = models.CharField(choices=WHO_USER, max_length=1, default=WHO_USER_NEAR)
    how_can_see_ss      = models.CharField(choices=WHO_USER, max_length=1, default=WHO_USER_NEAR)
    how_can_see_tel     = models.CharField(choices=WHO_USER, max_length=1, default=WHO_USER_LIKED)
    how_can_see_email   = models.CharField(choices=WHO_USER, max_length=1, default=WHO_USER_LIKED)
    ##### Privacy #####

    # Settings
    off_radar = models.BooleanField(default=False)

    #Server data
    _updated_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    _created_at = models.DateTimeField(auto_now_add=True)
    #Email waiting to confirm
    _email_wtc = models.EmailField(unique=True, null=True, blank=True, default=None)

    def like(self, user):
        self.likes.add(user)
        self.likes_number = self.likes.count()
        self.save()

        user.liked_number = self.likes.count()
        user.save()

    def settings(self):
        return {
            'off_radar': self.off_radar
        }

    ##### Privacy #####
    def privacy(self):
        return {
            'name':     self.how_can_see_name,
            'picture':  self.how_can_see_picture,
            'age':      self.how_can_see_age,
            'ss':       self.how_can_see_ss,
            'bio':      self.how_can_see_bio,
            'tel':      self.how_can_see_tel,
            'email':    self.how_can_see_email,
        }

    def _trust_lvl(self, user):
        if user == self:
            #The highest level
            return 0

        if self.likes.filter(pk=user.pk, likes_to__anonymous=False).exists():
            return 10

        #The lowest level
        return 100

    def _can_see(self, users_trust_lvl, privacy_lvl):
        if privacy_lvl == self.WHO_USER_NEAR:
            return True

        if privacy_lvl == self.WHO_USER_LIKED:
            return users_trust_lvl <= 10

        if privacy_lvl == self.WHO_USER_NOBODY:
            return users_trust_lvl == 0
    ##### Privacy #####

    def preview(self, user):
        prev = {
            'id':           self.id,
            'sex':          self.sex,
            'liked_number': self.liked_number,
        }

        user_lvl = self._trust_lvl(user)

        if self._can_see(user_lvl, self.how_can_see_name):
            prev['name'] = self.name

        if self._can_see(user_lvl, self.how_can_see_picture):
            prev['picture'] = self.picture.preview(user) if self.picture is not None else None

        if self._can_see(user_lvl, self.how_can_see_ss):
            prev['sentimental_status'] = self.sentimental_status

        return prev

    def preview_anonym(self, user):
        prev = {
            'r_interest':   self.r_interest,
            'sex':          self.sex,
        }

        user_lvl = self._trust_lvl(user)

        if(self._can_see(user_lvl, self.how_can_see_ss)):
            prev['sentimental_status'] = self.sentimental_status

        return prev

    def serialize(self, user):
        if user is None:
            user = self

        user_lvl = self._trust_lvl(user)

        result = {
            'r_interest': self.r_interest,
        }

        if self._can_see(user_lvl, self.how_can_see_tel):
            result['tel'] = self.tel

        if self._can_see(user_lvl, self.how_can_see_email):
            result['email'] = self.email

        if self._can_see(user_lvl, self.how_can_see_bio):
            result['bio'] = self.bio

        if self._can_see(user_lvl, self.how_can_see_age):
            result['birthday'] = self.birthday.isoformat() if self.birthday is not None else None
            result['age'] = self.age

        if self._can_see(user_lvl, self.WHO_USER_NOBODY):
            result = dict(result, **{
                'email_wtc':    self._email_wtc,
                'likes':        map(lambda l: l.preview(user), self.likes_from.all()[:100]),
                'liked':        map(lambda l: l.preview(user), self.likes_to.all()[:100]),
                'likes_number': self.likes_number,
                'settings':     self.settings(),
                'privacy':      self.privacy(),

                '_updated_at': self._updated_at.isoformat(),
            })

        return dict(self.preview(user), **result)

    def __unicode__(self):
        return self.name

    #Some stuff added so django-allauth can work properly:
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password']
    # admin
    is_active = models.BooleanField(default=True)
    is_admin  = models.BooleanField(default=False)
    objects   = UserManager()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def is_anonymous(self):
        """
        Always returns False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return self.name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            self.save()
        return check_password(raw_password, self.password, setter)
    # End od django-allauth stuff

    # Emailing and email confirmation:

    @property
    def email_is_confirmed(self):
        try:
            Confirmation.objects.get(user=self, confirmation_type='E')
            return False
        except Confirmation.DoesNotExist:
            return self._email_wtc is None

    @property
    def email_confirmation_token(self):
        conf = Confirmation.objects.get(user=self, confirmation_type='E')
        return conf.token

    @property
    def email_confirmation_created_at(self):
        conf = Confirmation.objects.get(user=self, confirmation_type='E')
        return conf.created_at

    def confirm_email(self, token):
        if not self.email_is_confirmed:
            try:
                conf = Confirmation.objects.get(user=self)
            except Confirmation.DoesNotExist:
                return 404
            if conf.token != token:
                return 403
            if self.id != conf.user.id:
                return 403
            if self._email_wtc != conf.email:
                return 403
            # confirmation ok
            conf.delete()
            self._confirm_email()
            return 200
        else:
            return 405

    def _confirm_email(self):
        if not self.email_is_confirmed:
            self.email = self._email_wtc
            self._email_wtc = None
            self.save()

    def generate_email_confirmation(self):
        if not self.email_is_confirmed:
            from apps.auth.models import Confirmation
            import random

            VALID_CHARS = Confirmation.VALID_CHARS

            conf = Confirmation()
            conf.user = self
            conf.confirmation_type = Confirmation.EMAIL
            conf.email = self._email_wtc

            exists = True
            while exists:
                token = ''.join(random.choice(VALID_CHARS) for x in range(8))
                try:
                    Confirmation.objects.get(token=token)
                except Confirmation.DoesNotExist:
                    exists = not exists
                    conf.token = token
                    conf.save()

    def send_confirmation_mail(self, user_just_created, template='', subject=''):
        if not self.email_is_confirmed:
            if template == '':
                if user_just_created:
                    template = 'auth/email_confirmation.html'
                else:
                    template = 'auth/new_email_confirmation.html'  # cambiar
            if subject == '':
                subject += settings.EMAIL_SUBJECT_PREFIX
                if user_just_created:
                    subject += ' Thank you for joining us!'
                subject += ' Please, confirm your E-Mail address'

            grace_time = (self.email_confirmation_created_at + timedelta(days=settings.ACCOUNT_GRACE_TIME)) - datetime.now()
            context = {
                'BASE_URL':     settings.BASE_URL,
                'user':         self,
                'grace_time':   grace_time.days,
                'token':        self.email_confirmation_token,
                'emailAddress':  self._email_wtc
            }
            self._send_mail_from_template(subject, template, context)

    def send_confirmation_reminder_mail(self):
        subject = settings.EMAIL_SUBJECT_PREFIX + 'Email confirmation reminder'
        self.send_confirmation_mail(user_just_created=False, subject=subject)

    def _set_mandrill_options_on_email(self, message):
        message.inline_css = True
        return message

    def _send_multi_mail(self, subject, primary_content, alternatives, from_email='', html=True):

        if not self.email_is_confirmed:
            emailAddress = self._email_wtc
        else:
            emailAddress = self.email

        if from_email == '':
            from_email = settings.DEFAULT_FROM_EMAIL
        email = EmailMultiAlternatives(subject, primary_content, from_email, [emailAddress])
        if html:
            email.content_subtype = "html"
        for alt in alternatives:
            email.attach_alternative(alt[0], alt[1])

        email = self._set_mandrill_options_on_email(email)

        email.send()

    def _send_mail(self, subject, content, from_email='', html=True):
        if self.email_is_confirmed:
            emailAddress = self.email
        else:
            emailAddress = self._email_wtc

        msg = EmailMessage(subject, content, from_email, [emailAddress])
        if html:
            msg.content_subtype = "html"  # Main content is now text/html

        msg = self._set_mandrill_options_on_email(msg)

        msg.send()

    def _send_mail_from_template(self, subject, template_path, context={}, multialternatives=True):
        file_path = template_path.split('.')
        file_name, file_ext = ".".join(file_path[len(file_path)-1]), file_path[len(file_path)-1:]
        primary_is_html = True
        alt_ext = 'txt'
        if file_ext == 'txt':
            alt_ext = 'html'
            primary_is_html = False
        primary_content = loader.render_to_string(template_path, context)
        if multialternatives:
            try:
                alt_content = loader.render_to_string(file_name+"."+alt_ext, context)
            except Exception:
                multialternatives = False
        if multialternatives:
            if not primary_is_html:
                tmp = primary_content
                primary_content = alt_content
                alt_content = tmp
            alts = [(alt_content, "text/plain")]
            self._send_multi_mail(subject, primary_content, alts)
        else:
            self._send_mail(subject, primary_content, html=primary_is_html)

    # End of Emailing and email confirmation
