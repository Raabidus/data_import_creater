import pandas as pd
import os
import data_import_creater as dic


# TO-DO
    # otestovat - přidat do asset "chyná data a spustit"
    # kontroly budovy - csv s budovami z minulého roku x nové budovy - přidat do importu nakonec?
    # kontroly místnosti

# Check for duplicates and missing IDs
# Generate the validation report
# Save the valid entries to a new CSV file


def asset_validation():
    try:
        output_folder = os.path.join(os.path.dirname(__file__), 'kb_imports')
        asset_file_path = os.path.join(output_folder, '04_asset.csv')

        if not os.path.exists(asset_file_path):
            print(f"{asset_file_path} does not exist.")
            return

        # Load the CSV file, handling bad lines
        try:
            df = pd.read_csv(asset_file_path, encoding=dic.DEFAULT_ENCODING, delimiter=';', dtype=str, on_bad_lines='warn')
            print("CSV file loaded successfully with problematic lines skipped.")
        except pd.errors.ParserError as e:
            print(f"Error parsing the CSV file: {e}")
            return
        
        # Check for duplicates and missing IDs
        duplicates = df[df.duplicated('ID majetku', keep=False)]
        missing_ids = df[df['ID majetku'].isnull() | (df['ID majetku'].str.strip() == '')]

        # Generate the validation report
        report_path = os.path.join(output_folder, 'validation_report.txt')
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

        # Inform the user of the validation results
        if not duplicates.empty or not missing_ids.empty:
            print(f"Validation issues found. See the report at {report_path}")
        else:
            print("No validation issues found.")

        # Save the valid entries to a new CSV file
        valid_df = df.drop_duplicates('ID majetku').dropna(subset=['ID majetku'])
        valid_df = valid_df[valid_df['ID majetku'].str.strip() != '']
        valid_output_path = os.path.join(output_folder, '04_asset_valid.csv')
        valid_df.to_csv(valid_output_path, index=False, encoding=dic.DEFAULT_ENCODING)
        print(f"Valid entries saved to {valid_output_path}")

    except Exception as e:
        print(f"An error occurred during asset validation: {str(e)}")