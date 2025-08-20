from login_app import views
from django.urls import path

urlpatterns = [
# HOME PAGE
  path('', views.index, name='index'),

# SIGNUP, LOGIN, LOGOUT & RESET_PASSWORD PAGE
  path('signup/', views.signup, name='signup'),
  path('login/', views.login_view, name='login'),
  path('logout/', views.logout_view, name='logout'),
  path('reset-password/', views.CustomPasswordResetView.as_view(), name='reset_password'),
  path('reset-password-done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
  path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
  path('reset-password-complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

# PROFILE (ADMIN & TEACHER), ADMIN ACCOUNT DELETION & CHANGE PASSWORD PAGE
  path('admin-profile/', views.admin_profile, name='admin_profile'),
  path('teacher-profile/', views.teacher_profile, name='teacher_profile'),
  path('delete_admin_account/', views.delete_admin_account, name='delete_admin_account'),
  path('change-password/', views.change_password, name='change_password'),

# ADMIN DASHBOARD PAGE
  path('dashboard/', views.dashboard, name='dashboard'),

# TEACHERS PAGE
  path('manage_teachers', views.manage_teachers, name='manage_teachers'), 
  path("update_teacher/<int:pk>", views.update_teacher, name="update_teacher"),
  path("delete_teacher/<int:pk>", views.delete_teacher, name="delete_teacher"),

# BATCHES PAGE
  path("manage_batches", views.manage_batches, name="manage_batches"),
  path("update_batch/<int:pk>", views.update_batch, name="update_batch"),
  path("delete_batch/<int:pk>", views.delete_batch, name="delete_batch"),
  
# COURSES PAGE
  path("manage_courses", views.manage_courses, name="manage_courses"),
  path("update_course/<str:course_id>", views.update_course, name="update_course"),
  path("delete_course/<str:course_id>", views.delete_course, name="delete_course"),
  
# SECTIONS PAGE
  path("manage_sections", views.manage_sections, name="manage_sections"),
  path("update_section/<str:section_id>", views.update_section, name="update_section"),
  path("delete_section/<str:section_id>", views.delete_section, name="delete_section"),
  
# SUBJECTS PAGE
  path("manage_subjects", views.manage_subjects, name="manage_subjects"),
  path("update_subject/<str:subject_id>", views.update_subject, name="update_subject"),
  path("delete_subject/<str:subject_id>", views.delete_subject, name="delete_subject"),
  
# STUDENTS PAGE
  path("manage_students", views.manage_students, name="manage_students"),
  path("update_student/<str:student_id>", views.update_student, name="update_student"),
  path("delete_student/<str:student_id>", views.delete_student, name="delete_student"),

# MANAGE ATTENDANCE RECORD PAGE (ADMIN)
  path("manage_attendance_record", views.manage_attendance_record, name="manage_attendance_record"),

# MARK ATTENDANCE PAGE
  path("mark_attendance", views.mark_attendance, name="mark_attendance"),

# ATTENDANCE RECORD PAGE (TEACHER)
  path("attendance_record", views.attendance_record, name="attendance_record"),

# ATTENDANCE ANALYTICS PAGE (ADMIN)
  path("manage_attendance_analytics", views.manage_attendance_analytics, name="manage_attendance_analytics"),

# ATTENDANCE ANALYTICS PAGE (TEACHER)
  path("attendance_analytics", views.attendance_analytics, name="attendance_analytics"),

]
