import os
import json
import datetime
from typing import Iterable

from yt.wrapper import YtClient, TypedJob, yt_dataclass
from yt.wrapper.schema import RowIterator

INPUT_TABLE = "//home/data/tutorial/ytsaurus_intro/user_activity_log"
BASE_TMP = "//tmp"


@yt_dataclass
class UserRow:
    userid: str
    timestamp: datetime.datetime
    action: str
    value: float
    testids: str


@yt_dataclass
class UserFiltered:
    userid: str
    timestamp: datetime.datetime
    action: str


@yt_dataclass
class UserCheckCount:
    userid: str
    count: int


class Operation_1(TypedJob):
    def __call__(self, user: UserRow) -> Iterable[UserFiltered]:
        if user.action == "checkout":
            yield UserFiltered(userid=user.userid,
                               timestamp=user.timestamp,
                               action="checkout")


class Operation_2(TypedJob):
    def __call__(self, stream: RowIterator[UserFiltered]) -> Iterable[UserCheckCount]:
        count = 0
        last_id = None

        for row in stream:
            last_id = row.userid
            count += 1

        assert last_id is not None

        yield UserCheckCount(userid=last_id, count=count)


def main():
    YT_PROXY = os.getenv("YT_PROXY", default="84.201.169.208:80")

    with open("config.json", "r") as f:
        config = json.load(f)

    client = YtClient(proxy=YT_PROXY, config=config)

    client.run_map(
        Operation_1(),
        source_table=INPUT_TABLE,
        destination_table=f"{BASE_TMP}/1_map"
    )

    client.run_sort(
        source_table=f"{BASE_TMP}/1_map",
        destination_table=f"{BASE_TMP}/1_map_sort",
        sort_by=["userid"]
    )
    client.run_reduce(
        Operation_2(),
        source_table=f"{BASE_TMP}/1_map_sort",
        destination_table=f"{BASE_TMP}/2_red",
        reduce_by=["userid"],
    )
    client.run_sort(
        source_table=f"{BASE_TMP}/2_red",
        destination_table=f"{BASE_TMP}/2_red_sort",
        sort_by=["count"]
    )

    data = client.read_table(f"{BASE_TMP}/2_red_sort")

    for row in list(data)[-1:-11:-1]:
        print((row["userid"], row["count"]))
        # data_2.append((row["userid"], row["count"]))
        # print(row["userid"], row["count"])

    # [print(*row) for row in data_2]
    # data_2.sort(key=lambda x: (-x[0], int(x[1].split("_")[-1])))
    # [print(*row) for row in data_2]


if __name__ == "__main__":
    main()
