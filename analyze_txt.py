import re
from pathlib import Path
import argparse
import csv

def parse_timestamps(file_path: Path) -> list:
    timestamps = []

    with file_path.open() as file:
        lines = file.readlines()
        for i in range(len(lines)):
            if 'stamp:' in lines[i].strip():
                sec_line = lines[i+1].strip()
                nanosec_line = lines[i+2].strip()
                sec_match = re.search(r'sec:\s(\d+)', sec_line)
                nanosec_match = re.search(r'nanosec:\s(\d+)', nanosec_line)
                if sec_match and nanosec_match:
                    sec = int(sec_match.group(1))
                    nanosec = int(nanosec_match.group(1))
                    timestamps.append((sec, nanosec))

    if not timestamps:
        print("No timestamps found.")
        return

    first_timestamp = timestamps[0]
    last_timestamp = timestamps[-1]

    first_time = first_timestamp[0] + first_timestamp[1] / 1e9
    last_time = last_timestamp[0] + last_timestamp[1] / 1e9

    return [file_path.as_posix(), len(timestamps), first_time, last_time]

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "root_dir",
        help="root directory where the file to be analyzed is located",
    )
    parser.add_argument(
        "file_name",
        help="path of the scenario to load evaluator settings",
    )
    parser.add_argument(
        "-c",
        "--csv_output",
        default="./analysis.csv",
        help="csv output file path"
    )
    args = parser.parse_args()
    target_file_paths = Path(args.root_dir).glob(f"**/{args.file_name}")
    csv_file = Path(args.csv_output).open("w")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["File to be analyzed", "Number of Topic", "Start", "End"])
    for topic_file in target_file_paths:
        csv_writer.writerow(parse_timestamps(topic_file))
    csv_file.close()


if __name__ == "__main__":
    main()
