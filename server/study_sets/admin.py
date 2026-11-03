from django.contrib import admin
from .models import StudyFolder, StudySet, StudyTerm

# Register your models here.
admin.site.register(StudyFolder)
admin.site.register(StudySet)
admin.site.register(StudyTerm)