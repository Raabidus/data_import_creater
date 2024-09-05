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
        df = pd.read_csv(file_path, encoding=dic.DEFAULT_ENCODING, delimiter=';', dtype=str, on_bad_lines='warn')
        print(f"CSV file {file_path} loaded successfully.")
        return df
    except pd.errors.ParserError as e:
        print(f"Error parsing the CSV file {file_path}: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred while loading {file_path}: {e}")
    return None

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

    # Identify new buildings
    new_buildings = df_all_data[~df_all_data['Číslo budovy'].isin(df_dumb_data['Číslo budovy'])]

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

# Main execution - když to chci spustit tady
# if __name__ == "__main__":
#     print("Running asset validation...")
#     asset_validation()
#     print("\nRunning buildings validation...")
#     buildings_validation()
#     print("\nValidation process completed.")