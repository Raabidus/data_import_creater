import pandas as pd
import io
import os


# Constant for the default encoding
DEFAULT_ENCODING = 'Windows-1250'

# Clean the DataFrame by removing double quotes and replacing semicolons - přendat do kontrol a vybrat znaky na odmazání??
def clean_data(df):
    return df.apply(lambda x: x.replace(';', ',').replace('"', '') if isinstance(x, str) else x)


# Load data from a file
def load_file(file_path, encoding=DEFAULT_ENCODING):
    try:
        print(f'Loading file: {file_path}.')

        # Read file content with specified encoding, ignoring errors
        with open(file_path, 'r', errors='ignore', encoding=encoding) as f:
            data = f.read()

        # Create a file-like object from the data and read it into a DataFrame
        df = pd.read_csv(io.StringIO(data), delimiter=';', dtype='str', encoding=encoding)

        # Clean the DataFrame
        df = clean_data(df)

        return df
    
    except FileNotFoundError:
        print(f'Error: The file path "{file_path}" was not found')
    except pd.errors.EmptyDataError as e:
        print(f'Error: The file is empty')
    except pd.errors.ParserError as e:
        print(f'Error: The file could not be parsed')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return None


# Save selected columns from a DataFrame to a CSV file
def create_csv(df, output_path, columns_to_include, encoding=DEFAULT_ENCODING):
    try:
        # Select specific columns
        df_selected = df[columns_to_include]

        # Save the DataFrame to a CSV file with specified encoding
        df_selected.to_csv(output_path, index=False, sep=';', encoding=encoding)
        print(f'Successfully saved to {output_path} with encoding {encoding}')

    except Exception as e:
        print(f'An error occurred while saving the file: {e}')


# Function to process a single file
def process_file(input_path, output_name, encoding=DEFAULT_ENCODING):
    df = load_file(input_path, encoding=DEFAULT_ENCODING)
    if df is not None:
        # Display available columns
        print("\nAvailable columns in the file:")
        for idx, column in enumerate(df.columns):
            print(f"{idx}: {column}")

        # Inform the user to select columns by index
        selected_columns = input("\nEnter the column indices to include in the output file, separated by commas: ")
        try:
            selected_indices = [int(idx) for idx in selected_columns.split(',')]
            columns_to_include = [df.columns[idx] for idx in selected_indices]

            # Ensure the output file has a .csv extension
            if not output_name.endswith('.csv'):
                output_name += '.csv'

            # Create the 'kb_imports' folder if it doesn't exist
            output_folder = os.path.join(os.path.dirname(__file__), 'kb_imports')
            os.makedirs(output_folder, exist_ok=True)

            # Define the full output path
            output_path = os.path.join(output_folder, output_name)
            
            # Save the selected columns to the output CSV file
            create_csv(df, output_path, columns_to_include, encoding)
        except ValueError:
            print("Invalid input for column indices. Aborting operation.")

    else:
        print(f'Skipping file {input_path} due to loading issues.')


# Select encoding of import csv file
def select_encoding():
    print("Select the encoding for the output CSV file:")
    print("1. utf-8")
    print("2. Windows-1250")
    print("3. ANSI")
    encoding_choice = input("Enter the number corresponding to your choice: ")

    if encoding_choice == '1':
        return 'utf-8'
    elif encoding_choice == '2':
        return 'Windows-1250'
    elif encoding_choice == '3':
        return 'ANSI'
    else:
        print("Invalid choice, defaulting to utf-8")
        return 'utf-8'
