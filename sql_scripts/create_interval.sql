CREATE PROCEDURE create_interval(@start_date varchar(20), @end_date varchar(20))
AS
BEGIN

	DECLARE @delta INT
	DECLARE @now DATE
	DECLARE @table VARCHAR(20)

	SET @delta = DATEDIFF(DAY,@start_date,@end_date )
	SET @now = @start_date

	DECLARE @CREATE_VIEW_SQL VARCHAR(MAX)
	DECLARE @SINGLE_TABLE_SQL_1 VARCHAR(MAX)
	DECLARE @SINGLE_TABLE_SQL_2 VARCHAR(MAX)
	DECLARE @THIS_TABLE VARCHAR(MAX)
	DECLARE @CREATE_VIEW_SQL_TAIL VARCHAR(MAX)

	SET @CREATE_VIEW_SQL = 'CREATE VIEW temp_query as '
	SET @CREATE_VIEW_SQL = @CREATE_VIEW_SQL + 'select ROW_NUMBER()over(order by realtrainnum) as id_num , '
	SET @CREATE_VIEW_SQL = @CREATE_VIEW_SQL + 'realtrainnum, arrtime, deptime, code, stationname, delayflag, delaydetail, dropflag FROM ( '
	SET @CREATE_VIEW_SQL_TAIL = ')TEMP'

	SET @SINGLE_TABLE_SQL_1 = 'SELECT realtrainnum, arrtime, deptime, code, stationname, delayflag, delaydetail, LEFT(realtrainnum, len(realtrainnum) - 2) AS dropflag FROM '
	SET @SINGLE_TABLE_SQL_2 = ' WHERE delaydetail <> ''-''UNION ALL '

	IF EXISTS(SELECT 1 FROM sys.views WHERE name='temp_query')
	BEGIN
		DROP VIEW temp_query
	END;

	WHILE @delta >= 0
		BEGIN
			SET @table = 'newtrain' + CONVERT(varchar(100), @now, 112)
			SET @THIS_TABLE = @SINGLE_TABLE_SQL_1 + @table + @SINGLE_TABLE_SQL_2
			SET @delta = @delta -1
			SET @now = DATEADD(DAY,1,@now)

			SET @CREATE_VIEW_SQL = @CREATE_VIEW_SQL + @THIS_TABLE
		END

	SET @CREATE_VIEW_SQL = LEFT(@CREATE_VIEW_SQL, len(@CREATE_VIEW_SQL) - 9) + @CREATE_VIEW_SQL_TAIL
	EXEC(@CREATE_VIEW_SQL)
END