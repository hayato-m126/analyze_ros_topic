import yaml
from pathlib import Path



def count_topic(file_path: Path) -> None:
    timestamps = []

    with file_path.open() as echo_file:
        # https://analytics-note.xyz/programming/python-yaml/
        yaml_obj = yaml.safe_load_all(echo_file)

        for topic in yaml_obj:
            print(topic)
            print(type(topic))

    # first_timestamp = timestamps[0]
    # last_timestamp = timestamps[-1]

    # first_time = first_timestamp[0] + first_timestamp[1] / 1e9
    # last_time = last_timestamp[0] + last_timestamp[1] / 1e9

    # print(f"Number of timestamps: {len(timestamps)}")
    # print(f"First timestamp: {first_time} seconds")
    # print(f"Last timestamp: {last_time} seconds")

# ファイルのパスを指定してください
file_path = Path("sample/stop.yaml")
count_topic(file_path)
