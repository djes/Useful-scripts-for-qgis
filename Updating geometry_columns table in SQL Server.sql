--https://gis.stackexchange.com/questions/71558/implementing-geometry-columns-table-in-sql-server-for-qgis
--run with SQL 'dbo.fill_geometry_columns'
DROP PROCEDURE IF EXISTS dbo.fill_geometry_columns
GO
CREATE PROCEDURE dbo.fill_geometry_columns AS 

DECLARE @RowsToProcess INT
DECLARE @CurrentRow INT
DECLARE @SelectCol_schema_name NVARCHAR(100)
DECLARE @SelectCol_table_name NVARCHAR(100)
DECLARE @SelectCol_column_name NVARCHAR(100)
DECLARE @run_sql1 NVARCHAR(max)
DECLARE @run_sql2 NVARCHAR(max)
DECLARE @run_update1 NVARCHAR(max)
DECLARE @run_update2 NVARCHAR(max)
DECLARE @Selected_geometry_type NVARCHAR(100)
DECLARE @Selected_geometry_srid NVARCHAR(100)

DELETE FROM [dbo].[geometry_columns]

CREATE TABLE #spatialTables (
    RowID INT NOT NULL PRIMARY KEY identity(1, 1)
    ,f_table_catalog NVARCHAR(128) NOT NULL
    ,f_table_schema NVARCHAR(100)
    ,f_table_name NVARCHAR(256) NOT NULL
    ,f_geometry_column NVARCHAR(256) NOT NULL
    ,coord_dimension INT NOT NULL
    ,[srid] [int] NOT NULL
    ,[geometry_type] [varchar](30) NOT NULL
    )

INSERT INTO #spatialTables
SELECT DISTINCT c.TABLE_CATALOG
    ,c.TABLE_SCHEMA AS TABLE_SCHEMA
    ,c.TABLE_NAME AS TABLE_NAME
    ,c.COLUMN_NAME AS COLUMN_NAME
    ,2 AS coord_dimension
    ,4326
    ,'nu'
FROM information_schema.columns c
JOIN information_schema.tables t ON c.TABLE_NAME = t.TABLE_NAME
    AND t.TABLE_TYPE IN (
        'BASE TABLE'
        ,'VIEW'
        )
WHERE c.DATA_TYPE = 'geometry'
ORDER BY c.TABLE_SCHEMA
    ,c.TABLE_NAME

SET @RowsToProcess = @@ROWCOUNT
SET @CurrentRow = 0

WHILE @CurrentRow < @RowsToProcess
BEGIN
    SET @CurrentRow = @CurrentRow + 1

    SELECT @SelectCol_schema_name = f_table_schema
        ,@SelectCol_table_name = f_table_name
        ,@SelectCol_column_name = f_geometry_column
    FROM #spatialTables
    WHERE RowID = @CurrentRow

    SET @run_sql1 = 'SELECT TOP 1 @table_geometry_type='+ @SelectCol_column_name + '.STGeometryType() FROM [' + @SelectCol_schema_name + '].[' + @SelectCol_table_name + '] WHERE ['+ @SelectCol_column_name + '] IS NOT NULL'
    print @run_sql1

    EXECUTE sp_executesql @run_sql1
        ,N'@table_geometry_type nvarchar(100) OUTPUT'
        ,@table_geometry_type = @Selected_geometry_type OUTPUT
    
    print @SelectCol_table_name + '  ' + @SelectCol_column_name + ' ' + @Selected_geometry_type

    --SET @run_update1 = 'update #spatialTables  set [geometry_type] = ''' + @Selected_geometry_type + ''' where [f_table_name]=''' + @SelectCol_table_name + ''''
     
    set @run_update1='update #spatialTables set [geometry_type] = '''+@Selected_geometry_type+
    ''',coord_dimension = '+
    'case 
    when '''+@Selected_geometry_type +'''= ''Point''
    Then 0
    when '''+@Selected_geometry_type +'''= ''LineString''
    Then 1
    Else 2
    END'
    +' where [f_table_name]='''+@SelectCol_table_name+''' and [f_geometry_column]=''' + @SelectCol_column_name+''' and [f_table_schema]=''' + @SelectCol_schema_name + ''''
      print @run_update1
      EXECUTE sp_executesql @run_update1 
     
SET @run_sql2 = 'select TOP 1 @table_geometry_srid= ['+ @SelectCol_column_name + '].STSrid from [' + @SelectCol_schema_name + '].[' + @SelectCol_table_name + '] WHERE '''+ @SelectCol_column_name + ''' IS NOT NULL'

    print @run_sql2
    EXECUTE sp_executesql @run_sql2
        ,N'@table_geometry_srid nvarchar(100) OUTPUT'
        ,@table_geometry_srid = @Selected_geometry_srid OUTPUT
    
   print @SelectCol_table_name + ' '+ @SelectCol_column_name + ' ' +  @Selected_geometry_srid

    SET @run_update2 = 'update #spatialTables  set [srid] = ''' + @Selected_geometry_srid + ''' where [f_table_name]=''' + @SelectCol_table_name + ''' and [f_geometry_column]=''' + @SelectCol_column_name+''' and [f_table_schema]=''' + @SelectCol_schema_name + ''''

    print @run_update2
    EXECUTE sp_executesql @run_update2

    --PRINT @run_update
END

INSERT INTO [dbo].[geometry_columns]
SELECT [f_table_catalog]
    ,[f_table_schema]
    ,[f_table_name]
    ,[f_geometry_column]
    ,[coord_dimension]
    ,[srid]
    ,[geometry_type]
FROM #spatialTables

DROP TABLE #spatialTables