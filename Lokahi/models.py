from django.db import models
import datetime
from django.contrib.auth.models import Group


# models
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Investor(models.Model):
    username = models.CharField(max_length=30, default="")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=30, default="")
    banned = models.BooleanField(default=False)

    def __str__(self):
        return self.username + " " + self.first_name


class Company(models.Model):
    company_time = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now)
    company_update = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now)
    company_name = models.CharField(max_length=50)
    company_username = models.CharField(max_length=30, default="")
    company_password = models.CharField(max_length=30, default="")
    company_ceo = models.CharField(max_length=50, default="")
    company_email = models.EmailField(max_length=254, default="")
    company_state = models.CharField(max_length=20, default="")
    company_country = models.CharField(max_length=20, default="")
    company_phone = models.CharField(max_length=20, default="")
    company_sector = models.CharField(max_length=50, default="")
    company_industry = models.CharField(max_length=50, default="")
    company_project = models.TextField(max_length=1000, default="")
    banned = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name


class Message(models.Model):
    message_timestamp = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now)
    receiver = models.CharField(max_length=30, default="")
    sender = models.CharField(max_length=30, default="")
    message = models.CharField(max_length=1000, default="", null=True)
    encrypted_message = models.CharField(max_length=5000, null=True)
    encrypted = models.NullBooleanField(default=False)
    RSA_key = models.CharField(max_length=1000, default="", null=True, blank=True)
    hash_id = models.CharField(max_length=25, default="", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.message


# Create your models here.
class Picture(models.Model):
    files_id = models.CharField(max_length=50, default="")
    picfile = models.FileField(upload_to='pictures')
    timestamp = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now)
    owner = models.CharField(max_length=50, default="")
    investor = models.CharField(max_length=50, default="")
    encrypted = models.NullBooleanField(default=False)


class Project(models.Model):
    project_id = models.CharField(max_length=50, default="")
    timestamp = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now)
    owner = models.CharField(max_length=50, default="")
    project = models.CharField(max_length=50, default="")


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    public = models.CharField(max_length=50, default="")
    private = models.CharField(max_length=50, default="")
    company_time = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now)
    company_update = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now)
    company_name = models.CharField(max_length=50, default="")
    company_ceo = models.CharField(max_length=50, default="")
    company_email = models.EmailField(max_length=254, default="")
    company_phone = models.CharField(max_length=20, default="")
    company_state = models.CharField(max_length=20, default="")
    company_country = models.CharField(max_length=20, default="")
    company_sector = models.CharField(max_length=50, default="")
    company_industry = models.CharField(max_length=50, default="")
    company_project = models.TextField(max_length=1000, default="")
    company_file = models.TextField(max_length=1000, null=True)
    company_groups = models.CharField(max_length=1000, default='')


from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())