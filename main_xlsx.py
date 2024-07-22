import pandas as pd
import io
import os

########
#dependencies
        # python 3.12 higher
        # pandas
        # io
        # os
# TO DO
# funkce pro načtení souborů, soubor je vždy csv a má jeden pracovní sheet
# soubory, ze kterých seberou data:
    # z db - buď ručně nebo se napojit:
        # budovy, místnosti, nálezy, pžíznaky: vytištěno a catalog
    # soubor ALL-data.csv, místnosti_csc, harmonogram
# vytvořit importy:
    # 02_budovy
    # 03_místnosti
    # 04_majetek
    # 06_katalog
########

# Define a constant for the encoding
ENCODING = 'Windows-1250'

# Load data from a file
def load_file(file_path):
    try:
        print(f'Loading file: {file_path}.')

        # Read file content with specified encoding, ignoring errors
        with open(file_path, 'r', errors='ignore', encoding=ENCODING) as f:
            data = f.read()

        # Create a file-like object from the data and read it into a DataFrame
        df = pd.read_csv(io.StringIO(data), delimiter=';', dtype='str', encoding=ENCODING)
        
        # Replace semicolons with commas within text fields in the DataFrame
        df = df.applymap(lambda x: x.replace(';', ',') if isinstance(x, str) else x)

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
def create_csv(df, output_path, columns_to_include):
    try:
        # Select specific columns
        df_selected = df[columns_to_include]

        # Save the DataFrame to a CSV file with specified encoding
        df_selected.to_csv(output_path, index=False, sep=';', encoding=ENCODING)
        print(f'Successfully saved to {output_path}')

    except Exception as e:
        print(f'An error occurred while saving the file: {e}')


# Function to process a single file
def process_file(input_path, output_name):
    df = load_file(input_path)
    if df is not None:
        # Display available columns
        print("\nAvailable columns in the file:")
        for idx, column in enumerate(df.columns):
            print(f"{idx}: {column}")

        # Inform the user to select columns by index
        selected_columns = input("\nEnter the column indices to include in the output file, separated by commas: ")
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
        create_csv(df, output_path, columns_to_include)
    else:
        print(f'Skipping file {input_path} due to loading issues.')

# Instruct user for input file and output filename
input_path = input("Enter the path of the CSV file to load: ")
output_name = input("Enter the desired name for the output CSV file (without extension): ")

# Process the file
process_file(input_path, output_name)