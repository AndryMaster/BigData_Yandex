$SourceTable      = "//home/students/donkandr/files/user_activity_log";
$DestinationTable = "//home/students/donkandr/homework/les_2/table_7";


INSERT INTO
    $DestinationTable
WITH truncate

SELECT
    `action`,
    COUNT(`userid`) as `count`
FROM
    $SourceTable
GROUP BY
    `action`
;

-- INSERT INTO
--     $DestinationTable
-- -- WITH truncate

-- SELECT
--     -- "total" as `action`,
--     -- SUM(`count`) as `count`
--     CAST(<|"action": "total", "count": SUM(`count`)|> AS Struct<two:Utf8, three:Int64>)
-- FROM
--     $DestinationTable
-- ;
