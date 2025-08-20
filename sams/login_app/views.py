from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .decorators import unauthenticated_user
from django.shortcuts import get_object_or_404
from .models import Batch, Course, Semester, Section, Subject, Student, Attendance
import string
from datetime import date, datetime
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# ------------------- HOME PAGE --------------------
# INDEX VIEW
def index(request):
    return render(request,'index.html')

# ------------------- SIGNUP, LOGIN & LOGOUT PAGE --------------------
# SIGNUP VIEW
@unauthenticated_user
def signup(request):
    group_name = request.GET.get('group', 'teacher')
    if request.user.is_authenticated:
        if request.user.groups.filter(name='admin').exists():
            return redirect('admin_profile') 
        elif request.user.groups.filter(name='teacher').exists():
            return redirect('teacher_profile')  
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
            else:
                if group_name == 'admin' and User.objects.filter(groups__name='admin').exists():
                    messages.error(request, "Admin already exists. Only one admin is allowed.")
                else:
                    user = form.save()
                    group = Group.objects.get(name=group_name)
                    user.groups.add(group)
                    messages.success(request, f"Account created successfully! Please log in as {group_name}.")
                    return redirect(f'{reverse("login")}?group={group_name}')
    context = {'form': form, 'group_name': group_name}
    return render(request, 'signup.html', context)

# LOGIN VIEW
@unauthenticated_user
def login_view(request):
    group_name = request.GET.get('group', 'teacher')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if group_name == "admin" and user.groups.filter(name="admin").exists():
                login(request, user)
                return redirect('admin_profile')
            elif group_name == "teacher" and user.groups.filter(name="teacher").exists():
                login(request, user)
                return redirect('teacher_profile')
            else:
                messages.error(request, f"Invalid login. This account does not belong to the {group_name} group.")
        else:
            messages.error(request, "Username or password is incorrect")
    context = {'group_name': group_name}
    return render(request, 'login.html', context)


# LOGOUT VIEW
def logout_view(request):
    logout(request)
    return redirect('/')
    
# ------------------- PROFILE (ADMIN & TEACHER), ADMIN ACCOUNT DELETION & CHANGE PASSWORD PAGE --------------------
# ADMIN PROFILE VIEW
@login_required
def admin_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            email = request.POST.get("email")
            if email:
                request.user.email = email
                request.user.save()
                messages.success(request, "Email updated successfully.")
                return redirect("admin_profile")
            else:
                messages.error(request, "Email cannot be empty.")
        context = {'user': request.user}
        return render(request,'admin_profile.html', context)
    else:
        return redirect('login')

# TEACHER PROFILE VIEW
@login_required
def teacher_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            email = request.POST.get("email")
            if email:
                request.user.email = email
                request.user.save()
                messages.success(request, "Email updated successfully.")
                return redirect("teacher_profile")
            else:
                messages.error(request, "Email cannot be empty.")
        context = {'user': request.user}
        return render(request,'teacher_profile.html', context)
    else:
        return redirect('login')
    
# ADMIN ACCOUNT DELETION VIEW
def delete_admin_account(request):
    if request.user.groups.filter(name='admin').exists():
        request.user.delete()
        logout(request)
        messages.success(request, "Your admin account has been deleted successfully.")
        return redirect('/')
    else:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('/')
    

#FORGOT PASSWORD VIEW (BOTH ADMIN & TEACHER)
class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        group = None
        if user.is_authenticated:
            user_group = user.groups.first()
            group = user_group.name if user_group else None
        context['group'] = group or self.request.GET.get('group', 'teacher')
        return context

    def get_success_url(self):
        group = self.request.GET.get('group', 'teacher')
        return reverse('password_reset_done') + f'?group={group}'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        
        if not User.objects.filter(email=email).exists():
            messages.error(self.request, "No account found with this email address.")
            return self.form_invalid(form) 

        group = self.request.GET.get('group', 'teacher') 
        form.save(
        request=self.request,
        use_https=self.request.is_secure(),
        email_template_name=self.email_template_name,
        extra_email_context={
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': self.request.get_host(),
            'group': group 
        },
    )
        return redirect(self.get_success_url())


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'

    def dispatch(self, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')

        if not uidb64 or not token:
            messages.error(self.request, "Invalid reset link.")
            return redirect('password_reset')

        return super().dispatch(*args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        group = request.GET.get('group', None)
        if group:
            request.session['reset_group'] = group
        
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.request.session.get('reset_group', 'teacher') 
        return context

    def get_success_url(self):
        group = self.request.session.pop('reset_group', 'teacher')
        return reverse('password_reset_complete') + f"?group={group}"


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.request.GET.get('group', 'teacher')
        return context


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.request.GET.get('group', 'teacher')
        return context
    
    
# CHANGE PASSWORD VIEW (BOTH ADMIN & TEACHER)
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) 
            messages.success(request, 'Your password was successfully updated!')
        else:
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)
    if request.user.groups.filter(name='admin').exists():            
        return redirect('admin_profile') 
    elif request.user.groups.filter(name='teacher').exists():
        return redirect('teacher_profile')  
    else:
        messages.error(request, 'Your role is not recognized!')
        return redirect('/')

# ------------------- ADMIN DASHBOARD PAGE --------------------
# ADMIN DASHBOARD VIEW
@login_required
def dashboard(request):
    if request.user.is_authenticated:
        # teachers
        teacher_group = Group.objects.get(name="teacher")
        teacher_count = teacher_group.user_set.count()
        # students
        student_count = Student.objects.count()
        # courses
        total_unique_courses = Course.objects.values("course_name").distinct().count()
        # attendance
        total_attendance = Attendance.objects.count()
        total_present = Attendance.objects.filter(is_present=True).count()
        attendance_percent = (total_present/total_attendance)*100 if total_attendance>0 else 0
        context = {
            'user': request.user, 
            'teacher_count': teacher_count,
            'student_count': student_count,
            'total_unique_courses': total_unique_courses,
            'attendance_percent': attendance_percent
        }
        return render(request,'dashboard.html', context)
    else:
        return redirect('login')
    
# ------------------- TEACHERS PAGE --------------------
# MANAGE TEACHERS VIEW
@login_required
def manage_teachers(request):
    teachers_group = Group.objects.get(name="teacher")
    teachers = teachers_group.user_set.all()
    if request.method == "POST":
        name = request.POST.get("teacher_name")
        email = request.POST.get("teacher_email")
        password = request.POST.get("teacher_password")
        if User.objects.filter(username=name).exists():
            messages.error(request, "Teacher with this name already exists.")
        else:
            user = User.objects.create_user(username=name, email=email, password=password)
            teachers_group.user_set.add(user) 
            messages.success(request, "New teacher added successfully.")
        return redirect("manage_teachers")
    return render(request, "manage_teachers.html", {"teachers": teachers})

# UPDATE TEACHER VIEW
@login_required
def update_teacher(request, pk):
    teacher = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        teacher.username = request.POST.get("teacher_name")
        teacher.email = request.POST.get("teacher_email")
        teacher.save()
        messages.success(request, "Teacher updated successfully.")
        return redirect("manage_teachers")
    return render(request, "update_teacher.html", {"teacher": teacher})

# DELETE TEACHER VIEW
@login_required
def delete_teacher(request, pk):
    teacher = get_object_or_404(User, pk=pk)
    teacher.delete()
    messages.success(request, "Teacher deleted successfully.")
    return redirect("manage_teachers")

# ------------------- BATCHES PAGE --------------------
# MANAGE BATCHES VIEW
@login_required
def manage_batches(request):
    batches = Batch.objects.all()
    if request.method == "POST":
        batch_year = request.POST.get("batch_year")
        if batch_year:
            Batch.objects.create(batch_year=batch_year)
            return redirect("manage_batches")
    context = {"batches": batches}
    return render(request, "manage_batches.html", context)

# UPDATE BATCH VIEW
@login_required
def update_batch(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    if request.method == "POST":
        batch_year = request.POST.get("batch_year")
        if batch_year:
            batch.batch_year = batch_year
            batch.save()
            return redirect("manage_batches")
    context = {"batch": batch}
    return render(request, "update_batch.html", context)

# DELETE BATCH VIEW
@login_required
def delete_batch(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    batch.delete()
    return redirect("manage_batches")

# ------------------- COURSES PAGE --------------------
# MANAGE COURSES VIEW
@login_required
def manage_courses(request):
    batches = Batch.objects.all()

    batch_id = request.GET.get("batch_id")
    selected_batch = Batch.objects.filter(id=batch_id).first() or batches.first()
    
    courses = Course.objects.filter(batch=selected_batch) if selected_batch else None

    if request.method == "POST":
        batch_id = request.POST.get("choose_batch")
        course_name = request.POST.get("course_name")
        course_duration = request.POST.get("course_duration")
        total_semesters = request.POST.get("total_semesters")
        
        if not (batch_id and course_name and course_duration and total_semesters):
            messages.error(request, "All fields are required to add a course.")
            return redirect(reverse("manage_courses"))
                
        selected_batch = get_object_or_404(Batch, id=batch_id) 
        
        total_courses = Course.objects.filter(batch=selected_batch).count()+1
        course_id = f"{str(selected_batch.batch_year)}C{str(total_courses).zfill(2)}"
        course_duration = int(course_duration)
        total_semesters = int(total_semesters)

        Course.objects.create(
            course_name=course_name,
            course_duration=course_duration,
            total_semesters=total_semesters,
            batch=selected_batch,
            course_id=course_id
        )
        messages.success(request, "New course added successfully!")
        return redirect(f"{reverse('manage_courses')}?batch_id={selected_batch.id}")

    return render(request, "manage_courses.html", {
        "batches": batches,
        "selected_batch": selected_batch,
        "courses": courses
    })

# UPDATE COURSE VIEW
@login_required
def update_course(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    if request.method == "POST":
        course_name = request.POST.get("course_name")
        course_duration = request.POST.get("course_duration")
        total_semesters = request.POST.get("total_semesters")
        if course_name and course_duration and total_semesters:
            try:
                course_duration = int(course_duration)
                total_semesters = int(total_semesters)
                course.course_name = course_name
                course.course_duration = course_duration
                if total_semesters != course.total_semesters:
                    course.total_semesters = total_semesters
                    if total_semesters < course.semesters.count():
                        Semester.objects.filter(course=course, semester_num__gt=total_semesters).delete()
                    course.create_semesters()
                course.save()
                messages.success(request, "Course updated successfully!")
                return redirect(f"{reverse('manage_courses')}?batch_id={course.batch.id}")
            except ValueError:
                messages.error(request, "Course duration and total semesters must be valid integers.")
        else:
            messages.error(request, "All fields are required to update the course.")
    context = {"course": course}
    return render(request, "update_course.html", context)

# DELETE COURSE VIEW
def delete_course(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    batch_id = course.batch.id  
    course.delete()
    messages.success(request, f"The course '{course.course_id}' has been deleted successfully.")
    return redirect(f"{reverse('manage_courses')}?batch_id={batch_id}")

# ------------------- SECTIONS PAGE --------------------
# MANAGE SECTIONS VIEW
@login_required
def manage_sections(request):
    batches = Batch.objects.all()
    
    batch_id = request.GET.get("batch_id")
    selected_batch = Batch.objects.filter(id=batch_id).first() or batches.first()
    
    # Get Courses for the Selected Batch
    courses = Course.objects.filter(batch=selected_batch) if selected_batch else None
    course_id = request.GET.get("course_id")
    selected_course = Course.objects.filter(id=course_id, batch=selected_batch).first() or (courses.first() if courses else None)
    
    # Get Semesters for the Selected Course
    semesters = Semester.objects.filter(course=selected_course) if selected_batch and selected_course else None
    semester_id = request.GET.get("semester_id")
    selected_semester = Semester.objects.filter(id=semester_id, course=selected_course).first() or (semesters.first() if semesters else None)

    # Get Sections for the Selected Semester
    sections = Section.objects.filter(batch=selected_batch, course=selected_course, semester=selected_semester) if selected_batch and selected_course and selected_semester else None

    if request.method == "POST":
        batch_id = request.POST.get("choose_batch")
        course_id = request.POST.get("choose_course")
        semester_id = request.POST.get("choose_semester")
        section_name = request.POST.get("section_name")

        if not (batch_id and course_id and semester_id and section_name):
            messages.error(request, "All fields are required to add a section.")
            return redirect(reverse("manage_sections"))
            
        selected_batch = get_object_or_404(Batch, id=batch_id)
        selected_course = get_object_or_404(Course, id=course_id, batch=selected_batch)
        selected_semester = get_object_or_404(Semester, id=semester_id, course=selected_course)

        total_sections = Section.objects.filter(batch=selected_batch,course=selected_course, semester=selected_semester).count()
        section_letter = string.ascii_uppercase[total_sections]
        section_id = f"{str(selected_semester.semester_id)}{section_letter}"
        
        Section.objects.create(
            section_name=section_name,
                batch=selected_batch,
                course=selected_course,
                semester=selected_semester,
                section_id=section_id,
        )
        messages.success(request, "New Section added successfully!")
        return redirect(f"{reverse('manage_sections')}?batch_id={selected_batch.id}&course_id={selected_course.id}&semester_id={selected_semester.id}")
    
    return render(
        request,
        "manage_sections.html",
        {
            "batches": batches,
            "courses": courses or [],
            "semesters": semesters or [],
            "sections": sections or [],
            "selected_batch": selected_batch,
            "selected_course": selected_course,
            "selected_semester": selected_semester,
        },
    )

# UPDATE SECTION VIEW
@login_required
def update_section(request, section_id):
    section = get_object_or_404(Section, section_id=section_id)
    if request.method == "POST":
        section_name = request.POST.get("section_name")
        if section_name:
            section.section_name = section_name
            section.save()
            messages.success(request, f"Section '{section.section_id}' updated successfully!")
            return redirect(f"{reverse('manage_sections')}?batch_id={section.batch.id}&course_id={section.course.id}&semester_id={section.semester.id}")
        else:
            messages.error(request, "Section name cannot be empty.")
    return render(request, "update_section.html", {"section": section})

# DELETE SECTION VIEW
@login_required
def delete_section(request, section_id):
    section = get_object_or_404(Section, section_id=section_id)
    batch_id = section.batch.id
    course_id = section.course.id
    semester_id = section.semester.id
    section.delete()
    messages.success(request, f"Section '{section.section_id}' deleted successfully!")
    return redirect(f"{reverse('manage_sections')}?batch_id={batch_id}&course_id={course_id}&semester_id={semester_id}")

# ------------------- SUBJECTS PAGE --------------------
# MANAGE SUBJECTS VIEW
@login_required
def manage_subjects(request):
    batches = Batch.objects.all()
    
    batch_id = request.GET.get("batch_id")
    selected_batch = Batch.objects.filter(id=batch_id).first() or batches.first()
    
    # Get Courses for the Selected Batch
    courses = Course.objects.filter(batch=selected_batch) if selected_batch else None
    course_id = request.GET.get("course_id")
    selected_course = Course.objects.filter(id=course_id, batch=selected_batch).first() or (courses.first() if courses else None)
    
    # Get Semesters for the Selected Course
    semesters = Semester.objects.filter(course=selected_course) if selected_batch and selected_course else None
    semester_id = request.GET.get("semester_id")
    selected_semester = Semester.objects.filter(id=semester_id, course=selected_course).first() or (semesters.first() if semesters else None)
    
    # Get Subjects for the Selected Semester
    subjects = Subject.objects.filter(batch=selected_batch, course=selected_course, semester=selected_semester) if selected_batch and selected_course and selected_semester else None
    
    if request.method == "POST":
        batch_id = request.POST.get("choose_batch")
        course_id = request.POST.get("choose_course")
        semester_id = request.POST.get("choose_semester")
        subject_name = request.POST.get("subject_name")
        
        if not (batch_id and course_id and semester_id and subject_name):
            messages.error(request, "All fields are required to add a subject.")
            return redirect(reverse("manage_subjects"))
        
        selected_batch = get_object_or_404(Batch, id=batch_id)
        selected_course = get_object_or_404(Course, id=course_id, batch=selected_batch)
        selected_semester = get_object_or_404(Semester, id=semester_id, course=selected_course)
        
        total_subjects = Subject.objects.filter(batch=selected_batch, course=selected_course,semester=selected_semester).count()+1
        subject_id = f"{str(selected_semester.semester_id)}{str(total_subjects).zfill(2)}"
            
        Subject.objects.create(
            subject_name=subject_name,
            batch=selected_batch,
            course=selected_course,
            semester=selected_semester,
            subject_id=subject_id,
        )
        messages.success(request, f"New Subject added successfully!")
        return redirect(f"{reverse('manage_subjects')}?batch_id={selected_batch.id}&course_id={selected_course.id}&semester_id={selected_semester.id}")
       
    return render(
        request,
        "manage_subjects.html",
        {
            "batches": batches,
            "courses": courses or [],
            "semesters":semesters or [],
            "subjects": subjects or [],
            "selected_batch": selected_batch,
            "selected_course": selected_course,
            "selected_semester": selected_semester,
        },
    )

# UPDATE SUBJECT VIEW
@login_required
def update_subject(request, subject_id):
    subject = get_object_or_404(Subject, subject_id=subject_id)
    if request.method == "POST":
        subject_name = request.POST.get("subject_name")
        if subject_name:
            subject.subject_name = subject_name
            subject.save()
            messages.success(request, f"Subject '{subject.subject_id}' updated successfully!")
            return redirect(f"{reverse('manage_subjects')}?batch_id={subject.batch.id}&course_id={subject.course.id}&semester_id={subject.semester.id}")
        else:
            messages.error(request, "Subject name cannot be empty.")
    return render(request, "update_subject.html", {"subject": subject})

# DELETE SUBJECT VIEW
@login_required
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, subject_id=subject_id)
    batch_id = subject.batch.id
    course_id = subject.course.id
    semester_id = subject.semester.id
    subject.delete()
    messages.success(request, f"Subject '{subject.subject_id}' deleted successfully!")
    return redirect(f"{reverse('manage_subjects')}?batch_id={batch_id}&course_id={course_id}&semester_id={semester_id}")

# ------------------- STUDENTS PAGE --------------------
# MANAGE STUDENTS VIEW
@login_required
def manage_students(request):
    batches = Batch.objects.all()
    
    batch_id = request.GET.get("batch_id")
    selected_batch = Batch.objects.filter(id=batch_id).first() or batches.first()
    
    # Get Courses for the Selected Batch
    courses = Course.objects.filter(batch=selected_batch) if selected_batch else None
    course_id = request.GET.get("course_id")
    selected_course = Course.objects.filter(id=course_id, batch=selected_batch).first() or (courses.first() if courses else None)
    
    # Get Semesters for the Selected Course
    semesters = Semester.objects.filter(course=selected_course) if selected_batch and selected_course else None
    semester_id = request.GET.get("semester_id")
    selected_semester = Semester.objects.filter(id=semester_id, course=selected_course).first() or (semesters.first() if semesters else None)
    
    # Get Sections for the Selected Semester
    sections = Section.objects.filter(semester=selected_semester) if selected_batch and selected_course and selected_semester else None
    section_id = request.GET.get("section_id")
    selected_section = Section.objects.filter(id=section_id, semester=selected_semester).first() or (sections.first() if sections else None)
    
    students = Student.objects.filter(batch=selected_batch, course=selected_course, semester=selected_semester, section=selected_section).order_by('student_roll') if selected_batch and selected_course and selected_semester and selected_section else None
    
    if request.method == "POST":
        batch_id = request.POST.get("choose_batch")
        course_id = request.POST.get("choose_course")
        semester_id = request.POST.get("choose_semester")
        section_id = request.POST.get("choose_section")
        student_name = request.POST.get("student_name")
        student_roll = request.POST.get("student_roll")
        student_phone = request.POST.get("student_phone")

         # Validate Roll Number (Only digits)
        if not student_roll.isdigit():
            messages.error(request, "Roll number must contain only digits.")
            return redirect(reverse("manage_students"))

          # Validate Phone Number
        if not student_phone.isdigit() or len(student_phone) != 10:
           messages.error(request, "Phone number must be exactly 10 digits and contain only numbers.")
           return redirect(reverse("manage_students"))

        if not (batch_id and course_id and semester_id and section_id and student_name and student_roll and student_phone):
            messages.error(request, "All fields are required to add a student.")
            return redirect(reverse("manage_students"))
        
        selected_batch = get_object_or_404(Batch, id=batch_id)
        selected_course = get_object_or_404(Course, id=course_id, batch=selected_batch)
        selected_semester = get_object_or_404(Semester, id=semester_id, course=selected_course)
        selected_section = get_object_or_404(Section, id=section_id, semester=selected_semester)
        
        total_students = Student.objects.filter(batch=selected_batch, course=selected_course,semester=selected_semester, section=selected_section).count()+1
        student_id = f"{str(selected_section.section_id)}{str(total_students).zfill(3)}"
        Student.objects.create(
            student_name=student_name,
            student_roll=student_roll,
            student_phone=student_phone,
            batch=selected_batch,
            course=selected_course,
            semester=selected_semester,
            section=selected_section,
            student_id=student_id,
        )
        messages.success(request, f"New Student added successfully!")
        return redirect(f"{reverse('manage_students')}?batch_id={selected_batch.id}&course_id={selected_course.id}&semester_id={selected_semester.id}&section_id={selected_section.id}")
    
    return render(
        request,
        "manage_students.html",
        {
            "batches": batches,
            "courses": courses or [],
            "semesters":semesters or [],
            "sections": sections or [],
            "students": students or [],
            "selected_batch": selected_batch,
            "selected_course": selected_course,
            "selected_semester": selected_semester,
            "selected_section": selected_section,
        },
    )

# UPDATE STUDENT VIEW
@login_required
def update_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == "POST":
        student_name = request.POST.get("student_name")
        student_roll = request.POST.get("student_roll")
        student_phone = request.POST.get("student_phone")


         # Validate Roll Number (Only digits)
        if not student_roll.isdigit():
            messages.error(request, "Roll number must contain only digits.")
            return redirect(reverse("manage_students"))
        # Validate Phone Number
        if not student_phone.isdigit() or len(student_phone) != 10:
           messages.error(request, "Phone number must be exactly 10 digits and contain only numbers.")
           return redirect(reverse("update_student", args=[student_id]))

        if student_name and student_roll and student_phone:
            student.student_name = student_name
            student.student_roll = student_roll
            student.student_phone = student_phone
            student.save()
            messages.success(request, f"Student '{student.student_id}' updated successfully!")
            return redirect(f"{reverse('manage_students')}?batch_id={student.batch.id}&course_id={student.course.id}&semester_id={student.semester.id}&section_id={student.section.id}")
        else:
            messages.error(request, "Student name or roll or phone cannot be empty.")
    return render(request, "update_student.html", {"student": student})

# DELETE STUDENT VIEW
@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    batch_id = student.batch.id
    course_id = student.course.id
    semester_id = student.semester.id
    section_id = student.section.id
    student.delete()
    messages.success(request, f"Student '{student.student_id}' deleted successfully!")
    return redirect(f"{reverse('manage_students')}?batch_id={batch_id}&course_id={course_id}&semester_id={semester_id}&section_id={section_id}")

# ------------------- MANAGE ATTENDANCE RECORD PAGE (ADMIN) --------------------
def manage_attendance_record(request):
    batches = Batch.objects.prefetch_related('courses').all()
    selected_batch = None
    selected_course = None
    selected_semester = None
    selected_section = None
    selected_subject = None
    selected_date = None
    courses = []
    semesters = []
    sections = []
    subjects = []
    students = []
    attendance_records = []
    if request.method=="GET":
        batch_id = request.GET.get("batch")
        course_id = request.GET.get("course")
        semester_id = request.GET.get("semester")
        section_id = request.GET.get("section")
        subject_id = request.GET.get("subject")
        date = request.GET.get("date")
        if batch_id:
            selected_batch = get_object_or_404(Batch, id=batch_id)
            courses = selected_batch.courses.prefetch_related('semesters')
        if course_id:
            selected_course = get_object_or_404(Course, id=course_id)
            semesters = selected_course.semesters.prefetch_related('sections', 'subjects')
        if semester_id:
            selected_semester = get_object_or_404(Semester, id=semester_id)
            sections = selected_semester.sections.prefetch_related('students')
            subjects = selected_semester.subjects.all()
        if section_id:
            selected_section = get_object_or_404(Section, id=section_id)
            students = selected_section.students.order_by('student_roll')
        if subject_id:
            selected_subject = get_object_or_404(Subject, id=subject_id)
        if date:
            try:
                selected_date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                selected_date = None
        if selected_batch and selected_course and selected_semester and selected_section and selected_subject and selected_date:
            attendance_records = Attendance.objects.filter(
                batch=selected_batch,
                course=selected_course,
                semester=selected_semester,
                section=selected_section,
                subject=selected_subject,
                date=selected_date,
            ).select_related('student')
    if not selected_batch and batches:
        selected_batch = batches.first()
        courses = selected_batch.courses.all()
    if selected_batch and not selected_course and courses:
        selected_course = courses.first()
        semesters = selected_course.semesters.all()
    if selected_course and not selected_semester and semesters:
        selected_semester = semesters.first()
        sections = selected_semester.sections.all()
        subjects = selected_semester.subjects.all()
    if selected_semester and not selected_section and sections:
        selected_section = sections.first()
        students = selected_section.students.order_by('student_roll')
    if selected_semester and not selected_subject and subjects:
        selected_subject = subjects.first()
    return render(request, "manage_attendance_record.html", {
        "batches": batches,
        "courses": courses,
        "semesters": semesters,
        "sections": sections,
        "subjects": subjects,
        "students": students,
        "selected_batch": selected_batch,
        "selected_course": selected_course,
        "selected_semester": selected_semester,
        "selected_section": selected_section,
        "selected_subject": selected_subject,
        "attendance_records": attendance_records,
        "selected_date": selected_date,
    })

# ------------------- STUDENT ATTENDANCE ANALYTICS PAGE (ADMIN)--------------------
def manage_attendance_analytics(request):
    batches = Batch.objects.all()
    selected_batch = request.GET.get('batch')
    selected_course = request.GET.get('course')
    selected_semester = request.GET.get('semester')
    selected_section = request.GET.get('section')
    selected_subject = request.GET.get('subject')

    analytics_data = None
    courses = semesters = sections = subjects = []

    if selected_batch:
        courses = Course.objects.filter(batch_id=selected_batch)
    if selected_course:
        semesters = Semester.objects.filter(course_id=selected_course)
    if selected_semester:
        sections = Section.objects.filter(semester_id=selected_semester)
        subjects = Subject.objects.filter(semester_id=selected_semester)

    if selected_batch and selected_course and selected_semester and selected_section and selected_subject:
        students = Student.objects.filter(
            batch_id=selected_batch,
            course_id=selected_course,
            semester_id=selected_semester,
            section_id=selected_section
        )
        total_days = Attendance.objects.filter(
            batch_id=selected_batch,
            course_id=selected_course,
            semester_id=selected_semester,
            section_id=selected_section,
            subject_id=selected_subject
        ).values('date').distinct().count()

        analytics_data = []

        for student in students:
            present_days = Attendance.objects.filter(
                student=student,
                subject_id=selected_subject,
                is_present=True
            ).count()
            absent_days = total_days - present_days
            percentage = round((present_days / total_days) * 100, 2) if total_days > 0 else 0
            fine_required = percentage < 60

            analytics_data.append({
                'student': student,
                'present_days': present_days,
                'absent_days': absent_days,
                'percentage': percentage,
                'fine_required': fine_required
            })

    context = {
        'batches': batches,
        'courses': courses,
        'semesters': semesters,
        'sections': sections,
        'subjects': subjects,
        'selected_batch': selected_batch,
        'selected_course': selected_course,
        'selected_semester': selected_semester,
        'selected_section': selected_section,
        'selected_subject': selected_subject,
        'analytics_data': analytics_data,
    }

    return render(request, 'manage_attendance_analytics.html', context)



# ------------------- MARK ATTENDANCE PAGE --------------------
def mark_attendance(request):
    batches = Batch.objects.prefetch_related('courses').all()
    selected_batch = None
    selected_course = None
    selected_semester = None
    selected_section = None
    selected_subject = None
    courses = []
    semesters = []
    sections = []
    subjects = []
    students = []
    if request.method == 'POST':
        batch_id = request.POST.get("batch")
        course_id = request.POST.get("course")
        semester_id = request.POST.get("semester")
        section_id = request.POST.get("section")
        subject_id = request.POST.get("subject")
        if batch_id:
            selected_batch = get_object_or_404(Batch, id=batch_id)
            courses = selected_batch.courses.prefetch_related('semesters')
        if course_id:
            selected_course = get_object_or_404(Course, id=course_id)
            semesters = selected_course.semesters.prefetch_related('sections', 'subjects')
        if semester_id:
            selected_semester = get_object_or_404(Semester, id=semester_id)
            sections = selected_semester.sections.prefetch_related('students')
            subjects = selected_semester.subjects.all()
        if section_id:
            selected_section = get_object_or_404(Section, id=section_id)
            students = selected_section.students.order_by('student_roll')
        if subject_id:
            selected_subject = get_object_or_404(Subject, id=subject_id)
    if not selected_batch and batches:
        selected_batch = batches.first()
        courses = selected_batch.courses.all()
    if selected_batch and not selected_course and courses:
        selected_course = courses.first()
        semesters = selected_course.semesters.all()
    if selected_course and not selected_semester and semesters:
        selected_semester = semesters.first()
        sections = selected_semester.sections.all()
        subjects = selected_semester.subjects.all()
    if selected_semester and not selected_section and sections:
        selected_section = sections.first()
        students = selected_section.students.order_by('student_roll')
    if selected_semester and not selected_subject and subjects:
        selected_subject = subjects.first()
    selected_attendance = []
    for student in students:
        attendance_key = f'attendance_{student.student_id}'
        if attendance_key in request.POST:
            selected_attendance.append(student.student_id)
    if 'submit_attendance' in request.POST:
        Attendance.objects.filter(
            batch=selected_batch,
            course=selected_course,
            semester=selected_semester,
            section=selected_section,
            subject=selected_subject,
            date=date.today(),
        ).delete()
        for student in students:
            attendance_key = f'attendance_{student.student_id}'
            is_present = attendance_key in request.POST
            Attendance.objects.update_or_create(
                batch=selected_batch,
                course=selected_course,
                semester=selected_semester,
                section=selected_section,
                subject=selected_subject,
                student=student,
                date=date.today(),
                defaults={'is_present': is_present},
            )
        messages.success(request, "Attendance has been successfully submitted!")
    return render(request, "mark_attendance.html", {
        "batches": batches,
        "courses": courses,
        "semesters": semesters,
        "sections": sections,
        "subjects": subjects,
        "students": students,
        "selected_batch": selected_batch,
        "selected_course": selected_course,
        "selected_semester": selected_semester,
        "selected_section": selected_section,
        "selected_subject": selected_subject,
        "selected_attendance": selected_attendance,
    })

# ------------------- ATTENDANCE RECORD PAGE (TEACHER) --------------------
def attendance_record(request):
    batches = Batch.objects.prefetch_related('courses').all()
    selected_batch = None
    selected_course = None
    selected_semester = None
    selected_section = None
    selected_subject = None
    selected_date = None
    courses = []
    semesters = []
    sections = []
    subjects = []
    students = []
    attendance_records = []
    if request.method=="GET":
        batch_id = request.GET.get("batch")
        course_id = request.GET.get("course")
        semester_id = request.GET.get("semester")
        section_id = request.GET.get("section")
        subject_id = request.GET.get("subject")
        date = request.GET.get("date")
        if batch_id:
            selected_batch = get_object_or_404(Batch, id=batch_id)
            courses = selected_batch.courses.prefetch_related('semesters')
        if course_id:
            selected_course = get_object_or_404(Course, id=course_id)
            semesters = selected_course.semesters.prefetch_related('sections', 'subjects')
        if semester_id:
            selected_semester = get_object_or_404(Semester, id=semester_id)
            sections = selected_semester.sections.prefetch_related('students')
            subjects = selected_semester.subjects.all()
        if section_id:
            selected_section = get_object_or_404(Section, id=section_id)
            students = selected_section.students.order_by('student_roll')
        if subject_id:
            selected_subject = get_object_or_404(Subject, id=subject_id)
        if date:
            try:
                selected_date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                selected_date = None
        if selected_batch and selected_course and selected_semester and selected_section and selected_subject and selected_date:
            attendance_records = Attendance.objects.filter(
                batch=selected_batch,
                course=selected_course,
                semester=selected_semester,
                section=selected_section,
                subject=selected_subject,
                date=selected_date,
            ).select_related('student')
    if not selected_batch and batches:
        selected_batch = batches.first()
        courses = selected_batch.courses.all()
    if selected_batch and not selected_course and courses:
        selected_course = courses.first()
        semesters = selected_course.semesters.all()
    if selected_course and not selected_semester and semesters:
        selected_semester = semesters.first()
        sections = selected_semester.sections.all()
        subjects = selected_semester.subjects.all()
    if selected_semester and not selected_section and sections:
        selected_section = sections.first()
        students = selected_section.students.order_by('student_roll')
    if selected_semester and not selected_subject and subjects:
        selected_subject = subjects.first()
    return render(request, "attendance_record.html", {
        "batches": batches,
        "courses": courses,
        "semesters": semesters,
        "sections": sections,
        "subjects": subjects,
        "students": students,
        "selected_batch": selected_batch,
        "selected_course": selected_course,
        "selected_semester": selected_semester,
        "selected_section": selected_section,
        "selected_subject": selected_subject,
        "attendance_records": attendance_records,
        "selected_date": selected_date,
    })

# ------------------- STUDENT ATTENDANCE ANALYTICS PAGE (TEACHER)--------------------
def attendance_analytics(request):
    batches = Batch.objects.all()
    selected_batch = request.GET.get('batch')
    selected_course = request.GET.get('course')
    selected_semester = request.GET.get('semester')
    selected_section = request.GET.get('section')
    selected_subject = request.GET.get('subject')

    analytics_data = None
    courses = semesters = sections = subjects = []

    if selected_batch:
        courses = Course.objects.filter(batch_id=selected_batch)
    if selected_course:
        semesters = Semester.objects.filter(course_id=selected_course)
    if selected_semester:
        sections = Section.objects.filter(semester_id=selected_semester)
        subjects = Subject.objects.filter(semester_id=selected_semester)

    if selected_batch and selected_course and selected_semester and selected_section and selected_subject:
        students = Student.objects.filter(
            batch_id=selected_batch,
            course_id=selected_course,
            semester_id=selected_semester,
            section_id=selected_section
        )
        total_days = Attendance.objects.filter(
            batch_id=selected_batch,
            course_id=selected_course,
            semester_id=selected_semester,
            section_id=selected_section,
            subject_id=selected_subject
        ).values('date').distinct().count()

        analytics_data = []

        for student in students:
            present_days = Attendance.objects.filter(
                student=student,
                subject_id=selected_subject,
                is_present=True
            ).count()
            absent_days = total_days - present_days
            percentage = round((present_days / total_days) * 100, 2) if total_days > 0 else 0
            fine_required = percentage < 60

            analytics_data.append({
                'student': student,
                'present_days': present_days,
                'absent_days': absent_days,
                'percentage': percentage,
                'fine_required': fine_required
            })

    context = {
        'batches': batches,
        'courses': courses,
        'semesters': semesters,
        'sections': sections,
        'subjects': subjects,
        'selected_batch': selected_batch,
        'selected_course': selected_course,
        'selected_semester': selected_semester,
        'selected_section': selected_section,
        'selected_subject': selected_subject,
        'analytics_data': analytics_data,
    }

    return render(request, 'attendance_analytics.html', context)

