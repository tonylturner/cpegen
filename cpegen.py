import csv
import argparse
import os
import sys

def clean_cpe_component(text):
    """Clean and transform a text component to adhere to CPE conventions."""
    return text.replace(" ", "_").replace("-", "_")

def generate_cpe(row):
    """Generate a CPE string from a list of components."""
    components = [clean_cpe_component(str(item)) for item in row]
    return "cpe:2.3:" + ":".join(components)

def process_csv_to_stdout(input_file):
    """Process a CSV file and print CPE strings to standard output."""
    try:
        with open(input_file, 'r', newline='') as infile:
            reader = csv.reader(infile)
            next(reader)  # Skip header
            for row in reader:
                if row:
                    print(generate_cpe(row))
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' does not exist. Please check the path.")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_csv_to_file(input_file, output_file):
    """Process a CSV file to generate CPE strings and write them to another CSV file."""
    try:
        with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            headers = next(reader)
            writer.writerow(headers + ['CPE String'])
            for row in reader:
                if row:
                    writer.writerow(row + [generate_cpe(row)])
        print(f"Output written to {output_file}")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' does not exist. Please check the path.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Generate CPE strings from a CSV file.')
    parser.add_argument('-f', '--file', required=True, help='Path to the input CSV file')
    parser.add_argument('-o', '--output', help='Optional output file path')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
    
    args = parser.parse_args()

    if args.output:
        process_csv_to_file(args.file, args.output)
    else:
        process_csv_to_stdout(args.file)

if __name__ == '__main__':
    main()
