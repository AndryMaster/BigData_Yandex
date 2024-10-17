$SourceTable      = "//home/data/tutorial/ytsaurus_intro/user_activity_log";
$DestinationTable = "//home/test/max_acquisition_month";

$format = DateTime::Format("%Y-%m");

INSERT INTO
    $DestinationTable
WITH truncate

SELECT
    `month`,
    count(*) as `count`
FROM
    (
        SELECT
            `userid`,
            $format(MIN(DateTime::MakeDate(DateTime::Split(`timestamp`)))) as `month`
        FROM
            $SourceTable
        GROUP BY
            `userid`
    )

GROUP BY
    `month`

ORDER BY
    `count` DESC,
    `month` DESC

LIMIT 1 OFFSET 0;
;
