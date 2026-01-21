from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from unfold.admin import ModelAdmin, StackedInline
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import Course, Module, Subject

admin.site.unregister(User)
admin.site.unregister(Group)


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


class ModuleInline(StackedInline):
    model = Module
    extra = 1


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ["title", "subject", "created"]
    list_filter = ["created", "subject"]
    search_fields = ["title", "overview"]
    prepopulated_fields = {"slug": ["title"]}
    inlines = [ModuleInline]


@admin.register(Subject)
class SubjectAdmin(ModelAdmin):
    list_display = ["title", "slug"]
    prepopulated_fields = {"slug": ["title"]}

