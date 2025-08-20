from django.contrib import admin
from .models import Batch, Course, Semester, Section, Subject, Student, Attendance

# BATCH MODEL
class BatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'batch_year')
admin.site.register(Batch, BatchAdmin)

# COURSE MODEL
class CourseAdmin(admin.ModelAdmin):
    list_display = ('batch', 'course_id', 'course_name', 'course_duration', 'total_semesters')
    list_filter = ('batch',)
admin.site.register(Course, CourseAdmin)

# SEMESTER MODEL
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('course', 'semester_id', 'semester_num')
admin.site.register(Semester, SemesterAdmin)

# SECTION MODEL
class SectionAdmin(admin.ModelAdmin):
    list_display = ('course', 'semester', 'section_id', 'section_name')
admin.site.register(Section, SectionAdmin)

# SUBJECT MODEL
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('course', 'semester', 'subject_id', 'subject_name')
    search_fields = ('subject_name', 'subject_id')  

admin.site.register(Subject, SubjectAdmin)

# STUDENT MODEL
class StudentAdmin(admin.ModelAdmin):
    list_display = ('course', 'semester', 'section', 'student_id', 'student_name', 'student_roll', 'student_phone')
    search_fields = ('student_name', 'student_roll', 'student_id') 

admin.site.register(Student, StudentAdmin)

# ATTENDANCE MODEL
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'is_present')
    list_per_page = 50 

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'batch', 'course', 'semester', 'section', 'subject', 'student'
        )

admin.site.register(Attendance, AttendanceAdmin)