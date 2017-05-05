drop table if exists patient;
create table patient(pid varchar(20),username varchar(20),name varchar(20),email varchar(20),contact varchar(20),address varchar(50),dob date,bloodgrp varchar(20));


drop table if exists pat_health;	
create table pat_health(pid varchar(20),symp0 varchar(10),symp1 varchar(10),symp2 varchar(10),symp3 varchar(10),symp4 varchar(10),symp5 varchar(10),symp6 varchar(10),symp7 varchar(10),symp8 varchar(10),symp9 varchar(10),symp10 varchar(10),symp11 varchar(10),symp12 varchar(10),result varchar(10));
