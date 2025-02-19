from django.db import models
from django.core.validators import RegexValidator
import string

# BATCH MODEL
class Batch(models.Model):
    batch_year = models.IntegerField()

    def __str__(self):
        return f"Batch {self.batch_year}"

# COURSE MODEL
class Course(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="courses")
    course_id = models.CharField(max_length=20, unique=True, null=True)
    course_name = models.CharField(max_length=100)
    course_duration = models.IntegerField()
    total_semesters = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.course_id:
            total_courses = Course.objects.filter(batch=self.batch).count() + 1
            self.course_id = f"{str(self.batch.batch_year)}C{str(total_courses).zfill(2)}"
        super(Course, self).save(*args, **kwargs)
        self.create_semesters()

    def create_semesters(self):
        existing_semesters = Semester.objects.filter(course=self).count()
        for semester_num in range(existing_semesters + 1, self.total_semesters + 1):
            semester_id = f"{str(self.course_id)}S{str(semester_num).zfill(2)}"
            Semester.objects.create(
                batch=self.batch,
                course=self,
                semester_id=semester_id,
                semester_num=semester_num
            )

    def __str__(self):
        return f"{self.course_name} - {self.batch.batch_year}"
    
# SEMESTER MODEL
class Semester(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="semesters")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="semesters")
    semester_id = models.CharField(max_length=20, unique=True, null=True)
    semester_num = models.IntegerField()

    def __str__(self):
        return f"{self.course.course_name} - {self.batch.batch_year} Sem {self.semester_num}"
    
# SECTION MODEL
class Section(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="sections")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="sections")
    section_id = models.CharField(max_length=20, unique=True, null=True)
    section_name = models.CharField(max_length=50)
    
    def save(self, *args, **kwargs):
        if not self.section_id:
            total_sections = Section.objects.filter(
                batch=self.batch, course=self.course, semester=self.semester
            ).count()
            section_letter = string.ascii_uppercase[total_sections]
            self.section_id = f"{str(self.semester.semester_id)}{section_letter}"
        super(Section, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.course_name} - {self.batch.batch_year} Sem {self.semester.semester_num} ({self.section_name})"
    
# SUBJECT MODEL
class Subject(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="subjects")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subjects")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="subjects")
    subject_id = models.CharField(max_length=20, unique=True, null=True)
    subject_name = models.CharField(max_length=50)
    
    def save(self, *args, **kwargs):
        if not self.subject_id:
            total_subjects = Subject.objects.filter(
                batch=self.batch, course=self.course, semester=self.semester
            ).count() + 1
            self.subject_id = f"{str(self.semester.semester_id)}{str(total_subjects).zfill(2)}"
        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.course_name} - {self.batch.batch_year} Sem {self.semester.semester_num} - Subject: ({self.subject_name})"

# STUDENT MODEL
class Student(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="students")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="students")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="students")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="students")
    student_id = models.CharField(max_length=20, unique=True, null=True)
    student_name = models.CharField(max_length=50)
    student_roll = models.IntegerField()
    student_phone = models.CharField(
        max_length=10, 
        validators=[RegexValidator(regex=r'^\d{10}$', message="Phone number must be exactly 10 digits.")]
    )

    def save(self, *args, **kwargs):
        if not self.student_id:
            total_students = Student.objects.filter(batch=self.batch, course=self.course, semester=self.semester, section=self.section).count() + 1
            self.student_id = f"{str(self.section.section_id)}{str(total_students).zfill(3)}"
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.course_name} - {self.batch.batch_year} Sem {self.semester.semester_num} ({self.section.section_name}) - {self.student_name}({self.student_roll})"
    
# ATTENDANCE MODEL:
class Attendance(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="attendance_records")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="attendance_records")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="attendance_records")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="attendance_records")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="attendance_records")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField(auto_now_add=True, db_index=True)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return (f"{self.course.course_name} - {self.batch.batch_year} "
                f"Sem {self.semester.semester_num} ({self.section.section_name}) - "
                f"{self.student.student_name} ({self.student.student_roll}) - {self.is_present}")

    class Meta:
        indexes = [
            models.Index(fields=['batch', 'course', 'semester', 'section', 'subject', 'student', 'date']),
        ]
        