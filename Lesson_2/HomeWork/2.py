import os
import json
import datetime
from typing import Iterable

from yt.wrapper import YtClient, TypedJob, yt_dataclass
from yt.wrapper.schema import RowIterator

BASE_TMP = "//tmp"
SRC_TABLE = "//home/data/tutorial/ytsaurus_intro/user_activity_log"
DEST_TABLE = "//home/test/local_dau"
# DEST_TABLE = "//home/students/donkandr/homework/les_2/table_2"


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
    timestamp: datetime.date
    action: str

@yt_dataclass
class DateCount:
    date: datetime.date
    users: int


class Operation_1(TypedJob):
    def __call__(self, user: UserRow) -> Iterable[UserFiltered]:
        yield UserFiltered(userid=user.userid,
                           timestamp=user.timestamp.date(),
                           action=user.action)

class Operation_2(TypedJob):
    def __call__(self, stream: RowIterator[UserFiltered]) -> Iterable[DateCount]:
        count = 0
        date = None

        for row in stream:
            date = row.timestamp
            count += 1

        assert date is not None
        yield DateCount(date=date, users=count)


def main():
    YT_PROXY = os.getenv("YT_PROXY", default="84.201.169.208:80")

    with open("config.json", "r") as f:
        config = json.load(f)

    client = YtClient(proxy=YT_PROXY, config=config)

    client.run_map(
        Operation_1(),
        source_table=SRC_TABLE,
        destination_table=f"{BASE_TMP}/1_map"
    )

    client.run_sort(
        source_table=f"{BASE_TMP}/1_map",
        destination_table=f"{BASE_TMP}/1_map_sort",
        sort_by=["timestamp", "userid"]
    )
    client.run_reduce(
        Operation_2(),
        source_table=f"{BASE_TMP}/1_map_sort",
        destination_table=DEST_TABLE,  # f"{BASE_TMP}/2_red"
        reduce_by=["timestamp", "userid"],
    )


if __name__ == "__main__":
    main()
