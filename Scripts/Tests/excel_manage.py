import pandas as pd

# Specify the path to the XLSX file
xlsx_file = './InfoMapa.xlsx'

# Read the XLSX file into a DataFrame
df = pd.read_excel(xlsx_file)

# Print the DataFrame
print(df)