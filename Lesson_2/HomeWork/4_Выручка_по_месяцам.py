import os
import json

from yt.wrapper import YtClient

SRC_TABLE = "//home/data/tutorial/ytsaurus_intro/user_activity_log"
DEST_TABLE = "//home/test/revenue_by_month"


def main():
    YT_PROXY = os.getenv("YT_PROXY")
    if YT_PROXY is None or YT_PROXY == "":
        raise RuntimeError("Environment variable YT_PROXY is empty")

    with open("config.json", "r") as f:
        config = json.load(f)

    client = YtClient(proxy=YT_PROXY, config=config)

    client.start_query(engine='yql', query=f"""
$format = DateTime::Format("%Y-%m");

INSERT INTO
    '{DEST_TABLE}'
WITH truncate

SELECT
    SUM(`value`) as `value`,
    `month`
FROM
    '{SRC_TABLE}'
WHERE
    `action` == "confirmation"
GROUP BY
    $format(DateTime::Split(`timestamp`)) as `month`
;
""")


if __name__ == "__main__":
    os.environ["YT_PROXY"] = "84.201.169.208:80"
    main()
