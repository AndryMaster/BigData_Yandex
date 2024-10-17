$SourceTable      = "//home/data/tutorial/ytsaurus_intro/user_activity_log";
$DestinationTable = "//home/test/revenue_by_month";

$format = DateTime::Format("%Y-%m");

INSERT INTO
    $DestinationTable
WITH truncate

SELECT
    SUM(`value`) as `value`,
    `month`
FROM
    $SourceTable
WHERE
    `action` == "confirmation"
GROUP BY
    $format(DateTime::Split(`timestamp`)) as `month`
;
