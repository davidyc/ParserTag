create database CountTags


use CountTags
 
create table SaitNameTable(
id int primary key identity(1,1) not null,
saitname varchar(255) not null 
);

create table TagsNameAndCount(
id int primary key identity(1,1) not null,
saitnameID int FOREIGN KEY REFERENCES SaitNameTable(id),
tag varchar(15) not null,
counttags int not null
);

insert into SaitNameTable(saitname)
values
('testdsait.com')

