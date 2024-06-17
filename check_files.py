import csv
import os

# Path to your CSV file
csv_file_path = "/path/to/your/CSV/file.csv"

def check_file_existence(csv_file_path):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        missing_files = []
        for row in reader:
            for file_path in row:
                # Check if the file path is not empty and the file does not exist
                if file_path and not os.path.exists(file_path):
                    missing_files.append(file_path)
    
    if missing_files:
        print(f"Missing Files ({len(missing_files)}):")
        for file_path in missing_files:
            print(file_path)
    else:
        print("All files exist.")

# Run the check
check_file_existence(csv_file_path)
