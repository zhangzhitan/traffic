CREATE PROCEDURE misalignment(@tdate varchar(30), @trainnum varchar(10))
AS
BEGIN
-- trainnum可以为数据表中不存在的值，但是tdate不可以
DECLARE @sql varchar(max) = 'INSERT INTO transform'

SET @sql = @sql+ @tdate +'(realtrainnum,lastarrtime ,thisdeptime ,thisdepcode ,thisarrtime ,nextdeptime,thisarrcode,delayflag ,delaydetail ,rownum ,allrow )
SELECT a.realtrainnum, a.arrtime AS lastarrtime, a.deptime AS thisdeptime, a.code as thisdepcode, b.arrtime AS thisarrtime
, b.deptime AS nextdeptime, b.code as thisarrcode, b.delayflag, b.delaydetail, a.rownum, count(*) over() as allrow
	FROM (
		SELECT row_number() OVER (ORDER BY deptime) AS rownum, *
		FROM newtrain'+@tdate+'
		WHERE realtrainnum ='+''''+ @trainnum+'''' +'
	) a, (
			SELECT row_number() OVER (ORDER BY deptime) AS rownum, *
			FROM newtrain'+@tdate+'
			WHERE realtrainnum ='+''''+ @trainnum+'''' +'
		) b
	WHERE a.rownum = b.rownum - 1
	ORDER BY thisdeptime'
EXEC(@sql)
END
