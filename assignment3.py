import argparse
import csv
import re
from collections import Counter

def process_csv_data(file_path):
    image_hits = []
    browsers = Counter()
    image_pattern = re.compile(r'\.(jpg|jpeg|png|gif)$', re.IGNORECASE)
    browser_pattern = re.compile(r'(Firefox|Chrome|Safari|Opera|MSIE|Trident)')

    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            path, datetime_accessed, user_agent, status, size = row
            if image_pattern.search(path):
                image_hits.append(row)
            browser_match = browser_pattern.search(user_agent)
            if browser_match:
                browsers[browser_match.group(1)] += 1
            else:
                browsers['Other'] += 1

    return image_hits, browsers

def analyze_image_hits(image_hits):
    image_types = Counter()
    for hit in image_hits:
        path = hit[0]
        extension = path.split('.')[-1].lower()
        image_types[extension] += 1

    print("\nImage Hits by Type:")
    for img_type, count in image_types.items():
        print(f"  - {img_type.upper()}: {count}")

def analyze_browsers(browsers):
    print("\nBrowser Usage:")
    for browser, count in browsers.most_common():
        print(f"  - {browser}: {count}")

def main(file_path):
    print(f"Processing file: {file_path}...")
    image_hits, browsers = process_csv_data(file_path)
    
    print(f"\nTotal image hits: {len(image_hits)}")
    analyze_image_hits(image_hits)
    analyze_browsers(browsers)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", help="Path to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.file_path)
