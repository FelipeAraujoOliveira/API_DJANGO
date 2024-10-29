from django.contrib import admin
from .models import User, Course, Area, Organization, Event

# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Area)
admin.site.register(Organization)
admin.site.register(Event)