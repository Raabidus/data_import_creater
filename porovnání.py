# import pandas as pd

# def compare_csv(file1, file2, key_columns=None):
#     # Load the CSV files into DataFrames with proper settings
#     df1 = pd.read_csv(file1, encoding='Windows-1250', delimiter=';', low_memory=False)
#     df2 = pd.read_csv(file2, encoding='Windows-1250', delimiter=';', low_memory=False)
    
#     # If specific columns are provided for comparison
#     if key_columns:
#         df1 = df1[key_columns]
#         df2 = df2[key_columns]
    
#     # Ensure both DataFrames have the same columns and index
#     df1 = df1.reindex(sorted(df1.columns), axis=1)
#     df2 = df2.reindex(sorted(df2.columns), axis=1)

#     # Ensure both have the same index
#     df1.index = range(len(df1))
#     df2.index = range(len(df2))

#     # Now compare the DataFrames
#     comparison = df1.compare(df2)
    
#     # Return the result
#     return comparison

# # Example usage
# differences = compare_csv(
#     '/home/kral-martin/workspace/dantem/KomercniBanka/kb_imports/04_asset.csv', 
#     '/home/kral-martin/workspace/dantem/KomercniBanka/kb_imports/04_majetek_2024.csv'
# )
# print(differences)
