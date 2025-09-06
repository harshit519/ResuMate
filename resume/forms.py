from django import forms
from django.forms import inlineformset_factory
from .models import Resume, Experience, Education, Skill, Project


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'title', 'full_name', 'email', 'phone', 'location', 'summary', 'photo'
        ]
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = [
            'job_title', 'company', 'location', 'start_date', 'end_date', 'is_current', 'description'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'start_year', 'end_year', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'level', 'category']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'role', 'description', 'link']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


ExperienceFormSet = inlineformset_factory(
    Resume, Experience, form=ExperienceForm, fields=ExperienceForm.Meta.fields, extra=1, can_delete=True
)

EducationFormSet = inlineformset_factory(
    Resume, Education, form=EducationForm, fields=EducationForm.Meta.fields, extra=1, can_delete=True
)

SkillFormSet = inlineformset_factory(
    Resume, Skill, form=SkillForm, fields=SkillForm.Meta.fields, extra=2, can_delete=True
)

ProjectFormSet = inlineformset_factory(
    Resume, Project, form=ProjectForm, fields=ProjectForm.Meta.fields, extra=1, can_delete=True
)


