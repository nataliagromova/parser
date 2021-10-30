import argparse
import os
import re
import csv


def parselogs(root, files, pl, result):
    global os_full_name
    for filename in files:
        path_to_file = root + '/' + filename
        if "txt" in filename and filename.replace(r".txt", ".end") in files:
            with open(path_to_file, 'r') as file:
                content = file.read()
                try:
                    num_of_tests = re.search(r".Number of tests\s+:\s+(\d+)", content).group(1)
                    num_of_success = re.search(r".Successes\s+:\s+(\d+)", content).group(1)
                    percentage = f'{float(num_of_success) / float(num_of_tests):.2%}'
                except Exception:
                    percentage = 'aborted'
        elif "txt" in filename and not filename.replace(r".txt",
                                                        ".end") in files or "end" in filename and not filename.replace(
            r".end", ".txt"):
            percentage = 'n/a'
        else:
            continue
        optimization = re.findall(r'_([^._]+)\.', filename)[-1]
        domain = os.path.basename(os.path.dirname(path_to_file))
        architecture = os.path.basename(os.path.dirname(os.path.dirname(path_to_file)))
        if pl == 'win':
            os_full_name = 'Windows'
        elif pl == 'mac':
            os_full_name = 'Macosx'
        elif pl == 'lin':
            os_full_name = 'Linux'
        result.append([os_full_name, architecture, domain, optimization, percentage])


def findlogs(path_to_logs, platform):
    platform_list = platform.split()
    result = []
    for pl in platform_list:
        for root, dirs, files in os.walk(path_to_logs):
            if pl in root and files:
                parselogs(root, files, pl, result)
    return result


def main(args):
    path_to_logs = args.dir_logs
    platform = args.platform
    if os.path.isdir(path_to_logs):
        result = findlogs(path_to_logs, platform)
    else:
        raise IsADirectoryError
    with open("result.csv", "w") as output:
        print("See statistics in result.csv")
        csv_out = csv.writer(output)
        csv_out.writerow(['OS', 'Architecture', 'Domain', 'Optimization', 'Pass rate'])
        for row in result:
            csv_out.writerow(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Log parser')
    parser.add_argument('dir_logs', type=str, help='Logs directory')
    parser.add_argument("--platform",
                        choices=["win", "lin", "mac"],
                        default="win lin mac",
                        type=str, help="Choose platform")
    args = parser.parse_args()

    main(args)
