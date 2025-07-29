--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: assets_branch; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.assets_branch (id, name, slug, created_at, choosable) FROM stdin;
1	stock	stock	2025-07-27 12:29:27+03	t
2	HQ	HQ	2025-07-27 12:29:34+03	t
3	Maadi	Maadi	2025-07-27 12:52:04+03	t
4	Assiut	Assiut	2025-07-27 12:52:20+03	t
5	Alex	Alex	2025-07-27 12:52:58+03	t
\.


--
-- Data for Name: users_customuser; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_customuser (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, role, phone) FROM stdin;
2	pbkdf2_sha256$870000$05YenSgh1fwSScUZWkybxC$CkyXesq/K8VcKRJ5qj81rprWgms+vOtUu/lT2PhmGek=	\N	f	mohamed_tarek			mohamed.tarek@misrlifetakaful.com	f	t	2025-07-27 12:32:54+03	admin	\N
1	pbkdf2_sha256$1000000$8YcH9AdXg2vypvuEoQKJJL$TSjx6iMNGHIqfORzFuNCyZc4cwwKt5qyk1DgBvx0Mcs=	2025-07-28 12:43:30.003316+03	t	hossam				t	t	2025-07-22 12:04:32.735891+03	user	\N
\.


--
-- Data for Name: assets_employee; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.assets_employee (id, name, department, title, email, creation_date, branch_id, created_by_id) FROM stdin;
406	Ahmed Hegazy	Unknown	Unknown	Ahmed.Hegazy@misrlifetakaful.com	2025-07-27 14:03:10.066721+03	2	1
409	IT Data Center	IT	IT data center	IT@a.com	2025-07-27 16:46:55.727951+03	2	1
336	Ahmed Samy	IT	Head of IT	Ahmed.Samy@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
407	IT Room Maadi	IT	IT room	itroom@abc.com	2025-07-27 15:21:50.785535+03	3	2
351	John Sawarsn	Agency	Upper Egypt Agency Team leader	John.Sawarsn@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	4	1
1	AbdelRahman ElShafie	Actuarial	Actuarial Manager	AbdelRahman.ElShafie@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	1
331	﻿Abeer Saleh	EXCOM	Managing Director & Board Member	Abeer.Saleh@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
332	Ahmed Abdelrehim	Agency Sales	Agency Sales Team Leader -Upper Egypt	Ahmed.Abdelrehim@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	4	\N
333	Ahmed ElSherbiny	Corporate operations	Corporate operations Supervisor	Ahmed.ElSherbiny@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
334	Ahmed Hanafi	Administration	Administration Specialist	Ahmed.Hanafi@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
335	Ahmed Rady	IT	Senior Appliction Support	Ahmed.Rady@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
337	Areej Elsayed	Agency Sales	Trainee	Areej.Elsayed@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	3	\N
338	Dina Wagdi	Finance	Finance assistant Manager	Dina.Wagdi@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
339	Enas Tawheed	Claims	Claims Assessor	Enas.Tawheed@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
340	Esraa Hassanein	Retail Sales 	Retail Sales Team Leader – Upper Egypt	Esraa.Hassanein@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	4	\N
341	Ghada Abdalla	Compliance & Legal	Compliance & Legal Manager	Ghada.Abdalla@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
342	Hagar Mohamed	Training -Sales	Senior Trainer	Hagar.Mohamed@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
343	Hanna Hamdy	Sales Support	Agency Sales Team Leader -Upper Egypt	Hanna.Hamdy@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	4	\N
344	Hany Naan	Agency Sales	Agency Sales Team Leader -Upper Egypt	Hany.Naan@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	4	\N
345	Heba Ashraf	Billing & Collection	Billing & Collection Assistant Manager	Heba.Ashraf@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
346	Hedaya Ashraf	Retail Sales 	Retail Sales Agent	Hedaya.Ashraf@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	3	\N
347	Hesham Mohamed	Administration	Administration Manager	Hesham.Mohamed@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
348	Hossam Alakwah	IT	Application support 	Hossam.Alakwah@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
349	Islam Gamal	Retail Sales	Retail Brokers Account Manager	islam.gamal@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
350	IT Device	None	None	IT.Device@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
352	Kareem Aboelkheir	Retail Operations & Underwriting	Head Of Retail Operations & Underwriting	Kareem.Aboelkheir@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
353	Karim Abdelwahab	Commercial	Head Of Sales	Karim.abdelwahab@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
354	Maged Gamil	Training -Sales	Senior Trainer	Maged.Gamil@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	3	\N
355	Mahmoud  Tawilla	Corporate Brokers	Corporate Brokers Unit Manager	Mahmoud.Tawilla@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
356	Mahmoud ElSherif	Sales	Corporate Sales Director	Mahmoud.ElSherif@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
357	Mahmoud Hefnawy	Corporate Operations and Underwriting 	Head of Corporate Operations and Underwriting 	Mahmoud.Hefnawy@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
358	Mahmoud Thabet	IT	Network & Infrastructure Engineer	Mahmoud.Thabet@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
359	Mai Rasheed	Agency Sales - Cairo	Cairo Agency Manager	Mai.Rasheed@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	3	\N
360	Mai Sarhan	Retail Sales	Retail Sales Agent	Mai.Sarhan@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	3	\N
361	Mary Adel	MD Offfice	Receptionist	Mary.Adel@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
362	Menna Farouk	Agency Sales	Agency Sales Manager - Cairo	Menna.Farouk@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
363	Michael Fam	Agency Sales - Upper Egypt	Upper Egypt Agency Team leader	Michael.Fam@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	4	\N
364	Mina Hanna	Project Management	PMO Head	Mina.Hanna@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
365	Mina Zaki	Claims	Claims Head	Mina.Zaki@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
366	Mohamed Adel	Corporate Operations	Corporate Operations Manager	mohamed.adel@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
367	Mohamed Elserty	Finance	Senior Accountant	Mohamed.Elserty@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
368	Mohamed Nabil	Corporate Sales Direct	Senior Corporate Direct Account Manager	Mohamed.Nabil@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
369	Mohamed Tarek	IT	IT Specialist	Mohamed.Tarek@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
370	Monica Ghaly	HR	Head Of HR	Monica.Ghaly@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
371	Muhammed Amer	Finance	Financial Planning & Analysis Manager	Muhammed.Amer@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
372	Nada Essam	Retail Operations	Branch Coordinator	Nada.Essam@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
373	Nardin Nabil	Agency sales	Trainee	Nardin.Nabil@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	3	\N
374	Nayera hassan	Actuarial	Senior Actuary	Nayera.hassan@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
376	Nermeen Youssef	Training -Sales	Training Senior Manager	Nermeen.Youssef@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	3	\N
377	Nermine yehia	Management	Managing director Office Manager	Nermine.yehia@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
378	Nesrine Mohamed	Sales	Sales Coordinator	Nesrine.Mohamed@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	3	\N
379	Nevine Onsy	Agency Sales	Agency Team Leader - Cairo	Nevine.Onsy@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	3	\N
380	Omar Mamdouh	Corporates Sales Direct	Corporate Direct Account Manager	Omar.Mamdouh@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
381	Omar Mohamed	Sales Support	Sales Support supervisor	Omar.Mohamed@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
382	Omar Othman	Corporates Sales Brokers	Corporate Brokers Sr Account Manager	Omar.Othman@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
383	Peter Amin	Agency Sales - Upper Egypt	Agency Manager Assuit	Peter.Amin@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	4	\N
384	Ragab Gaber	HR	Human Resources Generalist	Ragab.Gaber@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
385	Ramy Youssef	Finance	CFO	ramy.youssef@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
386	Ramzy Raafat	Retail Underwriting	Retail Underwriting Supervisor	Ramzy.Raafat@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
387	Rana Saher	Reinsurance	Retail Underwriting Supervisor	Rana.saher@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
388	Rania El Kady	Retail Operations	Issuance Supervisor	Rania.ElKady@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
389	Rany El-Melehy	Retail Sales	Retail Sales Agent	Rany.El-Melehy@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	3	\N
390	Rasha Khallaf	Information Technology	IT Consultant	Rasha.Khallaf@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
391	Riham Refaat	Retail Sales	Retail Sales Agent	Riham.Refaat@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	3	\N
392	Saad Adel	Agency	Regional Agency Manager Alex & Delta	Saad.Adel@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	5	\N
393	Samar Samy	Corporates Sales Brokers	Corporate Brokers Account Manager	Samar.Samy@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
394	Sayed Allam	Agency Sales	Agency Sales Manager - Cairo	Sayed.Allam@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	3	\N
395	Shady Gamal	Corporates Sales Direct	Corporate Direct sales Unit Manager	Shady.Gamal@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
396	Shaimaa Ali	Corporate Operation	Corporate Underwriting Manager	Shaimaa.Ali@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
397	Tarek Salah	Information Technology	None	tarek.salah@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
398	Tasneem Mohamed	Retail Operations	Sr Issuance Specialist	Tasneem.Mohamed@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
399	Wesam Elwakeel	Marketing & Sales Support	Head of Marketing & Sales Support	wesam.elwakeel@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
400	Yara Morsy	Claims	Senior Claims Assessor	Yara.Morsy@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
401	Yasmin Aly	Retail Sales 	Retail Sales Agent	Yasmin.Aly@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	3	\N
402	Yomna Essam	HR 	Sr Human Resources Specialist	Yomna.Essam@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
403	Youssef Yasser	Agency Sales	Agency Team Leader - Cairo	Youssef.Yasser@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
404	Youstina Mufid	HR	Receptionist	Youstina.Mufid@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
405	Ziad Tarek	Claim	Claim Assessor	Ziad.Tarek@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
375	Nermeen Hossam	Corporate Operations & Underwriting	Head Of Corporate Operations & Underwriting	Nermeen.Hossam@misrlifetakaful.com	2025-07-27 12:42:06.372821+03	2	\N
408	IT Room Assuit	IT	IT room	itroom@abcd.com	2025-07-27 15:23:07.599817+03	4	2
\.


--
-- Data for Name: assets_asset; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.assets_asset (id, product, serial, cpu, cpu_generation, ram, status, warranty, on_hand_date, return_date, comments, type, created_at, updated_at, created_by_id, branch_id, employee_name_id) FROM stdin;
1	PROBOOK 450 G8	5CD147KZ4T	\N	\N	\N	In Use	\N	\N	\N	Used as IT main laptop	Laptop	2025-07-27 00:00:00+03	2025-07-28 11:23:27.077439+03	2	2	397
3	PROBOOK 450 G8	5CD147KZ4N	\N	\N	\N	In Use	2023-06-04	2022-06-06	\N	SCREEN	Laptop	2025-07-27 00:00:00+03	2025-07-28 11:24:03.038752+03	2	2	352
2	PROBOOK 450 G8	5CD147KZ35	\N	\N	\N	In Use	2023-06-04	2022-06-06	\N	Screen & Keyboard kit	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	347
4	PROBOOK 450 G8	5CD147KZ31	\N	\N	\N	Stock	2023-06-04	\N	2024-12-26	Notes: 'Working, Has been Hit by AmmerScreen & Keyboard kit	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
5	PROBOOK 450 G8	5CD147KZ4V	\N	\N	\N	Stock	2023-06-18	\N	2024-12-26	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
6	PROBOOK 450 G8	5CD147KZ4Y	\N	\N	\N	In Use	2023-06-04	2022-07-24	\N	Notes: 'Maryam Abbas مريم عباس محمد Screen & 	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	338
7	PROBOOK 450 G8	5CD147KZ3Y	\N	\N	\N	In Use	2023-06-04	2022-01-07	\N	Screen & Keyboard kit	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	353
8	PROBOOK 450 G8	5CD147KZ48	\N	\N	\N	In Use	2023-06-04	2022-03-07	\N	Screen & Keyboard kit	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	365
9	PROBOOK 450 G8	5CD147KZ3N	\N	\N	\N	Stock	2023-06-04	\N	2025-07-21	Screen & Keyboard kit	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
94	DELL i5-12Th 	8X7NFV3	\N	\N	\N	Stock	2025-07-14	\N	\N	\N	Desktop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
10	PROBOOK 450 G8	5CD147KZ33	\N	\N	\N	In Use	2023-06-04	2022-06-26	\N	Screen & Keyboard kit	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	385
11	PROBOOK 450 G8	5CD147KZ55	\N	\N	\N	In Use	2023-06-04	2025-07-22	2025-07-22	laptop with nermeen youssef Screen & Keyboard kit 	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	370
12	PROBOOK 450 G8	5CD147KZ2H	\N	\N	\N	In Use	2023-06-04	2022-07-18	\N	Screen & Keyboard kit	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	399
13	PROBOOK 450 G8	5CD147KZ42	\N	\N	\N	In Use	2023-09-03	2022-04-09	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	364
14	PROBOOK 450 G8	5CD147KZ3B	\N	\N	\N	In Use	2023-08-30	2022-10-30	\N	Screen & Keyboard kit	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	341
15	PROBOOK 450 G8	5CD147KZ4L	\N	\N	\N	In Use	2024-03-14	2023-03-16	\N	Notes: 'Maryam Abbas مريم عباس محمد Screen & 	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	377
16	PROBOOK 450 G8	5CD147KZ54	\N	\N	\N	In Use	2024-03-14	2025-07-21	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	387
17	PROBOOK 450 G8	5CD147KZ40	\N	\N	\N	In Use	2023-06-04	2024-11-01	\N	Screen & Keyboard kit	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	1
18	PROBOOK 450 G9	5CD248D4VT	\N	\N	\N	In Use	2024-11-18	2025-06-16	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	404
19	PROBOOK 450 G9	5CD248D4WF	\N	\N	\N	In Use	2025-01-08	2024-09-01	\N	Screen & Keyboard kit\nPreviously was with Jailan Salah	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	333
20	PROBOOK 450 G9	5CD248D4WV	\N	\N	\N	In Use	2025-01-30	2024-01-02	\N	Screen 	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	396
21	PROBOOK 450 G9	5CD248D4VS	\N	\N	\N	In Use	2025-01-30	2024-03-03	\N	Screen24 & Keyboard kit	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	345
22	PROBOOK 450 G9	5CD248D4X5	\N	\N	\N	In Use	2024-01-30	2024-03-18	\N	Screen 24& Keyboard kit	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	398
23	PROBOOK 450 G9	5CD248D4WL	\N	\N	\N	In Use	2024-01-30	\N	\N	Screen & Keyboard kit	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	386
24	PROBOOK 450 G9	5CD248D4WN	\N	\N	\N	In Use	2024-01-30	2024-04-04	\N	Screen & Keyboard kit	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	400
25	PROBOOK 450 G9	5CD248D4WX	\N	\N	\N	In Use	2024-01-30	2024-07-04	\N	Screen& Keyboard kit	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	3	376
26	PROBOOK 450 G9	5CD248D4VG	\N	\N	\N	In Use	2024-01-30	2024-05-15	\N	replacement for his old one as it is under fixing	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	366
27	PROBOOK 450 G9	5CD248D4VN	\N	\N	\N	In Use	2024-01-30	2024-06-02	\N	Screen24	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	348
28	PROBOOK 450 G9	5CD248D4X3	\N	\N	\N	In Use	2024-01-30	2024-06-02	\N	Screen24	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	381
29	PROBOOK 450 G9 I5-12th	5CD248D4X7	\N	\N	\N	Stock	2024-01-30	\N	2025-07-22	outsource service desk	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
30	PROBOOK 450 G9 I5-12th	5CD248D4VZ	\N	\N	\N	In Use	2024-01-30	2024-07-01	\N	Screen 24	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	335
31	PROBOOK 450 G9 I5-12th	5CD248D4VD	\N	\N	\N	In Use	2024-01-30	2025-01-02	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	342
32	PROBOOK 450 G9 I5-12th	5CD248D4W2	\N	\N	\N	In Use	2024-01-30	2024-05-01	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	349
33	PROBOOK 450 G9 I5-12th	5CD248D4WC	\N	\N	\N	In Use	2024-01-30	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	338
34	PROBOOK 450 G9 I5-12th	5CD248D4VK	\N	\N	\N	In Use	2024-01-30	2024-06-23	\N	Screen24	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	374
35	PROBOOK 450 G9 I5-12th	5CD248D4VC	\N	\N	\N	In Use	2024-01-30	2024-07-02	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	4	383
36	PROBOOK 450 G9 I5-12th	5CD248D4V5	\N	\N	\N	In Use	2024-01-30	2024-07-02	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	361
37	PROBOOK 450 G9 I5-12th	5CD248D4X8	\N	\N	\N	Stock	2024-01-30	\N	2025-05-05	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
38	PROBOOK 450 G8 I7-12th	5CD147KZ2J	\N	\N	\N	Stock	2023-06-05	\N	2024-07-01	It was wz Mohamed Adel and got power issue but after a while it worked fine so we format it and it is in IT Store	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
39	PROBOOK 450 G8 I5-12th	5CD248D4WW	\N	\N	\N	In Use	2024-01-30	2023-02-11	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	380
40	PROBOOK 450 G8 I5-12th	5CD248D4VB	\N	\N	\N	In Use	2024-01-30	2024-02-09	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	382
41	PROBOOK 450 G8 I5-12th	5CD248D4V8	\N	\N	\N	In Use	2024-01-30	2025-07-15	\N	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	405
42	PROBOOK 450 G8 I5-12th	5CD248D4WK	\N	\N	\N	In Use	2024-01-30	2024-10-09	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	4	351
43	PROBOOK 450 G8 I5-12th	5CD248D4X6	\N	\N	\N	In Use	2024-01-30	2024-10-09	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	4	363
44	PROBOOK 450 G8 I5-12th	5CD248D4WM	\N	\N	\N	In Use	2024-01-30	2024-09-16	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	3	359
45	PROBOOK 450 G10 I7-13th	1H84160DF5	\N	\N	\N	In Use	2025-09-17	2024-09-22	\N	Screen27 & Keyboard kit	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	336
46	PROBOOK 450 G8 I5-12th	5CD248D4WQ	\N	\N	\N	In Use	2024-01-30	2025-03-01	\N	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	339
47	PROBOOK 450 G8 I5-12th	5CD248D4X1	\N	\N	\N	In Use	2024-01-30	2025-01-05	\N	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	3	354
48	PC Dell I5-12th 	5X7NFV3	\N	\N	\N	Stock	2025-07-04	\N	2025-04-22	SCREEN	Desktop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
49	PROBOOK 450 G8 I5-12th	5CD248D4X4	\N	\N	\N	In Use	2024-01-30	2024-10-15	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	367
50	PROBOOK 450 G8	5CD147KZ3L	\N	\N	\N	Damage	2024-02-19	\N	2022-10-30	Died	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
51	PROBOOK 450 G8	5CD147KZ3C	\N	\N	\N	Damage	2023-08-30	\N	2024-01-11	screen	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
52	PROBOOK 450 G10 I7-13th	1H84160DDJ	\N	\N	\N	Stock	2025-08-31	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
53	PROBOOK 450 G10 I5-13th	1H8416096J	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
54	PROBOOK 450 G10 I5-13th	1H8416096V	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
55	PROBOOK 450 G10 I5-13th	1H84160976	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
56	PROBOOK 450 G10 I5-13th	1H8416097C	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
57	PROBOOK 450 G10 I5-13th	1H8416097Q	\N	\N	\N	In Use	2025-09-02	2025-04-15	\N	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	388
58	PROBOOK 450 G10 I5-13th	1H84160982	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
59	PROBOOK 450 G10 I5-13th	1H8416098G	\N	\N	\N	Stock	2025-09-02	\N	2025-07-09	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
60	PROBOOK 450 G10 I5-13th	1H8416098Y	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
61	PROBOOK 450 G10 I5-13th	1H84160995	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
62	PROBOOK 450 G10 I5-13th	1H84160966	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
63	PROBOOK 450 G10 I5-13th	1H8416096L	\N	\N	\N	In Use	2025-09-02	2025-07-10	\N	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	352
64	PROBOOK 450 G10 I5-13th	1H8416096Z	\N	\N	\N	In Use	2025-09-02	2025-04-17	\N	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	334
65	PROBOOK 450 G10 I5-13th	1H84160977	\N	\N	\N	In Use	2025-09-02	2025-01-15	\N	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	4	332
66	PROBOOK 450 G10 I5-13th	1H8416097D	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
67	PROBOOK 450 G10 I5-13th	1H8416097V	\N	\N	\N	In Use	2025-09-02	2024-12-01	\N	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	3	394
68	PROBOOK 450 G10 I5-13th	1H84160987	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
69	PROBOOK 450 G10 I5-13th	1H8416098H	\N	\N	\N	In Use	2025-09-02	2025-06-01	\N	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	384
70	PROBOOK 450 G10 I5-13th	1H8416098Z	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
71	PROBOOK 450 G10 I5-13th	1H8416099B	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
72	PROBOOK 450 G10 I5-13th	1H84160969	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
73	PROBOOK 450 G10 I5-13th	1H8416096Q	\N	\N	\N	Stock	2025-09-02	\N	2025-06-01	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
74	PROBOOK 450 G10 I5-13th	1H84160971	\N	\N	\N	In Use	2025-09-02	2025-01-15	\N	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	3	343
75	PROBOOK 450 G10 I5-13th	1H84160978	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
76	PROBOOK 450 G10 I5-13th	1H8416097F	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
77	PROBOOK 450 G10 I5-13th	1H8416097W	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
78	PROBOOK 450 G10 I5-13th	1H84160989	\N	\N	\N	In Use	2025-09-02	2025-01-15	\N	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	4	344
79	PROBOOK 450 G10 I5-13th	1H8416098P	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
80	PROBOOK 450 G10 I5-13th	1H84160991	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
81	PROBOOK 450 G10 I5-13th	1H84160974	\N	\N	\N	In Use	2025-09-02	2024-11-03	\N	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	3	379
82	PROBOOK 450 G10 I5-13th	1H8416096H	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
83	PROBOOK 450 G10 I5-13th	1H8416096R	\N	\N	\N	In Use	2025-09-02	2025-07-22	2025-07-22	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	3	379
84	PROBOOK 450 G10 I5-13th	1H84160975	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
85	PROBOOK 450 G10 I5-13th	1H84160979	\N	\N	\N	In Use	2025-09-02	2025-06-01	\N	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	4	340
86	PROBOOK 450 G10 I5-13th	1H8416097H	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
87	PROBOOK 450 G10 I5-13th	1H8416097Y	\N	\N	\N	In Use	2025-09-02	2024-12-11	\N	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	358
88	PROBOOK 450 G10 I5-13th	1H8416098F	\N	\N	\N	In Use	2025-09-02	2025-03-02	\N	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	3	378
89	PROBOOK 450 G10 I5-13th	1H8416098R	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
90	PROBOOK 450 G10 I5-13th	1H84160994	\N	\N	\N	In Use	2025-09-02	2025-07-01	\N	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	357
91	PROBOOK 450 G10 I5-13th	1H84160984	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
92	PROBOOK 450 G10 I5-13th	1H84160965	\N	\N	\N	Stock	2025-09-02	\N	\N	\N	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
93	PROBOOK 450 G10 I5-12th	5CD248D4WP	\N	\N	\N	In Use	2024-01-30	2025-02-25	2025-06-25	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	5	392
95	DELL i5-12Th 	8H6NFV3	\N	\N	\N	In Use	2025-07-14	2024-12-02	\N	None	Desktop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	372
96	DELL i5-12Th 	557NFV3	\N	\N	\N	Stock	2025-07-14	\N	\N	\N	Desktop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
97	DELL i5-12Th 	147NFV3	\N	\N	\N	In Use	2025-07-14	2025-07-22	2025-07-22	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	3	407
98	DELL i5-12Th 	GF7NFV3	\N	\N	\N	Stock	2025-07-14	\N	2025-07-22	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	1	\N
99	HP ENVY x360 Convert	CND142386H	\N	\N	\N	In Use	2023-07-19	2022-07-07	\N	None	Laptop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	2	331
100	Dell OptiPlex Tower 7020	BMTP184	\N	\N	\N	In Use	2026-04-29	2025-07-22	2025-07-22	it room assuit	Desktop	2025-07-27 00:00:00+03	2025-07-27 00:00:00+03	2	4	408
\.


--
-- Data for Name: assets_assetlog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.assets_assetlog (id, old_status, new_status, on_hand_date, return_date, change_time, asset_id, changed_by_id, branch_id, new_employee_id, old_employee_id) FROM stdin;
207	\N	Stock	\N	\N	2024-11-14 00:00:00+02	1	2	1	\N	\N
208	\N	Stock	\N	\N	2024-11-14 00:00:00+02	2	2	1	\N	\N
209	\N	Stock	\N	\N	2024-11-14 00:00:00+02	3	2	1	\N	\N
210	\N	Stock	\N	\N	2024-11-14 00:00:00+02	4	2	1	\N	\N
211	\N	Stock	\N	\N	2024-11-14 00:00:00+02	5	2	1	\N	\N
212	\N	Stock	\N	\N	2024-11-14 00:00:00+02	6	2	1	\N	\N
213	\N	Stock	\N	\N	2024-11-14 00:00:00+02	7	2	1	\N	\N
214	\N	Stock	\N	\N	2024-11-14 00:00:00+02	8	2	1	\N	\N
215	\N	Stock	\N	\N	2024-11-14 00:00:00+02	9	2	1	\N	\N
216	\N	Stock	\N	\N	2024-11-14 00:00:00+02	10	2	1	\N	\N
217	\N	Stock	\N	\N	2024-11-14 00:00:00+02	11	2	1	\N	\N
218	\N	Stock	\N	\N	2024-11-14 00:00:00+02	12	2	1	\N	\N
219	\N	Stock	\N	\N	2024-11-14 00:00:00+02	13	2	1	\N	\N
220	\N	Stock	\N	\N	2024-11-14 00:00:00+02	14	2	1	\N	\N
221	\N	Stock	\N	\N	2024-11-14 00:00:00+02	15	2	1	\N	\N
222	\N	Stock	\N	\N	2024-11-14 00:00:00+02	16	2	1	\N	\N
223	\N	Stock	\N	\N	2024-11-14 00:00:00+02	17	2	1	\N	\N
224	\N	Stock	\N	\N	2024-11-14 00:00:00+02	18	2	1	\N	\N
225	\N	Stock	\N	\N	2024-11-14 00:00:00+02	19	2	1	\N	\N
226	\N	Stock	\N	\N	2024-11-14 00:00:00+02	20	2	1	\N	\N
227	\N	Stock	\N	\N	2024-11-14 00:00:00+02	21	2	1	\N	\N
228	\N	Stock	\N	\N	2024-11-14 00:00:00+02	22	2	1	\N	\N
229	\N	Stock	\N	\N	2024-11-14 00:00:00+02	23	2	1	\N	\N
230	\N	Stock	\N	\N	2024-11-14 00:00:00+02	24	2	1	\N	\N
231	\N	Stock	\N	\N	2024-11-14 00:00:00+02	25	2	1	\N	\N
232	\N	Stock	\N	\N	2024-11-14 00:00:00+02	26	2	1	\N	\N
233	\N	Stock	\N	\N	2024-11-14 00:00:00+02	27	2	1	\N	\N
234	\N	Stock	\N	\N	2024-11-14 00:00:00+02	28	2	1	\N	\N
235	\N	Stock	\N	\N	2024-11-14 00:00:00+02	29	2	1	\N	\N
236	\N	Stock	\N	\N	2024-11-14 00:00:00+02	30	2	1	\N	\N
237	\N	Stock	\N	\N	2024-11-14 00:00:00+02	31	2	1	\N	\N
238	\N	Stock	\N	\N	2024-11-14 00:00:00+02	32	2	1	\N	\N
239	\N	Stock	\N	\N	2024-11-14 00:00:00+02	33	2	1	\N	\N
240	\N	Stock	\N	\N	2024-11-14 00:00:00+02	34	2	1	\N	\N
241	\N	Stock	\N	\N	2024-11-14 00:00:00+02	35	2	1	\N	\N
242	\N	Stock	\N	\N	2024-11-14 00:00:00+02	36	2	1	\N	\N
243	\N	Stock	\N	\N	2024-11-14 00:00:00+02	37	2	1	\N	\N
244	\N	Stock	\N	\N	2024-11-14 00:00:00+02	38	2	1	\N	\N
245	\N	Stock	\N	\N	2024-11-14 00:00:00+02	39	2	1	\N	\N
246	\N	Stock	\N	\N	2024-11-14 00:00:00+02	40	2	1	\N	\N
247	\N	Stock	\N	\N	2024-11-14 00:00:00+02	41	2	1	\N	\N
248	\N	Stock	\N	\N	2024-11-14 00:00:00+02	42	2	1	\N	\N
249	\N	Stock	\N	\N	2024-11-14 00:00:00+02	43	2	1	\N	\N
250	\N	Stock	\N	\N	2024-11-14 00:00:00+02	44	2	1	\N	\N
251	\N	Stock	\N	\N	2024-11-14 00:00:00+02	45	2	1	\N	\N
252	\N	Stock	\N	\N	2024-11-14 00:00:00+02	46	2	1	\N	\N
253	\N	Stock	\N	\N	2024-11-14 00:00:00+02	47	2	1	\N	\N
254	\N	Stock	\N	\N	2024-11-14 00:00:00+02	48	2	1	\N	\N
255	\N	Stock	\N	\N	2024-11-14 00:00:00+02	49	2	1	\N	\N
256	\N	Stock	\N	\N	2024-11-14 00:00:00+02	50	2	1	\N	\N
257	\N	Stock	\N	\N	2024-11-14 00:00:00+02	51	2	1	\N	\N
258	\N	Stock	\N	\N	2024-11-14 00:00:00+02	52	2	1	\N	\N
259	\N	Stock	\N	\N	2024-11-14 00:00:00+02	53	2	1	\N	\N
260	\N	Stock	\N	\N	2024-11-14 00:00:00+02	54	2	1	\N	\N
261	\N	Stock	\N	\N	2024-11-14 00:00:00+02	55	2	1	\N	\N
262	\N	Stock	\N	\N	2024-11-14 00:00:00+02	56	2	1	\N	\N
263	\N	Stock	\N	\N	2024-11-14 00:00:00+02	57	2	1	\N	\N
264	\N	Stock	\N	\N	2024-11-14 00:00:00+02	58	2	1	\N	\N
265	\N	Stock	\N	\N	2024-11-14 00:00:00+02	59	2	1	\N	\N
266	\N	Stock	\N	\N	2024-11-14 00:00:00+02	60	2	1	\N	\N
267	\N	Stock	\N	\N	2024-11-14 00:00:00+02	61	2	1	\N	\N
268	\N	Stock	\N	\N	2024-11-14 00:00:00+02	62	2	1	\N	\N
269	\N	Stock	\N	\N	2024-11-14 00:00:00+02	63	2	1	\N	\N
270	\N	Stock	\N	\N	2024-11-14 00:00:00+02	64	2	1	\N	\N
271	\N	Stock	\N	\N	2024-11-14 00:00:00+02	65	2	1	\N	\N
272	\N	Stock	\N	\N	2024-11-14 00:00:00+02	66	2	1	\N	\N
273	\N	Stock	\N	\N	2024-11-14 00:00:00+02	67	2	1	\N	\N
274	\N	Stock	\N	\N	2024-11-14 00:00:00+02	68	2	1	\N	\N
275	\N	Stock	\N	\N	2024-11-14 00:00:00+02	69	2	1	\N	\N
276	\N	Stock	\N	\N	2024-11-14 00:00:00+02	70	2	1	\N	\N
277	\N	Stock	\N	\N	2024-11-14 00:00:00+02	71	2	1	\N	\N
278	\N	Stock	\N	\N	2024-11-14 00:00:00+02	72	2	1	\N	\N
279	\N	Stock	\N	\N	2024-11-14 00:00:00+02	73	2	1	\N	\N
280	\N	Stock	\N	\N	2024-11-14 00:00:00+02	74	2	1	\N	\N
281	\N	Stock	\N	\N	2024-11-14 00:00:00+02	75	2	1	\N	\N
282	\N	Stock	\N	\N	2024-11-14 00:00:00+02	76	2	1	\N	\N
283	\N	Stock	\N	\N	2024-11-14 00:00:00+02	77	2	1	\N	\N
284	\N	Stock	\N	\N	2024-11-14 00:00:00+02	78	2	1	\N	\N
285	\N	Stock	\N	\N	2024-11-14 00:00:00+02	79	2	1	\N	\N
286	\N	Stock	\N	\N	2024-11-14 00:00:00+02	80	2	1	\N	\N
287	\N	Stock	\N	\N	2024-11-14 00:00:00+02	81	2	1	\N	\N
288	\N	Stock	\N	\N	2024-11-14 00:00:00+02	82	2	1	\N	\N
289	\N	Stock	\N	\N	2024-11-14 00:00:00+02	83	2	1	\N	\N
290	\N	Stock	\N	\N	2024-11-14 00:00:00+02	84	2	1	\N	\N
291	\N	Stock	\N	\N	2024-11-14 00:00:00+02	85	2	1	\N	\N
292	\N	Stock	\N	\N	2024-11-14 00:00:00+02	86	2	1	\N	\N
293	\N	Stock	\N	\N	2024-11-14 00:00:00+02	87	2	1	\N	\N
294	\N	Stock	\N	\N	2024-11-14 00:00:00+02	88	2	1	\N	\N
295	\N	Stock	\N	\N	2024-11-14 00:00:00+02	89	2	1	\N	\N
296	\N	Stock	\N	\N	2024-11-14 00:00:00+02	90	2	1	\N	\N
297	\N	Stock	\N	\N	2024-11-14 00:00:00+02	91	2	1	\N	\N
298	\N	Stock	\N	\N	2024-11-14 00:00:00+02	92	2	1	\N	\N
299	\N	Stock	\N	\N	2024-11-14 00:00:00+02	93	2	1	\N	\N
300	\N	Stock	\N	\N	2024-11-14 00:00:00+02	94	2	1	\N	\N
301	\N	Stock	\N	\N	2024-11-14 00:00:00+02	95	2	1	\N	\N
302	\N	Stock	\N	\N	2024-11-14 00:00:00+02	96	2	1	\N	\N
303	\N	Stock	\N	\N	2024-11-14 00:00:00+02	97	2	1	\N	\N
304	\N	Stock	\N	\N	2024-11-14 00:00:00+02	98	2	1	\N	\N
305	Stock	In Use	\N	\N	2024-11-14 00:00:00+02	1	2	\N	397	\N
306	Stock	In Use	2022-06-06	\N	2024-11-14 00:00:00+02	2	2	\N	347	\N
307	Stock	In Use	2022-06-06	\N	2024-11-14 00:00:00+02	3	2	\N	352	\N
308	Stock	In Use	2022-07-17	\N	2024-11-14 00:00:00+02	4	2	\N	371	\N
309	Stock	In Use	\N	\N	2024-11-14 00:00:00+02	5	2	\N	355	\N
310	Stock	In Use	2022-07-24	\N	2024-11-14 00:00:00+02	6	2	\N	338	\N
311	Stock	In Use	2022-01-07	\N	2024-11-14 00:00:00+02	7	2	\N	353	\N
312	Stock	In Use	2022-03-07	\N	2024-11-14 00:00:00+02	8	2	\N	365	\N
313	Stock	In Use	2022-04-07	\N	2024-11-14 00:00:00+02	9	2	\N	387	\N
314	Stock	In Use	2022-06-26	\N	2024-11-14 00:00:00+02	10	2	\N	385	\N
315	Stock	In Use	2022-07-19	\N	2024-11-14 00:00:00+02	11	2	\N	370	\N
316	Stock	In Use	2022-07-18	\N	2024-11-14 00:00:00+02	12	2	\N	399	\N
317	Stock	In Use	2022-04-09	\N	2024-11-14 00:00:00+02	13	2	\N	364	\N
318	Stock	In Use	2022-10-30	\N	2024-11-14 00:00:00+02	14	2	\N	341	\N
319	Stock	In Use	2023-03-16	\N	2024-11-14 00:00:00+02	15	2	\N	377	\N
320	Stock	In Use	2023-03-16	\N	2024-11-14 00:00:00+02	16	2	\N	406	\N
321	Stock	In Use	2024-11-01	\N	2024-11-14 00:00:00+02	17	2	\N	1	\N
322	Stock	In Use	2023-11-21	\N	2024-11-14 00:00:00+02	18	2	\N	377	\N
323	Stock	In Use	2024-09-01	\N	2024-11-14 00:00:00+02	19	2	\N	333	\N
324	Stock	In Use	2024-01-02	\N	2024-11-14 00:00:00+02	20	2	\N	396	\N
325	Stock	In Use	2024-03-03	\N	2024-11-14 00:00:00+02	21	2	\N	345	\N
326	Stock	In Use	2024-03-18	\N	2024-11-14 00:00:00+02	22	2	\N	398	\N
327	Stock	In Use	\N	\N	2024-11-14 00:00:00+02	23	2	\N	386	\N
328	Stock	In Use	2024-04-04	\N	2024-11-14 00:00:00+02	24	2	\N	400	\N
329	Stock	In Use	2024-07-04	\N	2024-11-14 00:00:00+02	25	2	\N	376	\N
330	Stock	In Use	2024-05-15	\N	2024-11-14 00:00:00+02	26	2	\N	366	\N
331	Stock	In Use	2024-06-02	\N	2024-11-14 00:00:00+02	27	2	\N	348	\N
332	Stock	In Use	2024-06-02	\N	2024-11-14 00:00:00+02	28	2	\N	381	\N
333	Stock	In Use	2024-06-10	\N	2024-11-14 00:00:00+02	29	2	\N	369	\N
334	Stock	In Use	2024-07-01	\N	2024-11-14 00:00:00+02	30	2	\N	335	\N
335	Stock	In Use	2024-05-01	\N	2024-11-14 00:00:00+02	31	2	\N	334	\N
336	Stock	In Use	2024-05-01	\N	2024-11-14 00:00:00+02	32	2	\N	349	\N
337	Stock	In Use	\N	\N	2024-11-14 00:00:00+02	33	2	\N	338	\N
338	Stock	In Use	2024-06-23	\N	2024-11-14 00:00:00+02	34	2	\N	374	\N
339	Stock	In Use	2024-07-02	\N	2024-11-14 00:00:00+02	35	2	\N	383	\N
340	Stock	In Use	2024-07-02	\N	2024-11-14 00:00:00+02	36	2	\N	361	\N
341	Stock	In Use	2024-07-07	\N	2024-11-14 00:00:00+02	37	2	\N	395	\N
342	Stock	In Use	2023-02-11	\N	2024-11-14 00:00:00+02	39	2	\N	380	\N
343	Stock	In Use	2024-02-09	\N	2024-11-14 00:00:00+02	40	2	\N	382	\N
344	Stock	In Use	2024-09-08	\N	2024-11-14 00:00:00+02	41	2	\N	402	\N
345	Stock	In Use	2024-10-09	\N	2024-11-14 00:00:00+02	42	2	\N	351	\N
346	Stock	In Use	2024-10-09	\N	2024-11-14 00:00:00+02	43	2	\N	363	\N
347	Stock	In Use	2024-09-16	\N	2024-11-14 00:00:00+02	44	2	\N	359	\N
348	Stock	In Use	2024-09-22	\N	2024-11-14 00:00:00+02	45	2	\N	336	\N
349	Stock	In Use	2024-09-25	\N	2024-11-14 00:00:00+02	46	2	\N	393	\N
350	Stock	In Use	2024-01-10	\N	2024-11-14 00:00:00+02	47	2	\N	368	\N
351	Stock	In Use	2024-06-08	\N	2024-11-14 00:00:00+02	48	2	\N	334	\N
352	Stock	In Use	2024-10-15	\N	2024-11-14 00:00:00+02	49	2	\N	367	\N
353	Stock	In Use	2022-01-09	\N	2024-11-14 00:00:00+02	50	2	\N	341	\N
354	Stock	In Use	2023-01-03	\N	2024-11-14 00:00:00+02	51	2	\N	1	\N
355	In Use	Damage	\N	2022-10-30	2024-11-14 00:00:00+02	50	2	1	\N	341
356	In Use	Damage	\N	2024-01-11	2024-11-14 00:00:00+02	51	2	1	\N	1
357	In Use	Stock	\N	2024-06-27	2024-11-14 00:00:00+02	16	2	1	\N	406
358	In Use	Stock	\N	2024-08-06	2024-11-14 00:00:00+02	31	2	1	\N	334
359	In Use	Stock	\N	2024-07-01	2024-11-14 00:00:00+02	38	2	1	\N	\N
360	Stock	In Use	2024-11-03	\N	2024-11-14 00:00:00+02	81	2	\N	379	\N
361	Stock	In Use	2024-11-03	\N	2024-11-14 00:00:00+02	63	2	\N	403	\N
362	Stock	In Use	2024-11-03	\N	2024-11-14 00:00:00+02	93	2	\N	392	\N
363	Stock	In Use	2024-11-17	\N	2024-11-17 00:00:00+02	87	2	\N	339	\N
364	Stock	In Use	2024-12-01	\N	2024-12-01 00:00:00+02	67	2	\N	394	\N
365	Stock	In Use	2024-12-02	\N	2024-12-02 00:00:00+02	95	2	\N	372	\N
366	In Use	Stock	\N	2024-12-10	2024-12-10 00:00:00+02	87	2	1	\N	339
367	Stock	In Use	2024-12-11	\N	2024-12-10 00:00:00+02	87	2	\N	358	\N
368	Stock	In Use	2024-12-10	\N	2024-12-10 00:00:00+02	98	2	\N	339	\N
369	In Use	Stock	\N	2024-12-22	2024-12-24 00:00:00+02	46	2	1	\N	393
370	In Use	Stock	\N	\N	2024-12-26 00:00:00+02	5	2	1	\N	355
371	In Use	Stock	\N	2024-12-26	2024-12-26 00:00:00+02	4	2	1	\N	371
372	In Use	Stock	\N	2024-12-31	2025-01-14 00:00:00+02	47	2	1	\N	368
373	Stock	In Use	2025-01-05	\N	2025-01-14 00:00:00+02	47	2	\N	354	\N
374	Stock	In Use	2025-01-02	\N	2025-01-14 00:00:00+02	31	2	\N	342	\N
375	Stock	In Use	2025-01-15	\N	2025-01-27 00:00:00+02	73	2	2	362	\N
376	Stock	In Use	2025-01-15	\N	2025-01-27 00:00:00+02	74	2	2	343	\N
377	Stock	In Use	2025-01-15	\N	2025-01-27 00:00:00+02	65	2	2	332	\N
378	Stock	In Use	2024-12-31	\N	2025-01-27 00:00:00+02	97	2	3	407	\N
379	Stock	In Use	2025-01-15	\N	2025-01-27 00:00:00+02	78	2	2	344	\N
380	\N	Stock	\N	\N	2025-01-27 00:00:00+02	99	2	1	\N	\N
381	Stock	In Use	2022-07-07	\N	2025-01-27 00:00:00+02	99	2	2	331	\N
382	Stock	In Use	2025-03-02	\N	2025-03-03 00:00:00+02	88	2	2	378	\N
383	Stock	In Use	2025-04-15	\N	2025-04-15 00:00:00+02	57	2	2	388	\N
384	Stock	In Use	2025-03-01	\N	2025-04-16 00:00:00+02	46	2	2	339	\N
385	Stock	In Use	2025-04-17	\N	2025-04-17 00:00:00+02	64	2	2	334	\N
386	In Use	Stock	\N	2025-04-22	2025-04-22 00:00:00+02	48	2	1	\N	334
387	In Use	Stock	\N	2025-05-05	2025-05-07 00:00:00+03	37	2	1	\N	395
388	Stock	In Use	2025-05-15	\N	2025-05-15 00:00:00+03	59	2	2	379	\N
389	In Use	In Use	2025-05-15	2025-05-15	2025-05-15 00:00:00+03	59	2	2	403	379
390	Stock	In Use	2025-05-15	\N	2025-05-15 00:00:00+03	83	2	2	379	\N
391	In Use	Stock	\N	2025-05-22	2025-05-26 00:00:00+03	18	2	1	\N	375
392	Stock	In Use	2025-06-01	\N	2025-06-01 00:00:00+03	69	2	2	384	\N
393	Stock	In Use	2025-06-01	\N	2025-06-01 00:00:00+03	85	2	2	340	\N
394	In Use	Stock	\N	2025-06-01	2025-06-01 00:00:00+03	73	2	1	\N	362
395	Stock	In Use	2025-06-16	\N	2025-06-16 00:00:00+03	18	2	2	404	\N
396	In Use	Stock	\N	2025-06-22	2025-06-22 00:00:00+03	41	2	1	\N	402
397	In Use	In Use	2025-02-25	2025-06-25	2025-06-25 00:00:00+03	93	2	2	392	392
398	Stock	In Use	2025-07-01	\N	2025-06-30 00:00:00+03	90	2	2	357	\N
399	In Use	Stock	\N	2025-07-09	2025-07-09 00:00:00+03	63	2	1	\N	403
400	In Use	Stock	\N	2025-07-09	2025-07-09 00:00:00+03	59	2	1	\N	403
401	Stock	In Use	2025-07-10	\N	2025-07-10 00:00:00+03	63	2	2	352	\N
402	Stock	In Use	2025-07-15	\N	2025-07-15 00:00:00+03	41	2	2	405	\N
403	Stock	In Use	2025-07-21	\N	2025-07-21 00:00:00+03	16	2	2	387	\N
404	In Use	Stock	\N	2025-07-21	2025-07-21 00:00:00+03	9	2	1	\N	387
405	In Use	Stock	\N	2025-07-22	2025-07-22 00:00:00+03	29	2	1	\N	369
406	In Use	Stock	\N	2025-07-22	2025-07-22 00:00:00+03	98	2	1	\N	339
407	In Use	In Use	2025-07-22	2025-07-22	2025-07-22 00:00:00+03	11	2	2	370	370
408	In Use	In Use	2025-07-22	2025-07-22	2025-07-22 00:00:00+03	83	2	2	379	379
409	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	66	2	1	\N	\N
410	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	67	2	1	\N	\N
411	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	68	2	1	\N	\N
412	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	69	2	1	\N	\N
413	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	70	2	1	\N	\N
414	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	71	2	1	\N	\N
415	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	72	2	1	\N	\N
416	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	73	2	1	\N	\N
417	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	74	2	1	\N	\N
418	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	75	2	1	\N	\N
419	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	76	2	1	\N	\N
420	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	77	2	1	\N	\N
421	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	78	2	1	\N	\N
422	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	79	2	1	\N	\N
423	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	80	2	1	\N	\N
424	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	81	2	1	\N	\N
425	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	82	2	1	\N	\N
426	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	83	2	1	\N	\N
427	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	84	2	1	\N	\N
428	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	85	2	1	\N	\N
429	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	86	2	1	\N	\N
430	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	87	2	1	\N	\N
431	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	88	2	1	\N	\N
432	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	89	2	1	\N	\N
433	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	90	2	1	\N	\N
434	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	91	2	1	\N	\N
435	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	92	2	1	\N	\N
436	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	93	2	1	\N	\N
437	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	94	2	1	\N	\N
438	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	95	2	1	\N	\N
439	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	96	2	1	\N	\N
440	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	97	2	1	\N	\N
441	\N	Stock	\N	2024-11-14	2024-11-14 00:00:00+02	98	2	1	\N	\N
442	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	1	2	2	397	\N
443	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	2	2	2	347	\N
444	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	3	2	2	352	\N
445	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	4	2	1	371	\N
446	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	5	2	1	355	\N
447	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	6	2	2	338	\N
448	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	7	2	2	353	\N
449	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	8	2	2	365	\N
450	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	9	2	1	387	\N
451	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	10	2	2	385	\N
452	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	11	2	2	370	\N
453	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	12	2	2	399	\N
454	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	13	2	2	364	\N
455	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	14	2	2	341	\N
456	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	15	2	2	377	\N
457	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	16	2	2	406	\N
458	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	17	2	2	1	\N
459	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	18	2	2	377	\N
460	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	19	2	2	333	\N
461	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	20	2	2	396	\N
462	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	21	2	2	345	\N
463	Stock	In Use	\N	2024-11-14	2024-11-14 00:00:00+02	22	2	2	398	\N
\.


--
-- Data for Name: assets_reportablemodel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.assets_reportablemodel (id, name, model_path) FROM stdin;
\.


--
-- Data for Name: assets_reportablefield; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.assets_reportablefield (id, field_name, display_name, is_filter, is_visible, field_type, choices, model_id) FROM stdin;
\.


--
-- Data for Name: assets_storagedevice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.assets_storagedevice (id, type, size, asset_id) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	users	customuser
7	assets	branch
8	assets	employee
9	assets	storagedevice
10	assets	asset
11	assets	assetlog
12	assets	reportablefield
13	assets	reportablemodel
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add user	6	add_customuser
22	Can change user	6	change_customuser
23	Can delete user	6	delete_customuser
24	Can view user	6	view_customuser
25	Can add Branch	7	add_branch
26	Can change Branch	7	change_branch
27	Can delete Branch	7	delete_branch
28	Can view Branch	7	view_branch
29	Can add employee	8	add_employee
30	Can change employee	8	change_employee
31	Can delete employee	8	delete_employee
32	Can view employee	8	view_employee
33	Can add storage device	9	add_storagedevice
34	Can change storage device	9	change_storagedevice
35	Can delete storage device	9	delete_storagedevice
36	Can view storage device	9	view_storagedevice
37	Can add Asset	10	add_asset
38	Can change Asset	10	change_asset
39	Can delete Asset	10	delete_asset
40	Can view Asset	10	view_asset
41	Can add Asset Log	11	add_assetlog
42	Can change Asset Log	11	change_assetlog
43	Can delete Asset Log	11	delete_assetlog
44	Can view Asset Log	11	view_assetlog
45	Can add reportable field	12	add_reportablefield
46	Can change reportable field	12	change_reportablefield
47	Can delete reportable field	12	delete_reportablefield
48	Can view reportable field	12	view_reportablefield
49	Can add reportable model	13	add_reportablemodel
50	Can change reportable model	13	change_reportablemodel
51	Can delete reportable model	13	delete_reportablemodel
52	Can view reportable model	13	view_reportablemodel
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2025-07-22 12:33:41.49056+03	1	Head office	1	[{"added": {}}]	7	1
2	2025-07-22 12:35:50.475406+03	2	stock	1	[{"added": {}}]	7	1
3	2025-07-22 12:35:59.771196+03	1	HP450 - 123456	1	[{"added": {}}]	10	1
4	2025-07-22 12:36:33.297128+03	2	stock	2	[]	7	1
5	2025-07-22 12:41:18.6472+03	1	HP450 - 123456	3		10	1
6	2025-07-22 12:42:46.049261+03	2	HP450 - 123456	1	[{"added": {}}]	10	1
7	2025-07-22 12:46:48.815955+03	5	حسن محمد حسن عبدالعزيز الاكوح	3		8	1
8	2025-07-22 12:55:01.46457+03	1	stock	2	[{"changed": {"fields": ["Choosable"]}}]	7	1
9	2025-07-22 13:06:06.572904+03	9	حسن محمد حسن عبدالعزيز الاكوح	3		8	1
10	2025-07-22 13:06:06.572904+03	1	hossam mohamed alakwah	3		8	1
11	2025-07-23 09:25:42.898667+03	6	Log for 123456 at 2025-07-22 12:35:12.677920+00:00	3		11	1
12	2025-07-23 09:25:42.898667+03	5	Log for 123456 at 2025-07-22 11:00:25.904873+00:00	3		11	1
13	2025-07-23 09:25:42.898667+03	4	Log for 123456 at 2025-07-22 09:57:04.066881+00:00	3		11	1
14	2025-07-23 09:25:42.898667+03	3	Log for 123456 at 2025-07-22 09:42:46.049261+00:00	3		11	1
15	2025-07-23 09:25:48.261019+03	2	HP450 - 123456	3		10	1
16	2025-07-23 09:26:03.033463+03	3	Screen 27 inches - 22CW28300343	1	[{"added": {}}]	10	1
17	2025-07-23 09:26:07.80136+03	3	Screen 27 inches - 22CW28300343	2	[{"changed": {"fields": ["Branch"]}}]	10	1
18	2025-07-23 09:26:17.079461+03	3	Screen 27 inches - 22CW28300343	3		10	1
19	2025-07-23 09:32:14.498392+03	4	Screen 27 inches - 22CW28300343	1	[{"added": {}}]	10	1
20	2025-07-23 09:51:55.767802+03	3	All	1	[{"added": {}}]	7	1
21	2025-07-23 10:15:55.980038+03	1	Assets	1	[{"added": {}}]	13	1
22	2025-07-23 10:19:41.049887+03	1	Assets	2	[]	13	1
23	2025-07-23 10:23:13.581033+03	1	Assets	3		13	1
24	2025-07-23 10:23:22.068379+03	2	assets	1	[{"added": {}}]	13	1
25	2025-07-23 10:28:25.21883+03	2	assets	3		13	1
26	2025-07-23 10:28:38.199931+03	3	asset	1	[{"added": {}}]	13	1
27	2025-07-23 10:38:14.86181+03	3	asset	3		13	1
28	2025-07-23 10:38:30.643778+03	4	assets	1	[{"added": {}}]	13	1
29	2025-07-23 10:41:01.513052+03	4	assets	3		13	1
30	2025-07-23 10:41:24.80992+03	5	Asset	1	[{"added": {}}]	13	1
31	2025-07-23 10:45:24.838799+03	5	assets.Asset	3		13	1
32	2025-07-23 10:45:32.148041+03	6	assets.Asset	1	[{"added": {}}]	13	1
33	2025-07-23 10:54:34.46846+03	1	assets - product	1	[{"added": {}}]	12	1
34	2025-07-23 10:58:05.205631+03	2	assets - Serisal	1	[{"added": {}}]	12	1
35	2025-07-23 10:58:24.854436+03	2	assets - Serisal	2	[{"changed": {"fields": ["Is visible"]}}]	12	1
36	2025-07-23 10:58:37.803206+03	2	assets - Serisal	2	[{"changed": {"fields": ["Is visible"]}}]	12	1
37	2025-07-23 15:25:34.763184+03	3	assets - branch	1	[{"added": {}}]	12	1
38	2025-07-24 16:18:18.285869+03	7	test - test	3		10	1
39	2025-07-24 16:18:18.285869+03	6	asdad - asdasw	3		10	1
40	2025-07-24 16:18:18.285869+03	5	HP450 - 123123	3		10	1
41	2025-07-24 16:18:18.285869+03	4	Screen 27 inches - 22CW28300343	3		10	1
42	2025-07-27 12:29:32.157297+03	1	stock	1	[{"added": {}}]	7	1
43	2025-07-27 12:29:42.528152+03	2	Head Office	1	[{"added": {}}]	7	1
44	2025-07-27 12:32:55.622582+03	2	mohamed_tarek	1	[{"added": {}}]	6	1
45	2025-07-27 12:33:10.926407+03	2	mohamed_tarek	2	[{"changed": {"fields": ["Role"]}}]	6	1
46	2025-07-27 12:37:55.638955+03	2	HQ	2	[{"changed": {"fields": ["Name"]}}]	7	1
47	2025-07-27 12:42:06.372821+03	1	AbdelRahman ElShafie	1	[{"added": {}}]	8	1
48	2025-07-27 12:52:12.865407+03	3	Maadi	1	[{"added": {}}]	7	1
49	2025-07-27 12:52:54.544744+03	4	Assiut	1	[{"added": {}}]	7	1
50	2025-07-27 12:53:04.104584+03	5	Alex	1	[{"added": {}}]	7	1
51	2025-07-27 14:03:10.066721+03	406	Ahmed Hegazy	1	[{"added": {}}]	8	1
52	2025-07-27 15:21:50.788543+03	407	IT Room Maadi	1	[{"added": {}}]	8	1
53	2025-07-27 15:23:07.600739+03	408	IT Room Assuit	1	[{"added": {}}]	8	1
54	2025-07-27 15:48:32.966517+03	1	PROBOOK 450 G8 - 5CD147KZ4T	2	[{"changed": {"fields": ["Branch"]}}]	10	1
55	2025-07-27 15:51:38.149481+03	351	John Sawarsn	2	[{"changed": {"fields": ["Branch", "Created by"]}}]	8	1
56	2025-07-27 16:46:55.730887+03	409	IT Data Center	1	[{"added": {}}]	8	1
57	2025-07-28 11:23:27.082598+03	1	PROBOOK 450 G8 - 5CD147KZ4T	2	[{"changed": {"fields": ["Employee name"]}}]	10	1
58	2025-07-28 11:24:03.039753+03	3	PROBOOK 450 G8 - 5CD147KZ4N	2	[{"changed": {"fields": ["Employee name", "Branch"]}}]	10	1
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2025-07-22 12:02:46.219354+03
2	contenttypes	0002_remove_content_type_name	2025-07-22 12:03:03.996878+03
3	auth	0001_initial	2025-07-22 12:03:04.066904+03
4	auth	0002_alter_permission_name_max_length	2025-07-22 12:03:04.070853+03
5	auth	0003_alter_user_email_max_length	2025-07-22 12:03:04.074949+03
6	auth	0004_alter_user_username_opts	2025-07-22 12:03:04.078924+03
7	auth	0005_alter_user_last_login_null	2025-07-22 12:03:04.081924+03
8	auth	0006_require_contenttypes_0002	2025-07-22 12:03:04.082803+03
9	auth	0007_alter_validators_add_error_messages	2025-07-22 12:03:04.084889+03
10	auth	0008_alter_user_username_max_length	2025-07-22 12:03:04.089809+03
11	auth	0009_alter_user_last_name_max_length	2025-07-22 12:03:04.114883+03
12	auth	0010_alter_group_name_max_length	2025-07-22 12:03:04.121874+03
13	auth	0011_update_proxy_permissions	2025-07-22 12:03:04.127641+03
14	auth	0012_alter_user_first_name_max_length	2025-07-22 12:03:04.130709+03
15	users	0001_initial	2025-07-22 12:03:04.206034+03
16	admin	0001_initial	2025-07-22 12:03:04.240822+03
17	admin	0002_logentry_remove_auto_add	2025-07-22 12:03:04.246609+03
18	admin	0003_logentry_add_action_flag_choices	2025-07-22 12:03:04.250608+03
19	sessions	0001_initial	2025-07-22 12:03:04.26873+03
21	assets	0002_employee_branch	2025-07-22 12:49:29.94142+03
22	assets	0003_reportablemodel_alter_asset_branch_and_more	2025-07-23 10:06:05.794526+03
23	assets	0004_alter_employee_branch_alter_employee_created_by	2025-07-27 12:21:08.598509+03
24	assets	0001_initial	2025-07-27 12:28:22.832054+03
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
4n07cau873auzcvernc98nwulsjjcmvx	.eJxVjEEOwiAQRe_C2pBCYaa4dO8ZyDCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-juIslDj9boH4keoO4p3qrUludV3mIHdFHrTLa4vpeTncv4NCvXxrNJitCqitApggOTZglUFAGsgZHWwcEQmmQMg5ZkhWsxl4RErZURTvD7ogN7g:1ue9Wr:QfK93IHjLp2e7nIZSGc-Chf-RR4vMBP9oukTvozCWkU	2025-08-05 12:43:21.240113+03
vg1e9bpkxrdcejkw57u6t9iyw5jbkba8	.eJxVjEEOwiAQRe_C2pBCYaa4dO8ZyDCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-juIslDj9boH4keoO4p3qrUludV3mIHdFHrTLa4vpeTncv4NCvXxrNJitCqitApggOTZglUFAGsgZHWwcEQmmQMg5ZkhWsxl4RErZURTvD7ogN7g:1ue9pA:NBp5cFh84Fop24Ct1wEzVFlwijchn-yg9MFtKIcRSRI	2025-08-05 13:02:16.742096+03
a9gswf9zuq5xtoqk4567f8l7llbmjrht	.eJxVjEEOwiAQRe_C2pBCYaa4dO8ZyDCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-juIslDj9boH4keoO4p3qrUludV3mIHdFHrTLa4vpeTncv4NCvXxrNJitCqitApggOTZglUFAGsgZHWwcEQmmQMg5ZkhWsxl4RErZURTvD7ogN7g:1ue9pM:myUgpPymncFM16PJPREcfJkfoZZjR8fP7Yg7sjR6W0E	2025-08-05 13:02:28.781658+03
cxl8l79fxbs2txaggly1oiwfpuoaeipj	.eJxVjEEOwiAQRe_C2pBCYaa4dO8ZyDCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-juIslDj9boH4keoO4p3qrUludV3mIHdFHrTLa4vpeTncv4NCvXxrNJitCqitApggOTZglUFAGsgZHWwcEQmmQMg5ZkhWsxl4RErZURTvD7ogN7g:1ue9pz:EUt3d0CTV53Uv-CefSi-rWFJ6sbnQAuynRej_ZFKnV0	2025-08-05 13:03:07.010051+03
o4b5kc26z2vuwqz6y64y9bwynutl9slo	.eJxVjMsOwiAUBf-FtSEF2gu6dN9vINxHpWogKe3K-O_apAvdnpk5LxXTtua4NVnizOqijDr9bpjoIWUHfE_lVjXVsi4z6l3RB216rCzP6-H-HeTU8rem4EGwR98JhiEgEkxgg7AfTAiWHfhz3wGBAHlrnWCCRAYYrLMkk3p_AOoLOBQ:1ue9qp:4TOJXCtqcPaqZbFvoNfDU28whB8hMX4DaLZTop0CwwY	2025-08-05 13:03:59.194098+03
vx34gc1x1bwrx5tppvawkvzdk854ze1h	.eJxVjMsOwiAUBf-FtSEF2gu6dN9vINxHpWogKe3K-O_apAvdnpk5LxXTtua4NVnizOqijDr9bpjoIWUHfE_lVjXVsi4z6l3RB216rCzP6-H-HeTU8rem4EGwR98JhiEgEkxgg7AfTAiWHfhz3wGBAHlrnWCCRAYYrLMkk3p_AOoLOBQ:1ue9r2:31fsJS1x3mTp-q3T6qgJywkR61PeZZtRgXdDQSIB5tc	2025-08-05 13:04:12.379089+03
0r52pjjqfh7gugy59pe1z7q351512bab	.eJxVjMsOwiAUBf-FtSEF2gu6dN9vINxHpWogKe3K-O_apAvdnpk5LxXTtua4NVnizOqijDr9bpjoIWUHfE_lVjXVsi4z6l3RB216rCzP6-H-HeTU8rem4EGwR98JhiEgEkxgg7AfTAiWHfhz3wGBAHlrnWCCRAYYrLMkk3p_AOoLOBQ:1ue9rG:e-RKekrxZH51nhi7MuM4t2pY7WCC0khJbWaJ1s1Mq2o	2025-08-05 13:04:26.029119+03
gfmzqi8hgxdujh9p3flijns4gz5kpj09	.eJxVjMsOwiAUBf-FtSEF2gu6dN9vINxHpWogKe3K-O_apAvdnpk5LxXTtua4NVnizOqijDr9bpjoIWUHfE_lVjXVsi4z6l3RB216rCzP6-H-HeTU8rem4EGwR98JhiEgEkxgg7AfTAiWHfhz3wGBAHlrnWCCRAYYrLMkk3p_AOoLOBQ:1ueAix:XAkNrYQ5URPXMDZ-Uvz_URtbFo89fGHDtyU-tbdmqqw	2025-08-05 13:59:55.113318+03
f74vmugrppm69y4pomgvndq97bhbbw4n	.eJxVjMsOwiAUBf-FtSEF2gu6dN9vINxHpWogKe3K-O_apAvdnpk5LxXTtua4NVnizOqijDr9bpjoIWUHfE_lVjXVsi4z6l3RB216rCzP6-H-HeTU8rem4EGwR98JhiEgEkxgg7AfTAiWHfhz3wGBAHlrnWCCRAYYrLMkk3p_AOoLOBQ:1ueSuu:TpM7n4oSVbTZ1w_JWWlJBE21k5mzZhPAdSxFCgeMEGM	2025-08-06 09:25:28.896353+03
mip8anes5slaz5t8u3n43p7g7iv5qs6c	.eJxVjMsOwiAUBf-FtSEF2gu6dN9vINxHpWogKe3K-O_apAvdnpk5LxXTtua4NVnizOqijDr9bpjoIWUHfE_lVjXVsi4z6l3RB216rCzP6-H-HeTU8rem4EGwR98JhiEgEkxgg7AfTAiWHfhz3wGBAHlrnWCCRAYYrLMkk3p_AOoLOBQ:1ueUUQ:KEplWcyUMZ1Z9W5pLcd8aMKJd3KYWcRg-ofFOHZdeAs	2025-08-06 11:06:14.003629+03
hff39lgffhq6usnqcv2gajikv414y05u	.eJxVjMsOwiAUBf-FtSEF2gu6dN9vINxHpWogKe3K-O_apAvdnpk5LxXTtua4NVnizOqijDr9bpjoIWUHfE_lVjXVsi4z6l3RB216rCzP6-H-HeTU8rem4EGwR98JhiEgEkxgg7AfTAiWHfhz3wGBAHlrnWCCRAYYrLMkk3p_AOoLOBQ:1ueUUZ:tV30CziB3aaAi6zMsx0cc6mhSzkulYOBvvifVixBnl4	2025-08-06 11:06:23.689382+03
cricv5cq5n89b5f4dgum5v9mfpvnpkz5	.eJxVjMsOwiAUBf-FtSEF2gu6dN9vINxHpWogKe3K-O_apAvdnpk5LxXTtua4NVnizOqijDr9bpjoIWUHfE_lVjXVsi4z6l3RB216rCzP6-H-HeTU8rem4EGwR98JhiEgEkxgg7AfTAiWHfhz3wGBAHlrnWCCRAYYrLMkk3p_AOoLOBQ:1ueUUq:m7RC1rasavfrEFvkCj1JZrGZcw6-PQox2Km7ljL2L8w	2025-08-06 11:06:40.318843+03
sldpvht9ya1evsldknpqf2ok7csrxkhd	.eJxVjMsOwiAUBf-FtSEF2gu6dN9vINxHpWogKe3K-O_apAvdnpk5LxXTtua4NVnizOqijDr9bpjoIWUHfE_lVjXVsi4z6l3RB216rCzP6-H-HeTU8rem4EGwR98JhiEgEkxgg7AfTAiWHfhz3wGBAHlrnWCCRAYYrLMkk3p_AOoLOBQ:1ueUV6:H3ar0hC_lRiLb2cwMvH7jrDq5tlNJ9lmngQouAAKk0g	2025-08-06 11:06:56.651887+03
7t7tdtmehunf061cf475uhsprv1rjlgx	.eJxVjMsOwiAUBf-FtSEF2gu6dN9vINxHpWogKe3K-O_apAvdnpk5LxXTtua4NVnizOqijDr9bpjoIWUHfE_lVjXVsi4z6l3RB216rCzP6-H-HeTU8rem4EGwR98JhiEgEkxgg7AfTAiWHfhz3wGBAHlrnWCCRAYYrLMkk3p_AOoLOBQ:1ueUVK:1oZz7tC9oOsljQUGM4PD3o4nOi27H9kb7z3UhczmUv4	2025-08-06 11:07:10.599081+03
d49gyv0hi9izkeflkr5eszd50ib98zrs	.eJxVjMsOwiAUBf-FtSEF2gu6dN9vINxHpWogKe3K-O_apAvdnpk5LxXTtua4NVnizOqijDr9bpjoIWUHfE_lVjXVsi4z6l3RB216rCzP6-H-HeTU8rem4EGwR98JhiEgEkxgg7AfTAiWHfhz3wGBAHlrnWCCRAYYrLMkk3p_AOoLOBQ:1ufITA:o_9bANQc6VASWXq_ZiH7CMR2nqS4x5STdOT7TBvbNQA	2025-08-08 16:28:16.227874+03
rix5yseksn7qiah22izymx5unyztu248	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufv93:ISEgxNXlcEcBijoiR6qCJUES5fJJa3GPzp3Rsw_oClM	2025-08-10 09:46:05.229585+03
t0e4n69ztdh3y5244j3q821wdowwzklv	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvAt:aQQHnRIDGu0uzKv_8dCKEXIpmjTljcYntivPbIDyBA4	2025-08-10 09:47:59.306634+03
9igczpttyjdy09lsq90uj7nhkshj9u38	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvBf:XIpgr9vNePb6q_likLI5zkMouBVCGRMdSfpBECkX7-Q	2025-08-10 09:48:47.434179+03
bcadh3hlg9j96odygq3gj4ncvkkk6bcb	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvBz:yQTquzY19lwJcHpXLuJyQpaSP2FpeYcXxsPjZ0Xyg4Q	2025-08-10 09:49:07.70654+03
h6q0r9873dumt7eypbdlwjs6e9ficaq8	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvCw:-hS6jWB4h6GGjSgsTCmF9FgHdE09orR5gde5ygEopdE	2025-08-10 09:50:06.879041+03
fix77mabsphqdsfeu5oj5l5swve6c9z2	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvKb:_2q3qonYZW1Tp8zbo8HKZF6Fd4aUx0m2Ec_b0-w4Cm8	2025-08-10 09:58:01.122689+03
w35jwbgwb020fbhcxebntvv3i2gfadhs	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvMM:UQNUAbVqFFywUTOmiNTitFrHC_7CijK5vZ4gOQC94TY	2025-08-10 09:59:50.05504+03
b7yq8pmtyzooynm2xgi1n08tjdjqk1cp	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvNQ:YUBTRnLYODat_VgrFR2v73bwPqrVsfThByBF6vtwO54	2025-08-10 10:00:56.357688+03
iumlj0roaj53kvvm5uf0imomlhg05xn1	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvPl:_duYH2pqArXbgJKR2JqpGxAPzz-FihfTYv5poTN4Xxw	2025-08-10 10:03:21.094815+03
cw5rbq7slb2q58p6wlnga74bk60c6jmn	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvPw:nWslizwJyvloqLuIrtrveLtaVqnF_1yVpNwSA5FmE_w	2025-08-10 10:03:32.778973+03
sb86pc5o9ig2ooxnt6x12q21lsagyn7q	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvQ2:uI89VnXel2rNBgT0UmpdLXcYu3wwu4dtNQA0JgL8Yps	2025-08-10 10:03:38.409864+03
dmxhlx05tlsjdsdd6stpf2zr4wf8fa30	e30:1ufvSS:zv1bY38reuTiHcapO546wKAzaJER6zjAl_fGgJWtotA	2025-08-10 10:06:08.753795+03
n21145t9rrg2ykmglmfzlmnz80brq1xm	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvSw:BZ7sbiOtihu2qx4HH8fmYTczf7picwKG1Mfv0sTXHc4	2025-08-10 10:06:38.167893+03
eexnw1ha0v1vx65hfoq181eqaen7jvkq	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvTG:dt7raaH6ppauPa6PeMK3K6R4hlZDI5jSd_JcE7QfmCo	2025-08-10 10:06:58.983569+03
x1anh11wcs1xd547crfgg1587mw17zir	e30:1ufvTk:W4WyexiP5EMxtYbmk4UqEUOCw64xggcvq_FNNZSoYfI	2025-08-10 10:07:28.133753+03
o7g1dhaqgbo9s6be65vta56dqegz46dt	e30:1ufvUX:Us8omRzJwfJJxvMHfLq8tL57LlRvPM2iw9ODgxnauzg	2025-08-10 10:08:17.227868+03
dlxtxg47ajx1rsp9wp7v1z3jbuuvkh4x	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvVO:Asi_BjOP_7EhZzPNbTSVkcIxuEJIFT3sU-aGJL6Aqls	2025-08-10 10:09:10.883389+03
ps2x8lfp6a9uv8ifbcy614o6jgvsezeu	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvWJ:_too5qstBn5m0CgDhad86DtuFOjHDpZsMdGvgVMjK3Q	2025-08-10 10:10:07.14525+03
qtz0pu57u1jou06aaii8jhrbge9r9x7z	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvWr:aRMZYnfp9s_dLLt-9ruKClWLSrBapiP1eziQKtMm8Gk	2025-08-10 10:10:41.325301+03
ze4w2fruk83oeuqd7pw4rc1f1fc0efgg	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufziZ:0YHXmQrTgSZHJqZEqqkxe3yrM1wonUDp4BOZvRFS4Bw	2025-08-10 14:39:03.634499+03
gxwpvyejax1d0ivvbq9roevzmy1wc86b	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvX4:2EM7gTBMNFAoFZ29ubLtgWjfVRtCDOUKR1_AxOkUhZQ	2025-08-10 10:10:54.416466+03
v3rvuzdusjpc06dccl86e8le8klcoufj	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ug0Ry:kgPzP7GLZRrvzNQmZ-RqepNwuaHIHm0GOpNsc7uB4ag	2025-08-10 15:25:58.454698+03
vupe7gvrbk3v2wnxudh1oslj8mikiz09	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvXU:1fXukwJUf5sQ1yV1FHtwTpGdU39H6HS505e6BEloB14	2025-08-10 10:11:20.986842+03
8hpyadfih6fmx8f5phr6trqt8ozm7z04	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ugJfP:txAYGcljq31CNVsybbwm_bCBesPCfzf2K4hVgf6VNw8	2025-08-11 11:57:07.52906+03
c80ytg0blvv9r0pz8rz3a0l58i7vb7g6	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvXt:R8lsA_cC_n0n4TYVMShHEW8c12EXrCvA8HcCDAV7oYc	2025-08-10 10:11:45.154117+03
v1vitsjshk433k6b2y4u4qcwh3tvzomg	.eJxVjDsOwjAQBe_iGlnrbwwlfc5grb1rHECOFCcV4u4QKQW0b2beS0Tc1hq3zkucSFyEEqffLWF-cNsB3bHdZpnnti5TkrsiD9rlOBM_r4f7d1Cx12_NylDIxgaXBgOez0F7doRFoSZTEmHWtiAAcPLEuZBxVCzAwAFKJvH-APnbORA:1ugKOI:suy6G0YWQZbYBeMjtJV5tbf6D_Iqf83O-p3pTa_Tpds	2025-08-11 12:43:30.013311+03
gdarf3oqvfcwzekz4df2slt56l456jch	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufvY6:kxgdUoBYmqsgrwqd_VKHhBCXwCLtG_j_sEPwH_6J1ZI	2025-08-10 10:11:58.275721+03
ez5aa7p3mpsnt596wr81k3hp55r1xhd1	.eJxVjDkOwjAUBe_iGln-2HihpOcM1t-EAyiR4qRC3B0ipYD2zcx7mYrr0urada6DmLMBc_jdCPmh4wbkjuNtsjyNyzyQ3RS7026vk-jzsrt_Bw17-9ZEhdlh0MhBfQEBKeQwgQNIHDwevRJF8uKT5lMJCWJSKFkFKHMx7w_zyDf8:1ufva0:Mc5a5r3UHESiU6EogaEO2WHtWHVRQCBbLnn-3mwqdtE	2025-08-10 10:13:56.158313+03
\.


--
-- Data for Name: users_customuser_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_customuser_groups (id, customuser_id, group_id) FROM stdin;
\.


--
-- Data for Name: users_customuser_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_customuser_user_permissions (id, customuser_id, permission_id) FROM stdin;
\.


--
-- Name: assets_asset_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.assets_asset_id_seq', 1, false);


--
-- Name: assets_assetlog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.assets_assetlog_id_seq', 463, true);


--
-- Name: assets_branch_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.assets_branch_id_seq', 5, true);


--
-- Name: assets_employee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.assets_employee_id_seq', 409, true);


--
-- Name: assets_reportablefield_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.assets_reportablefield_id_seq', 1, false);


--
-- Name: assets_reportablemodel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.assets_reportablemodel_id_seq', 1, false);


--
-- Name: assets_storagedevice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.assets_storagedevice_id_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 52, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 58, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 13, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 24, true);


--
-- Name: users_customuser_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_customuser_groups_id_seq', 1, false);


--
-- Name: users_customuser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_customuser_id_seq', 2, true);


--
-- Name: users_customuser_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_customuser_user_permissions_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

