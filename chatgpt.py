import tabula
import pandas as pd

# Read the PDF file into a dataframe
# df = tabula.read_pdf("Monat_09.22.pdf", pages="all")
df = tabula.read_pdf("Monat_09.22.pdf", pages = "1", multiple_tables = True)

# Convert the dataframe to a Pandas dataframe
df = pd.DataFrame(df[0])
df.to_csv("chatgpt-temp.csv", index=False)

# Create a new empty dataframe to store the modified rows
modified_df = pd.DataFrame(columns=df.columns)

# Iterate over the rows in the original dataframe
for index, row in df.iterrows():
    # Split the row's values on linebreaks
    values = row.str.split("\n")
    
    # If the row has more than one value, add a new row for each value
    if len(values) > 1:
        for value in values:
            modified_df = modified_df.append({df.columns[i]: value for i in range(len(df.columns))}, ignore_index=True)
    # If the row has only one value, just add it to the modified dataframe
    else:
        modified_df = modified_df.append(row, ignore_index=True)

# Save the modified dataframe to a new CSV file
modified_df.to_csv("chatgpt.csv", index=False)
