PRAGMA foreign_keys=OFF;
BEGIN TRANSCATION;
create table Readerlist(
  ReaderID char(50) primary key,
    Name char(50),
   Sex char(10),
   Department char(50)
);
insert into Readerlist values ('PB13207074','Xu Han','Female','EE');
insert into Readerlist values ('PB13207073','Yi Fu','Female','Biology');


create table Adlist(
   AdID char(50) primary key,
   Name char(50),
   Sex char(10),
   job char(50),
   password char(50)
);
insert into Adlist values('Ad001','Wei Wang','Male','Professor','123456'); 
insert into Adlist values('Ad002','Pingbo Yuan','Male','Professor','123456');
create table booklist(
   ISBN char(70) primary key,
   title char(100),
   num char(70),
   author char(100),
   publisher char(100),
   year char(70),
   state char(70),
   place char(200),
   leftnum int,
   borrowed int
);
insert into booklist values('HP1','Harry Potter 1','TP001','JK.Rowling','People Publisher','1995','can be borrowed','4th floor of the library on west campus',2,1);
COMMIT;
create table borrow(
   ISBN char(50),
   ReaderID char(70),
   borrowtime char(50),
   returntime char(50)
);
create table buy(
   ISBN char(50) primary key,
   num int,
   buytime char(50)
);
create table updatebook(
   ISBN char(50),
   newnum int,
   dienum int,
   updatetime char(50)
);