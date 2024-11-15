import pandas as pd
import os
import data_import_creater as dic

OUTPUT_FOLDER = 'kb_imports'

def get_file_path(filename):
    """Generate the full file path."""
    return os.path.join(os.path.dirname(__file__), OUTPUT_FOLDER, filename)

def load_csv(file_path):
    """Load a CSV file and handle potential errors."""
    try:
        df = pd.read_csv(file_path, encoding=dic.DEFAULT_ENCODING, delimiter=';', 
                         on_bad_lines='warn', encoding_errors='ignore')
        print(f"CSV file {file_path} loaded successfully.")
        return df
    except pd.errors.ParserError as e:
        print(f"Error parsing the CSV file {file_path}: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred while loading {file_path}: {e}")
    return None

def convert_csv_delimiter(input_file_path):
    """Convert a CSV file from comma to semicolon as a delimiter."""
    output_file_path = get_file_path(input("Insert file name: "))  # Define the output file name

    try:
        # Step 1: Load the original CSV with comma delimiter
        df = pd.read_csv(input_file_path, delimiter=',', encoding='utf-8', dtype=str)
        
        # Step 2: Save the DataFrame with semicolon delimiter, preserving commas in the address
        df.to_csv(output_file_path, sep=';', index=False, encoding=dic.DEFAULT_ENCODING, quotechar='"')
        
        print(f"Successfully converted '{input_file_path}' to '{output_file_path}' with semicolon delimiter.")
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_validation_report(duplicates, missing_ids, report_path):
    """Generate a validation report."""
    with open(report_path, 'w', encoding='utf-8') as report_file:
        if not duplicates.empty:
            report_file.write("Duplicate ID majetku found:\n")
            report_file.write(duplicates.to_string(index=False))
            report_file.write("\n\n")

        if not missing_ids.empty:
            report_file.write("Missing or empty ID majetku found:\n")
            report_file.write(missing_ids.to_string(index=False))
            report_file.write("\n\n")

        if duplicates.empty and missing_ids.empty:
            report_file.write("No duplicates or missing IDs found.\n")

def asset_validation():
    """Validate asset data, generate a report, and save valid entries."""
    asset_file_path = get_file_path('04_asset.csv')
    df = load_csv(asset_file_path)
    
    if df is None:
        return

    # Check for duplicates and missing IDs
    if 'ID majetku' not in df.columns:
        print("Error: Column 'ID majetku' not found in the asset data.")
        return

    duplicates = df[df.duplicated('ID majetku', keep=False)]
    missing_ids = df[df['ID majetku'].isnull() | (df['ID majetku'].str.strip() == '')]

    # Generate the validation report
    report_path = get_file_path('asset_validation_report.txt')
    generate_validation_report(duplicates, missing_ids, report_path)

    # Inform the user of the validation results
    if not duplicates.empty or not missing_ids.empty:
        print(f"Validation issues found. See the report at {report_path}")
    else:
        print("No validation issues found.")

    # Save the valid entries to a new CSV file
    valid_df = df.drop_duplicates('ID majetku').dropna(subset=['ID majetku'])
    valid_df = valid_df[valid_df['ID majetku'].str.strip() != '']
    valid_output_path = get_file_path('04_asset_valid.csv')
    valid_df.to_csv(valid_output_path, index=False, encoding=dic.DEFAULT_ENCODING, sep=';')
    print(f"Valid entries saved to {valid_output_path}")

def buildings_validation():
    """Validate buildings data and update with new buildings if found."""
    all_data_buildings_file_path = input("Enter path to all_data file: ")
    dumb_data_file_path = input("Enter path to last year db dumb data file: ")

    df_all_data = load_csv(all_data_buildings_file_path)
    df_dumb_data = load_csv(dumb_data_file_path)

    if df_all_data is None or df_dumb_data is None:
        return

    # print("Dumb Data Sample:")
    # print(df_dumb_data.head())
    # print("Dumb Data Columns:")
    # print(df_dumb_data.columns)  # Print column names for debugging

    # Check if required columns exist
    if 'Číslo budovy' not in df_all_data.columns:
        print("Error: Column 'Číslo budovy' not found in the all_data file.")
        return
    if 'building' not in df_dumb_data.columns:
        print("Error: Column 'building' not found in the dumb data.")
        return

    # Identify new buildings
    new_buildings = df_all_data[~df_all_data['Číslo budovy'].isin(df_dumb_data['building'])]

    if new_buildings.empty:
        print("No new buildings found.")
    else:
        print(f"Found {len(new_buildings)} new buildings.")

        # Sort the new buildings and append to existing data
        new_buildings_sorted = new_buildings.sort_values(by='Číslo budovy')
        df_updated = pd.concat([df_dumb_data, new_buildings_sorted], ignore_index=True)

        # Save the updated dataframe
        df_updated.to_csv(dumb_data_file_path, sep=';', encoding=dic.DEFAULT_ENCODING, index=False)
        print(f"Updated buildings data saved to {dumb_data_file_path}.")

    # Generate a report for new buildings
    report_path = get_file_path('buildings_validation_report.txt')
    with open(report_path, 'w', encoding='utf-8') as report_file:
        if new_buildings.empty:
            report_file.write("No new buildings found.\n")
        else:
            report_file.write(f"Found {len(new_buildings)} new buildings:\n")
            report_file.write(new_buildings.to_string(index=False))

    print(f"Buildings validation report saved to {report_path}")


def rooms_validation():
    """Validate rooms data and update with new rooms if found.
    Rooms from dumb x rooms from ALL-data"""

    all_data_rooms_file_path = input("Enter path to ALL-data file: ")
    dumb_rooms_data_file_path = input("Enter path to last year db dumb data file:")

    df_all_data = load_csv(all_data_rooms_file_path)
    df_dumb_data = load_csv(dumb_rooms_data_file_path)

    if df_all_data is None or df_dumb_data is None:
        return
    
    if 'Místnost' not in df_all_data:
        print("Error: Column 'Místnost' not found in the ALL-data file.")
        return
    if 'room' not in df_dumb_data:
        print("Error: Columnt 'room' not found in the dumb data.")
        return

    # Identify new rooms
    new_rooms = df_all_data[~df_all_data['Místnost'].isin(df_dumb_data['room'])]

    if new_rooms.empty:
        print("No new rooms dound.")
    else:
        print(f"Found {len(new_rooms)} new buildings.")

        # Appedn to existing data
        new_rooms_sorted = new_rooms.sort_values(by='Místnost')
        df_updated = pd.concat([df_dumb_data, new_rooms_sorted], ignore_index=True)

        # Safe updated df
        df_updated.to_csv(dumb_rooms_data_file_path, sep=';', encoding=dic.DEFAULT_ENCODING, index=False)
        print(f"Updated rooms data saved to {dumb_rooms_data_file_path}")

    # Generate a report for new buildings
    report_path = get_file_path('rooms_validation_report.txt')
    with open(report_path, 'w', encoding='utf-8') as report_file:
        if new_rooms.empty:
            report_file.write("No new buildings found.\n")
        else:
            report_file.write(f"Found {len(new_rooms)} new rooms:\n")
            report_file.write(new_rooms.to_string(index=False))

    print(f"Rooms validation report saved to {report_path}")






    
# Main execution
if __name__ == "__main__":
    # Example usage of convert_csv_delimiter
    # input_csv_path = input("Enter the path to the input CSV file (with comma delimiter): ")
    # convert_csv_delimiter(input_csv_path)

    # Validate asset data
    # print("Running asset validation...")
    # asset_validation()
    
    # Validate buildings data
    # print("\nRunning buildings validation...")
    # buildings_validation()

    # Validate rooms data
    print("validate rooms")
    rooms_validation()

    print("\nValidation process completed.")
