import os
import json

from yt.wrapper import YtClient

SRC_TABLE = "//home/data/tutorial/ytsaurus_intro/user_activity_log"
DEST_TABLE = "//home/test/search_dau"

QUERY = f"""
INSERT INTO
    '{DEST_TABLE}'
WITH truncate

SELECT
    DISTINCT count(userid) as users,
    `date`
FROM
    '{SRC_TABLE}'
WHERE
    `action` == "search"
GROUP BY
    DateTime::MakeDate(DateTime::Split(`timestamp`)) as `date`
;
"""


def main():
    YT_PROXY = os.getenv("YT_PROXY", default="84.201.169.208:80")
    if YT_PROXY is None or YT_PROXY == "":
        raise RuntimeError("Environment variable YT_PROXY is empty")

    with open("config.json", "r") as f:
        config = json.load(f)

    client = YtClient(proxy=YT_PROXY, config=config)

    client.start_query(engine='yql', query=QUERY)


if __name__ == "__main__":
    main()
