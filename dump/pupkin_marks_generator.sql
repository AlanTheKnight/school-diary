INSERT INTO diary_users(password, last_login, is_superuser, email, account_type, is_active, is_staff)
SELECT password, last_login, is_superuser, RANDOM()+ email, account_type, is_active, is_staff FROM diary_users where id = 3;

INSERT INTO diary_students(account_id, first_name, surname, second_name, grade_id)
SELECT id, 'Vasya'+ABS(RANDOM()%1000), 'Pupkin', 'SecName', 1 FROM diary_users where
        id not in (select account_id from diary_students);

INSERT INTO diary_lessons (date, homework, theme, grade_id, subject_id, control_id)
SELECT date, homework, theme, grade_id, subject_id, control_id FROM diary_lessons WHERE id = 1;

INSERT INTO diary_marks(amount, student_id, subject_id, lesson_id)
SELECT 5 as amount,
       diary_users.id as student_id,
       diary_lessons.subject_id as subject_id,
       diary_lessons.id as lesson_id
FROM diary_lessons, diary_users
WHERE diary_lessons.subject_id = 1 and diary_users.account_type = 3
AND (diary_users.id, diary_lessons.id) not in (SELECT student_id,lesson_id FROM diary_marks);





