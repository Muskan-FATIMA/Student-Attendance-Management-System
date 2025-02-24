# Generated by Django 5.1.4 on 2025-01-25 07:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=20, null=True, unique=True)),
                ('course_name', models.CharField(max_length=100)),
                ('course_duration', models.IntegerField()),
                ('total_semesters', models.IntegerField()),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='login_app.batch')),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_id', models.CharField(max_length=20, null=True, unique=True)),
                ('semester_num', models.IntegerField()),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semesters', to='login_app.batch')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semesters', to='login_app.course')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_id', models.CharField(max_length=20, null=True, unique=True)),
                ('section_name', models.CharField(max_length=50)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='login_app.batch')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='login_app.course')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='login_app.semester')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=20, null=True, unique=True)),
                ('student_name', models.CharField(max_length=50)),
                ('student_roll', models.IntegerField()),
                ('student_phone', models.IntegerField()),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='login_app.batch')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='login_app.course')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='login_app.section')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='login_app.semester')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_id', models.CharField(max_length=20, null=True, unique=True)),
                ('subject_name', models.CharField(max_length=50)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='login_app.batch')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='login_app.course')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='login_app.semester')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, db_index=True)),
                ('is_present', models.BooleanField(default=False)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='login_app.batch')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='login_app.course')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='login_app.section')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='login_app.semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='login_app.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='login_app.subject')),
            ],
            options={
                'indexes': [models.Index(fields=['batch', 'course', 'semester', 'section', 'subject', 'student', 'date'], name='login_app_a_batch_i_d53e1c_idx')],
            },
        ),
    ]
