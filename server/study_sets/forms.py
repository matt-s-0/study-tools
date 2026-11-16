from django import forms
from .models import StudyFolder, StudySet, StudyTerm
from django.contrib.auth import get_user_model

User = get_user_model()

class study_folder_form(forms.ModelForm):

    editors = forms.CharField(required=False, widget=forms.TextInput())
    viewers = forms.CharField(required=False, widget=forms.TextInput())

    class Meta:
        model = StudyFolder
        # auto set owner in views!!!!!!!!
        fields = ['title', 'public', 'editors', 'viewers']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):

        cleaned_data = super().clean()

        editor_emails = [e.strip().lower() for e in cleaned_data.get('editors', '').split(',') if e.strip()]
        viewer_Emails = [e.strip().lower() for e in cleaned_data.get('viewers', '').split(',') if e.strip()]

        overlapping_emails = set(editor_emails).intersection(set(viewer_Emails))
        if overlapping_emails:
            self.add_error('editors', 'A user cannot be in both the editor and viewer fields.')

        owner = self.user or (self.instance.owner if (self.instance and hasattr(self.instance, 'owner')) else None)

        if owner and getattr(owner, 'email', None):
            owner_email = owner.email.strip().lower()
            
            if owner_email in editor_emails:
                self.add_error('editors', 'The folder owner cannot be added as an editor.')
                
            if owner_email in viewer_Emails:
                self.add_error('viewers', 'The folder owner cannot be added as a viewer.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()

        editor_emails = [e.strip() for e in self.cleaned_data.get('editors', '').split(',') if e.strip()]
        viewer_Emails = [e.strip() for e in self.cleaned_data.get('viewers', '').split(',') if e.strip()]

        if commit:
            instance.editors.set(User.objects.filter(email__in=editor_emails))
            instance.viewers.set(User.objects.filter(email__in=viewer_Emails))
            self.save_m2m = lambda: None
        else:
            def save_m2m_custom():
                instance.editors.set(User.objects.filter(email__in=editor_emails))
                instance.viewers.set(User.objects.filter(email__in=viewer_Emails))
            self.save_m2m = save_m2m_custom

        return instance
    
class study_set_form(forms.ModelForm):
    editors = forms.CharField(required=False, widget=forms.TextInput())
    viewers = forms.CharField(required=False, widget=forms.TextInput())

    class Meta:
        model = StudySet
        # auto set owner in views!!!!!!!!
        fields = ['title', 'description', 'public', 'editors', 'viewers']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):

        cleaned_data = super().clean()

        editor_emails = [e.strip().lower() for e in cleaned_data.get('editors', '').split(',') if e.strip()]
        viewer_Emails = [e.strip().lower() for e in cleaned_data.get('viewers', '').split(',') if e.strip()]

        overlapping_emails = set(editor_emails).intersection(set(viewer_Emails))
        if overlapping_emails:
            self.add_error('editors', 'A user cannot be in both the editor and viewer fields.')

        owner = self.user or (self.instance.owner if (self.instance and hasattr(self.instance, 'owner')) else None)

        if owner and getattr(owner, 'email', None):
            owner_email = owner.email.strip().lower()
            
            if owner_email in editor_emails:
                self.add_error('editors', 'The set owner cannot be added as an editor.')
                
            if owner_email in viewer_Emails:
                self.add_error('viewers', 'The set owner cannot be added as a viewer.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()

        editor_emails = [e.strip() for e in self.cleaned_data.get('editors', '').split(',') if e.strip()]
        viewer_Emails = [e.strip() for e in self.cleaned_data.get('viewers', '').split(',') if e.strip()]

        if commit:
            instance.editors.set(User.objects.filter(email__in=editor_emails))
            instance.viewers.set(User.objects.filter(email__in=viewer_Emails))
            self.save_m2m = lambda: None
        else:
            def save_m2m_custom():
                instance.editors.set(User.objects.filter(email__in=editor_emails))
                instance.viewers.set(User.objects.filter(email__in=viewer_Emails))
            self.save_m2m = save_m2m_custom

        return instance

class study_term_form(forms.ModelForm):
    class Meta:
        model = StudyTerm
        fields = ['term', 'definition', 'position', 'study_set']