import os
import data_import_creater as dic

#TO-DO
    # když bude už import existovat - vypsat upozrnení a nabídnou možnst přepsání, nebo uložení pod novým názvem

# ASI ZBYTEČNÉ - BUDOVY JSOU Z POSLEDNÍ INV A NÁSLEDNĚ SE ŘEŠÍ VALIDACE BUDOVY Z MINULÉ INV VS id BUDOOVY V ALL-data
# def buildings_import(df):
#     try:
#         columns_to_include = ['building', 'adress'] # DOPLNIT
#         output_folder = os.path.join(os.path.dirname(__file__), 'kb_imports')
#         os.makedirs(output_folder, exist_ok=True)
#         output_path = os.path.join(output_folder, '02_buildings.csv')
#         dic.create_csv(df, output_path, columns_to_include, dic.DEFAULT_ENCODING)
#     except Exception as e:
#         print(f"An error occurred during rooms buildings: {str(e)}")


# Stejně jako u budov
# def rooms_import(df):
#     try:
#         columns_to_include = ['Číslo budovy', 'Popis místnosti', 'Zvyk.kód místn.', 'Lokalita'] # DOPLNIT
#         output_folder = os.path.join(os.path.dirname(__file__), 'kb_imports')
#         os.makedirs(output_folder, exist_ok=True)
#         output_path = os.path.join(output_folder, '03_rooms.csv')
#         dic.create_csv(df, output_path, columns_to_include, dic.DEFAULT_ENCODING)
#     except Exception as e:
#         print(f"An error occurred during rooms import: {str(e)}")

def asset_import(df):
    try:
        columns_to_include = ['ID majetku', 'Číslo štítku', 'Popis', 'Stav', 'Gesce',
                            'Typ majetku', 'SKP', 'Typ nákl.', 'Středisko',
                            'Lokalita', 'Číslo budovy', 'Místnost', 'Zvyk.kód místn.',
                            'Popis místnosti', 'Výr. číslo', 'Kategorie', 'Dat.pořízení',
                            'Celková cena', 'Zůstatková cena', 'Účet', 'Jméno odp.osoby',
                            'HROM'
                            ]
        output_folder = os.path.join(os.path.dirname(__file__), 'kb_imports')
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, '04_asset.csv')

        # když už bude soubor 04_asset existovat ve složce
        # if os.path.exists(output_path):
        #     choice = input(f"{output_path} already exist. Do yo want to rename the new
        #                    file or overwrite the existing one? (rename/overwrite): ").strip().lower()
        #     if choice == 'rename':
        #         new_filename = input("Enter thr new filenam (without extension)").strip()
        #         output_path = os.path.join(output_folder, f"{new_filename}")
        #     elif choice != 'overwrite':
        #         print("Invalid choice. Aborting operation")
        #         return

        dic.create_csv(df, output_path, columns_to_include, dic.DEFAULT_ENCODING)
    except Exception as e:
        print(f"An error occurred during asset: {str(e)}")

def catalog_import(df):
    pass

def founds_import(df):
    pass