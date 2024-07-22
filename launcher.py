import os
import data_import_creater as dic
import komercni_banka as kb
import data_validation_kb as dvkb

def main():
    print("Select an operation:")
    print("1. Data Import Creator")
    print("2. Data Validation")
    choice = input("Enter the number corresponding to your choice: ")

    if choice == '1':
        print("Select an option:")
        print("1. Open import creater")
        print("2. Komerční Banka")
        sub_choice = input("Enter the number corresponding to your choice: ")

        if sub_choice == '1':
            input_path = input("Enter the path of the CSV file to load: ")
            output_name = input("Enter the desired name for the output CSV file (without extension): ")
            encoding = dic.DEFAULT_ENCODING  # Default encoding

            dic.process_file(input_path, output_name, encoding)

        elif sub_choice == '2':
            input_path = input("Enter the path of the CSV file to load: ")
            encoding = dic.DEFAULT_ENCODING  # Default encoding
            df = dic.load_file(input_path, encoding)

            if df is not None:
                print("Select an export option:")
                print("1. Budovy")
                print("2. Mistnosti")
                print("3. Majetek")
                print("9. All")
                export_choice = input("Enter the number corresponding to your choice: ")

                if export_choice == '1':
                    kb.buildings_import(df)
                elif export_choice == '2':
                    kb.rooms_import(df)
                elif export_choice == '3':
                    kb.asset_import(df)
                elif export_choice == '9':
                    kb.buildings_import(df)
                    kb.rooms_import(df)
                    kb.asset_import(df)
                else:
                    print("Invalid choice. Please run the script again and select a valid option.")
            else:
                print("Failed to load the CSV file. Please check the file path and encoding.")
        else:
            print("Invalid choice. Please run the script again and select a valid option.")
    elif choice == '2':
        print("Select a validation type:")
        print("1. Asset Validation")
        print("2. Buildings Validation")
        validation_choice = input("Enter the number corresponding to your choice: ")

        if validation_choice == '1':
            dvkb.asset_validation()  # Call the asset validation function
        elif validation_choice == '2':
            dvkb.buildings_validation()  # Call the buildings validation function
        else:
            print("Invalid choice. Please run the script again and select a valid option.")
    else:
        print("Invalid choice. Please run the script again and select a valid option.")


if __name__ == '__main__':
    main()
