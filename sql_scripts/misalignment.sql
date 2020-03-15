CREATE PROCEDURE misalignment(@tdate varchar(30), @trainnum varchar(10))
AS
BEGIN
DECLARE @sql varchar(max) = 'INSERT INTO transform'
SET @sql = @sql+ @tdate +'(realtrainnum,lastarrtime ,thisdeptime ,thisdepcode ,thisarrtime ,nextdeprtime,thisarrcode,delayflag ,delaydetail ,rownum ,allrow )
SELECT a.realtrainnum, a.arrtime AS lastarrtime, a.deptime AS thisdeptime, a.code as thisdepcode, b.arrtime AS thisarrtime
, b.deptime AS nextdeprtime, b.code as thisarrcode, b.delayflag, b.delaydetail, a.rownum, count(*) over() as allrow
	FROM (
		SELECT row_number() OVER (ORDER BY deptime) AS rownum, *
		FROM newtrain20190702
		WHERE realtrainnum ='+''''+ @trainnum+'''' +'
	) a, (
			SELECT row_number() OVER (ORDER BY deptime) AS rownum, *
			FROM newtrain20190702
			WHERE realtrainnum ='+''''+ @trainnum+'''' +'
		) b
	WHERE a.rownum = b.rownum - 1
	ORDER BY thisdeptime'
EXEC(@sql)
END