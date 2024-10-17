import os
import json

from yt.wrapper import YtClient

BASE_DIR = "//home/data/tutorial/ytsaurus_intro/examine"


def main():
    YT_PROXY = os.getenv("YT_PROXY", default="84.201.169.208:80")
    if YT_PROXY is None or YT_PROXY == "":
        raise RuntimeError("Environment variable YT_PROXY is empty")

    with open("config.json", "r") as f:
        config = json.load(f)
    client = YtClient(proxy=YT_PROXY, config=config)

    data = []
    for table_path in client.search(
            root=BASE_DIR,
            node_type=["table"],
    ):
        path = table_path.split('/')[-1]
        chunk_count = client.get(f"{table_path}/@chunk_count")
        compressed_data_size = client.get(f"{table_path}/@compressed_data_size")
        data.append((path, chunk_count, compressed_data_size))
        # print(table_path, chunk_count, compressed_data_size)

    data.sort(key=lambda x: (x[1], x[2]), reverse=True)
    [print(*row) for row in data]


if __name__ == "__main__":
    main()
