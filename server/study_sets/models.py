from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class StudyFolder(models.Model):
    title = models.CharField(max_length=100)
    public = models.BooleanField(default=False, blank=True)
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_study_folders')

    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='study_folder_editors', blank=True)
    viewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='study_folder_viewers', blank=True)

    def save(self, *args, **kwargs) -> None:
        if self.pk:
            if self.editors.filter(pk=self.owner.pk).exists():
                raise ValidationError({'editors': 'Group owner is in the teacher field.'})
            
            if self.viewers.filter(pk=self.owner.pk).exists():
                raise ValidationError({'viewers': 'Group owner is in the student field.'})
            
            if self.editors.filter(pk__in=self.viewers.all()).exists():
                raise ValidationError('A user is in both editor and viewer fields.')
            
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

            if self.editors.filter(pk=self.owner.pk).exists():
                self.delete()
                raise ValidationError({'editors': 'Group owner is in the editor field.'})
            
            if self.viewers.filter(pk=self.owner.pk).exists():
                self.delete()
                raise ValidationError({'viewers': 'Group owner is in the viewer field.'})
            
            if self.editors.filter(pk__in=self.viewers.all()).exists():
                self.delete()
                raise ValidationError('A user is in both editor and viewer fields.')
            
    def __str__(self) -> str:
        return self.title


class StudySet(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1200, null=True, blank=True)
    public = models.BooleanField(default=False, blank=True)
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_study_sets')

    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='study_set_editors', blank=True)
    viewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='study_set_viewers', blank=True)

    study_set_folder = models.ForeignKey(StudyFolder, on_delete=models.CASCADE, related_name='study_sets', blank=True, null=True)

    def save(self, *args, **kwargs) -> None:
        if self.pk:
            if self.editors.filter(pk=self.owner.pk).exists():
                raise ValidationError({'editors': 'Study set owner is in the teacher field.'})
            
            if self.viewers.filter(pk=self.owner.pk).exists():
                raise ValidationError({'viewers': 'Study set is in the student field.'})
            
            if self.editors.filter(pk__in=self.viewers.all()).exists():
                raise ValidationError('A user is in both editor and viewer fields.')
            
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

            if self.editors.filter(pk=self.owner.pk).exists():
                self.delete()
                raise ValidationError({'editors': 'Study set is in the editor field.'})
            
            if self.viewers.filter(pk=self.owner.pk).exists():
                self.delete()
                raise ValidationError({'viewers': 'Study set is in the viewer field.'})
            
            if self.editors.filter(pk__in=self.viewers.all()).exists():
                self.delete()
                raise ValidationError('A user is in both editor and viewer fields.')
            
    def __str__(self) -> str:
        return self.title

class StudyTerm(models.Model):
    study_set = models.ForeignKey(StudySet, on_delete=models.CASCADE, related_name='terms')

    term = models.CharField(max_length=200)
    definition = models.TextField(max_length=600)
    position = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.term