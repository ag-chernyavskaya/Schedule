from django.contrib import admin
from .models import Course, Comment, Lesson, ClassroomAvailability


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["course_name", "course_type", "teacher", "location", "start_date", "start_time",
                    "start_day_of_week", "days_of_week", "number_of_lessons", ]
    ordering = ["-id"]
    search_fields = ["course_name"]
    list_filter = ["course_type", "teacher"]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["date", "start_time", "number", "course", "topic",
                    "description", "for_time_slot", "is_start_day", "is_end_day", "is_transit_day_1",
                    "is_transit_day_2"]
    ordering = ["number"]
    search_fields = ["topic"]
    list_filter = ["course__course_name", "teacher", "date", "start_time", 'for_time_slot']
    filter_horizontal = ['comment']


admin.site.register(Comment)


@admin.register(ClassroomAvailability)
class ClassroomAvailabilityAdmin(admin.ModelAdmin):
    list_display = ["date", "classroom", "start_time", "is_free"]
    ordering = ["date"]
    search_fields = ["date"]
    list_filter = ["date", "classroom", "start_time", "is_free"]