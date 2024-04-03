from django.contrib import admin
from .models import  TripModel, NoteModel

admin.site.register(TripModel)
admin.site.register(NoteModel)