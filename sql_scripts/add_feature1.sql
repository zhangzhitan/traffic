create procedure add_feature (@table_name varchar(30))
as
begin
declare @sql nvarchar(max)

set @sql = 'update '+ @table_name + ' set lastarrtime=thisdeptime where lastarrtime=''start'''
EXEC(@sql)
set @sql = 'update '+ @table_name +' set thisdeptime=lastarrtime where thisdeptime=''end'''
EXEC(@sql)
set @sql = 'update '+ @table_name +' set thisarrtime=nextdeptime where thisarrtime=''start'''
EXEC(@sql)
set @sql = 'update '+ @table_name +' set nextdeptime=thisarrtime where nextdeptime=''end'''
EXEC(@sql)


set @sql ='alter table ' + @table_name + ' alter column lastarrtime datetime'
EXEC(@sql)
set @sql ='alter table ' + @table_name + ' alter column thisdeptime datetime'
EXEC(@sql)
set @sql ='alter table ' + @table_name + ' alter column thisarrtime datetime'
EXEC(@sql)
set @sql ='alter table ' + @table_name + ' alter column nextdeptime datetime'
EXEC(@sql)
set @sql ='alter table ' + @table_name + ' alter column delaydetail smallint'
EXEC(@sql)
set @sql ='alter table ' + @table_name + ' alter column rownum tinyint'
EXEC(@sql)
set @sql ='alter table ' + @table_name + ' alter column allrow tinyint'
EXEC(@sql)

set @sql ='alter table ' + @table_name + ' add pair varchar(30)'
EXEC(@sql)
set @sql ='alter table ' + @table_name + ' add accumulative float'
EXEC(@sql)
set @sql ='alter table ' + @table_name + ' add t_month tinyint'
EXEC(@sql)
set @sql ='alter table ' + @table_name + ' add t_quart tinyint'
EXEC(@sql)
set @sql ='alter table ' + @table_name + ' add t_week tinyint'
EXEC(@sql)
set @sql ='alter table ' + @table_name + ' add t_hour tinyint'
EXEC(@sql)
set @sql ='alter table ' + @table_name + ' add t_period smallint'
EXEC(@sql)
set @sql ='alter table ' + @table_name + ' add t_type char(1)'
EXEC(@sql)


set @sql ='update ' + @table_name + ' set pair=thisdepcode+thisarrcode'
EXEC(@sql)
set @sql ='update ' + @table_name + ' set accumulative = 1.0*rownum/allrow'
EXEC(@sql)
set @sql ='update ' + @table_name + ' set t_month = DATEPART(mm, thisdeptime)'
EXEC(@sql)
set @sql ='update ' + @table_name + ' set t_quart = DATEPART(qq, thisdeptime)'
EXEC(@sql)
set @sql ='update ' + @table_name + ' set t_week = DATEPART(w, thisdeptime)'
EXEC(@sql)
set @sql ='update ' + @table_name + ' set t_hour = DATEPART(hh, thisdeptime)'
EXEC(@sql)
set @sql ='update ' + @table_name + ' set t_period = DATEDIFF(mi, thisdeptime, thisarrtime)'
EXEC(@sql)
set @sql ='update ' + @table_name + ' set t_type = SUBSTRING(realtrainnum, 1, 1)'
EXEC(@sql)
set @sql ='update ' + @table_name + ' set t_type = ''P'' WHERE t_type like ''[0-9]'' '
EXEC(@sql)

end

