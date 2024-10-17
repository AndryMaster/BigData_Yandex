$SourceTable      = "//home/data/tutorial/ytsaurus_intro/user_activity_log";
$DestinationTable = "//home/test/churned_in_may";


INSERT INTO
    $DestinationTable
WITH truncate

SELECT
    `userid`,
    `date`
FROM
    (
        SELECT
            `userid`,
            MAX(DateTime::MakeDate(DateTime::Split(`timestamp`))) as `date`
        FROM
            $SourceTable
        GROUP BY
            `userid`
    )
WHERE
    `date` >= DateTime::MakeDate(DateTime::Split(Datetime("2022-05-01T00:00:00Z")))
    AND
    `date` <  DateTime::MakeDate(DateTime::Split(Datetime("2022-06-01T00:00:00Z")))
ORDER BY
    `date`
;
