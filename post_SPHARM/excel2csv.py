import pandas as pd
import os

def excel_to_csv(excel_file_path, output_dir=None):
    # Read the Excel file
    xls = pd.ExcelFile(excel_file_path)
    
    # Get the output directory from the user or use the current directory
    if output_dir is None:
        output_dir = os.getcwd()
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Loop through each sheet in the Excel file
    for sheet_name in xls.sheet_names:
        # Read the sheet into a DataFrame
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        # Create a subdirectory named after the sheet
        sub_dir_path = os.path.join(output_dir, sheet_name)
        if not os.path.exists(sub_dir_path):
            os.makedirs(sub_dir_path)
        
        # Create a CSV file name based on the sheet name
        csv_file_name = f"{sheet_name}.csv"
        csv_file_path = os.path.join(sub_dir_path, csv_file_name)
        
        # Save the DataFrame to CSV inside the subdirectory
        df.to_csv(csv_file_path, index=False)
        
        print(f"Saved sheet '{sheet_name}' as '{csv_file_name}' in '{sub_dir_path}'")
    
# Example usage:
excel_to_csv("/path/to/your/Excel/spreadsheet.xlsx", "/path/to/your/output/directory/")
