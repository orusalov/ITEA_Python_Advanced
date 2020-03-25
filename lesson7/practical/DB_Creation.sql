create table faculty
(
id integer PRIMARY key AUTOINCREMENT,
faculty_name text not null
)
;

create table academic_group
(
id integer PRIMARY key AUTOINCREMENT,
academic_group_name text not null,
faculty_id integer not null,
constraint groups_faculty_fk foreign key (faculty_id) references faculty(id)
)
;

create table student
(
id integer PRIMARY key AUTOINCREMENT,
students_card text not null,
student_surname text not null,
student_name text not null,
academic_group_id integer not null references academic_group(id),
constraint u_student_card unique (students_card)
)
;

create table marks
(
student_id not null references student(id),
mark integer not null
)
;
