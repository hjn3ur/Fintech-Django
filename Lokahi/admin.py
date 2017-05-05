from django.contrib import admin
from .models import Investor, Message, Company, Person, Picture, Project, Report

# Register your models here.
admin.site.register(Person)
admin.site.register(Company)
admin.site.register(Investor)
admin.site.register(Message)
admin.site.register(Picture)
admin.site.register(Project)
admin.site.register(Report)
