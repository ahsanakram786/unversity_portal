from django.contrib import admin

from .models import Module, Course


class CourseInline(admin.TabularInline):
    model = Module.course_allowed.through
    extra = 1


class ModuleAdmin(admin.ModelAdmin):
    inlines = [CourseInline]


class ModuleAdmin(admin.ModelAdmin):
    inlines = [CourseInline]


class CourseAdmin(admin.ModelAdmin):
    exclude = ('modules',)  # Exclude modules field as it's managed by Module admin


admin.site.register(Module, ModuleAdmin)
admin.site.register(Course, CourseAdmin)
