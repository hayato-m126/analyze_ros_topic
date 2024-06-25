import argparse
import csv
from pathlib import Path

from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus

# from rosidl_runtime_py.utilities import get_message
from rclpy.serialization import deserialize_message

from bag import create_reader


def parse_timestamps(file_path: Path) -> list:
    timestamps = []

    reader = create_reader(file_path.as_posix())
    # type_map = {}
    # for topic_type in reader.get_all_topics_and_types():
    #     type_map[topic_type.name] = topic_type.type

    while reader.has_next():
        topic, data, t = reader.read_next()
        if topic == "/diagnostic/control_evaluator/metrics":
            # msg_type = get_message(type_map[topic])
            msg_deserialized: DiagnosticArray = deserialize_message(
                data, DiagnosticArray
            )
            if len(msg_deserialized.status) == 0:
                continue
            status0: DiagnosticStatus = msg_deserialized.status[0]
            if (
                status0.name == "autonomous_emergency_braking: aeb_emergency_stop"
                and status0.values[0].key == "decision"
                and status0.values[0].value == "stop"
            ):
                timestamps.append(
                    (
                        msg_deserialized.header.stamp.sec,
                        msg_deserialized.header.stamp.nanosec,
                    )
                )

    if not timestamps:
        print("No timestamps found.")
        return [file_path.as_posix(), 0, 0, 0]

    first_timestamp = timestamps[0]
    last_timestamp = timestamps[-1]

    first_time = first_timestamp[0] + first_timestamp[1] / 1e9
    last_time = last_timestamp[0] + last_timestamp[1] / 1e9

    return [file_path.as_posix(), len(timestamps), first_time, last_time]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "root_dir",
        default="/home/hyt/out/auto/planning_control",
        help="root directory where the file to be analyzed is located",
    )
    parser.add_argument(
        "-c", "--csv_output", default="./analysis.csv", help="csv output file path"
    )
    args = parser.parse_args()
    target_file_paths = Path(args.root_dir).glob("**/result_bag")
    csv_file = Path(args.csv_output).open("w")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Bag to be analyzed", "Number of Topic", "Start", "End"])
    for bag_path in sorted(target_file_paths):
        # print(bag_path)
        csv_writer.writerow(parse_timestamps(bag_path))
    csv_file.close()


if __name__ == "__main__":
    main()
