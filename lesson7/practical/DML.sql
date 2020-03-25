insert into faculty(faculty_name) values ('ITS');
insert into faculty(faculty_name) values ('IPSA');
insert into faculty(faculty_name) values ('IEE');
insert into faculty(faculty_name) values ('FIOT');

insert into academic_group (academic_group_name, faculty_id) values ('TS-51', (select id from faculty where faculty_name = 'ITS'));
insert into academic_group (academic_group_name, faculty_id) values ('TS-52', (select id from faculty where faculty_name = 'ITS'));
insert into academic_group (academic_group_name, faculty_id) values ('TS-51', (select id from faculty where faculty_name = 'IEE'));
insert into academic_group (academic_group_name, faculty_id) values ('IE-51', (select id from faculty where faculty_name = 'IEE'));
insert into academic_group (academic_group_name, faculty_id) values ('OT-51', (select id from faculty where faculty_name = 'IPSA'));
insert into academic_group (academic_group_name, faculty_id) values ('OT-51', (select id from faculty where faculty_name = 'FIOT'));
insert into academic_group (academic_group_name, faculty_id) values ('OT-52', (select id from faculty where faculty_name = 'FIOT'));

insert into student (students_card, student_name, student_surname, academic_group_id)
values
(
(select abs(random())),
'Oleksandr',
'Rusalovskyi',
(SELECT
	ag.id
 from academic_group ag join faculty f on ag.faculty_id = f.id
 where f.faculty_name='ITS'
   and ag.academic_group_name='TS-52'
)
)
;
insert into student (students_card, student_name, student_surname, academic_group_id)
values
(
(select abs(random())),
'Anton',
'Klymyk',
(SELECT
	ag.id
 from academic_group ag join faculty f on ag.faculty_id = f.id
 where f.faculty_name='ITS'
   and ag.academic_group_name='TS-52'
)
)
;
insert into student (students_card, student_name, student_surname, academic_group_id)
values
(
(select abs(random())),
'Maria',
'Pysareva',
(SELECT
	ag.id
 from academic_group ag join faculty f on ag.faculty_id = f.id
 where f.faculty_name='ITS'
   and ag.academic_group_name='TS-51'
)
)
;
insert into student (students_card, student_name, student_surname, academic_group_id)
values
(
(select abs(random())),
'Ivan',
'Ivanov',
(SELECT
	ag.id
 from academic_group ag join faculty f on ag.faculty_id = f.id
 where f.faculty_name='IEE'
   and ag.academic_group_name='TS-51'
)
)
;
insert into student (students_card, student_name, student_surname, academic_group_id)
values
(
(select abs(random())),
'Oleksandr',
'Honcharov',
(SELECT
	ag.id
 from academic_group ag join faculty f on ag.faculty_id = f.id
 where f.faculty_name='IEE'
   and ag.academic_group_name='IE-51'
)
)
;
insert into student (students_card, student_name, student_surname, academic_group_id)
values
(
(select abs(random())),
'Oleksandr',
'Lutyi',
(SELECT
	ag.id
 from academic_group ag join faculty f on ag.faculty_id = f.id
 where f.faculty_name='IPSA'
   and ag.academic_group_name='OT-51'
)
)
;
insert into student (students_card, student_name, student_surname, academic_group_id)
values
(
(select abs(random())),
'Oleksandr',
'Polyan',
(SELECT
	ag.id
 from academic_group ag join faculty f on ag.faculty_id = f.id
 where f.faculty_name='FIOT'
   and ag.academic_group_name='OT-51'
)
)
;
insert into student (students_card, student_name, student_surname, academic_group_id)
values
(
(select abs(random())),
'Mikhailo',
'Kalinin',
(SELECT
	ag.id
 from academic_group ag join faculty f on ag.faculty_id = f.id
 where f.faculty_name='FIOT'
   and ag.academic_group_name='OT-51'
)
)
;
insert into student (students_card, student_name, student_surname, academic_group_id)
values
(
(select abs(random())),
'Serhii',
'Kutyr',
(SELECT
	ag.id
 from academic_group ag join faculty f on ag.faculty_id = f.id
 where f.faculty_name='FIOT'
   and ag.academic_group_name='OT-52'
)
)
;
insert into student (students_card, student_name, student_surname, academic_group_id)
values
(
(select abs(random())),
'Gennadiy',
'Korban',
(SELECT
	ag.id
 from academic_group ag join faculty f on ag.faculty_id = f.id
 where f.faculty_name='FIOT'
   and ag.academic_group_name='OT-52'
)
)
;

insert into marks (student_id, mark)
WITH 
  fibo (mark)
AS
  ( SELECT abs(random()) % 4 + 2
    UNION ALL
    SELECT abs(random()) % 4 + 2 FROM fibo
    LIMIT (select abs(random()) % 7 + 4) )
SELECT s.id, f.mark 
FROM fibo f
cross join student s
where s.id=(select id from student order by id limit 1)
union all
SELECT s.id, f.mark 
FROM fibo f
cross join student s
where s.id=(select id from student order by id limit 1 offset 1)
union all
SELECT s.id, f.mark 
FROM fibo f
cross join student s
where s.id=(select id from student order by id limit 1 offset 2)
union all
SELECT s.id, f.mark 
FROM fibo f
cross join student s
where s.id=(select id from student order by id limit 1 offset 3)
union all
SELECT s.id, f.mark 
FROM fibo f
cross join student s
where s.id=(select id from student order by id limit 1 offset 4)
union all
SELECT s.id, f.mark 
FROM fibo f
cross join student s
where s.id=(select id from student order by id limit 1 offset 5)
union all
SELECT s.id, f.mark 
FROM fibo f
cross join student s
where s.id=(select id from student order by id limit 1 offset 6)
union all
SELECT s.id, f.mark 
FROM fibo f
cross join student s
where s.id=(select id from student order by id limit 1 offset 7)
union all
SELECT s.id, f.mark 
FROM fibo f
cross join student s
where s.id=(select id from student order by id limit 1 offset 8)
union all
SELECT s.id, f.mark 
FROM fibo f
cross join student s
where s.id=(select id from student order by id limit 1 offset 9)
;

commit;

select * from faculty;
select * from academic_group;
select * from student;
select * from marks;

--delete from marks;
--delete from student;
--delete from academic_group;
--delete from faculty;
--
--commit;