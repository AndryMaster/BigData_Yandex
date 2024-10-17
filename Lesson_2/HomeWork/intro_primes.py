import os
import json
from typing import Iterable

from yt.wrapper import YtClient, TypedJob, yt_dataclass
from yt.wrapper.schema import RowIterator

BASE_PATH = "//home/students/donkandr/tmp/test/1"
INPUT_TABLE = f"{BASE_PATH}/input_range"


@yt_dataclass
class InputRange:
    start: int
    end: int

@yt_dataclass
class PrimeCheckProblem:
    number: int

@yt_dataclass
class PrimeCheckResult:
    fake_key: int
    number: int
    is_prime: bool

@yt_dataclass
class PrimesCount:
    primes_count: int


class Operation_1(TypedJob):
    def __call__(self, input_range: InputRange) -> Iterable[PrimeCheckProblem]:
        for n in range(input_range.start, input_range.end + 1):
            yield PrimeCheckProblem(n)

class Operation_2(TypedJob):
    def __call__(self, check_num: PrimeCheckProblem) -> Iterable[PrimeCheckResult]:
        def is_prime(n):
            if n <= 1:
                return False
            elif n == 2:
                return True
            k = 3
            while k * k <= n:
                if n % k == 0:
                    return False
                k += 2
            return True

        yield PrimeCheckResult(
            fake_key=0,
            number=check_num.number,
            is_prime=is_prime(check_num.number))

class Operation_3(TypedJob):
    def __call__(self, stream: RowIterator[PrimeCheckResult]) -> Iterable[PrimesCount]:
        count = 0

        for row in stream:
            if row.is_prime:
                count += 1

        yield PrimesCount(count)


def main():
    YT_PROXY = os.getenv("YT_PROXY")

    if YT_PROXY == None or YT_PROXY == "":
        raise RuntimeError("Environment variable YT_PROXY is empty")

    with open("config.json", "r") as f:
        config = json.load(f)

    client = YtClient(proxy=YT_PROXY, config=config)

    # input
    data = [InputRange(start=1, end=100_000)]
    client.write_table_structured(INPUT_TABLE, InputRange, data)

    # map reduce
    client.run_map(
        Operation_1(),
        source_table=INPUT_TABLE,
        destination_table=f"{BASE_PATH}/op_1_res"
    )
    client.run_map(
        Operation_2(),
        source_table=f"{BASE_PATH}/op_1_res",
        destination_table=f"{BASE_PATH}/op_2_res"
    )
    client.run_sort(
        source_table=f"{BASE_PATH}/op_2_res",
        destination_table=f"{BASE_PATH}/op_2_res_sort",
        sort_by=["fake_key"]
    )
    client.run_reduce(
        Operation_3(),
        source_table=f"{BASE_PATH}/op_2_res_sort",
        destination_table=f"{BASE_PATH}/result_primes",
        reduce_by=["fake_key"]
    )


if __name__ == "__main__":
    os.environ["YT_PROXY"] = "84.201.169.208:80"
    main()
