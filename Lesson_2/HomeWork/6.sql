$SourceTable      = "//home/data/tutorial/ytsaurus_intro/user_activity_log";
$DestinationTable = "//home/test/checkout_freq";


INSERT INTO
    $DestinationTable
WITH truncate

SELECT
    `userid`,
    COUNT(`userid`) as `frequency`
FROM
    $SourceTable
WHERE
    `action` == "checkout"
GROUP BY
    `userid`
;
