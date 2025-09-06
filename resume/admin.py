from django.contrib import admin
from .models import Resume, Experience, Education, Skill, Project


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 2


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("title", "full_name", "email", "updated_at")
    search_fields = ("title", "full_name", "email")
    inlines = [ExperienceInline, EducationInline, SkillInline, ProjectInline]


admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(Project)
