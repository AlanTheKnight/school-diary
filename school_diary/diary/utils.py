from diary import models


def default_grades_and_subjects(teacher):
    available_subjects = teacher.subjects.all().order_by('name')
    available_grades = models.Grades.objects.filter(
        teachers=teacher).order_by('number', 'letter')
    return available_subjects, available_grades


def get_or_create_group(grade, subject):
    group = models.Groups.objects.get_or_create(grade_id=grade, subject_id=subject)
    if group[1]:  # If it hasn't been created yet
        group[0].set_default_students()
    group = group[0]
    return group
