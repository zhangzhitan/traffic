update Tablename set lastarrtime=thisdeptime where lastarrtime='start'
update Tablename set thisdeptime=lastarrtime where thisdeptime='end'
update Tablename set thisarrtime=nextdeptime where thisarrtime='start'
update Tablename set nextdeptime=thisarrtime where nextdeptime='end'


alter table Tablename alter column lastarrtime datetime
alter table Tablename alter column thisdeptime datetime
alter table Tablename alter column thisarrtime datetime
alter table Tablename alter column nextdeptime datetime
alter table Tablename alter column delaydetail smallint
alter table Tablename alter column rownum tinyint
alter table Tablename alter column allrow tinyint

alter table Tablename add pair varchar(30)
update Tablename set pair=thisdepcode+thisarrcode

alter table Tablename add accumulative float
update Tablename set accumulative = 1.0*rownum/allrow


alter table Tablename add t_month tinyint
update Tablename set t_month = DATEPART(mm, thisdeptime)

alter table Tablename add t_quart tinyint
update Tablename set t_quart = DATEPART(qq, thisdeptime)

alter table Tablename add t_week tinyint
update Tablename set t_week = DATEPART(w, thisdeptime)

alter table Tablename add t_hour tinyint
update Tablename set t_hour = DATEPART(hh, thisdeptime)

alter table Tablename add period smallint
update Tablename set period = DATEDIFF(mi, thisdeptime, thisarrtime)

alter table Tablename add t_type char(1)
update Tablename set t_type = SUBSTRING(realtrainnum, 1, 1)
update Tablename set t_type = 'P' WHERE t_type like '[0-9]'
