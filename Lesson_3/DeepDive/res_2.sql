$SourceTable      = "//home/data/tutorial/ytsaurus_intro/user_activity_log";
$DestinationTable = "//home/test/search_dau";

INSERT INTO
    $DestinationTable
WITH truncate

SELECT
    DISTINCT count(userid) as users,
    `date`
FROM
    $SourceTable
WHERE
    `action` == "search"
GROUP BY
    DateTime::MakeDate(DateTime::Split(`timestamp`)) as `date`
;
