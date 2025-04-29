import csv
import json
import argparse
import sys

def csv_to_json(csv_file, json_file):
    data = []
    with open(csv_file) as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Convert CSV to JSON')

    parser.add_argument('-c', '--csv', type=str, help='CSV file path', required=True)
    parser.add_argument('-j', '--json', type=str, help='JSON file path', default='output.json')

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    try:
        csv_to_json(args.csv, args.json)
    except Exception as e:
        print(f"An error occurred, please ensure you have entered an input and : {e}")



if __name__ == '__main__':
    main()

# Normal run with python:
# python csv_etl.py --csv=sample.csv --json=sample1.json

# Help:
# python csv_etl.py --help

# Run with docker:
# docker run -it --rm --name sample-script -v "$PWD":/usr/src/app -w /usr/src/app python:3.13-slim python csv_etl.py --csv=sample.csv --json=sample1.json