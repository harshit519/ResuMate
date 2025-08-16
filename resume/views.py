from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import (
    ResumeForm,
    ExperienceFormSet,
    EducationFormSet,
    SkillFormSet,
    ProjectFormSet,
)
from .models import Resume


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'resume/landing.html')


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('resume_list')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('resume_list')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login')


@login_required
def resume_list(request: HttpRequest) -> HttpResponse:
    resumes = Resume.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'resume/resume_list.html', {'resumes': resumes})


@login_required
@require_http_methods(["GET", "POST"])
def resume_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()

            # Initialize empty formsets to add after creating the resume
            exp_fs = ExperienceFormSet(instance=resume, data=request.POST)
            edu_fs = EducationFormSet(instance=resume, data=request.POST)
            skill_fs = SkillFormSet(instance=resume, data=request.POST)
            proj_fs = ProjectFormSet(instance=resume, data=request.POST)

            if all([exp_fs.is_valid(), edu_fs.is_valid(), skill_fs.is_valid(), proj_fs.is_valid()]):
                exp_fs.save()
                edu_fs.save()
                skill_fs.save()
                proj_fs.save()
                return redirect('resume_detail', pk=resume.pk)
    else:
        form = ResumeForm()

    # Provide empty formsets on GET
    exp_fs = ExperienceFormSet()
    edu_fs = EducationFormSet()
    skill_fs = SkillFormSet()
    proj_fs = ProjectFormSet()
    return render(
        request,
        'resume/resume_form.html',
        {
            'form': form,
            'exp_fs': exp_fs,
            'edu_fs': edu_fs,
            'skill_fs': skill_fs,
            'proj_fs': proj_fs,
            'new': True,
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def resume_edit(request: HttpRequest, pk: int) -> HttpResponse:
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        exp_fs = ExperienceFormSet(request.POST, instance=resume)
        edu_fs = EducationFormSet(request.POST, instance=resume)
        skill_fs = SkillFormSet(request.POST, instance=resume)
        proj_fs = ProjectFormSet(request.POST, instance=resume)

        if all([form.is_valid(), exp_fs.is_valid(), edu_fs.is_valid(), skill_fs.is_valid(), proj_fs.is_valid()]):
            form.save()
            exp_fs.save()
            edu_fs.save()
            skill_fs.save()
            proj_fs.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = ResumeForm(instance=resume)
        exp_fs = ExperienceFormSet(instance=resume)
        edu_fs = EducationFormSet(instance=resume)
        skill_fs = SkillFormSet(instance=resume)
        proj_fs = ProjectFormSet(instance=resume)

    return render(
        request,
        'resume/resume_form.html',
        {
            'form': form,
            'exp_fs': exp_fs,
            'edu_fs': edu_fs,
            'skill_fs': skill_fs,
            'proj_fs': proj_fs,
            'new': False,
        },
    )


@login_required
def resume_detail(request: HttpRequest, pk: int) -> HttpResponse:
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    return render(request, 'resume/resume_detail.html', {'resume': resume})


@login_required
@require_http_methods(["POST"])
def resume_delete(request: HttpRequest, pk: int) -> HttpResponse:
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    resume.delete()
    return redirect('resume_list')


@login_required
def resume_print(request: HttpRequest, pk: int) -> HttpResponse:
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    # Render a printer-friendly/HTML-to-PDF-ready page
    return render(request, 'resume/pdf_resume.html', {'resume': resume})

