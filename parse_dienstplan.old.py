import tabula
import camelot.io as camelot
import pandas as pd
import warnings
warnings.filterwarnings(action='ignore', category=FutureWarning)

filename = "Monat_09.22.pdf"
# filename = "Dienstplanentwurf Oktober 2022.pdf"

########################

df = tabula.read_pdf(filename, pages = "all", multiple_tables = True, stream=True)
# df = camelot.read_pdf(filename, pages = "1-end", process_background=True)

# df = df[0].df
# print(type(df))

df[0].to_excel("test_0.xlsx", index=False)
# df[1].to_excel("test_1.xlsx", index=False)
df[2].to_excel("test_2.xlsx", index=False)
# df2 = df[2]
df = df[0]

########################################

# Create a new empty dataframe to store the modified rows
modified_df = pd.DataFrame(columns=df.columns)

print(df.loc[7])

# Iterate over the rows in the original dataframe
for index, row in df.iterrows():

    # Split the row's values on linebreaks
    values = row.str.split("\r")
    
    # If the row has more than one value, add a new row for each value
    if len(values[0]) > 1:
        # print(str(index))
        for i in range(len(values[0])):
            # print(values[i])
            for k in range(len(df.columns)):
                # if index == 6 and i == 0:
                print(k)
                print(i)
                # print(values[k][i])
                if values[k] == values[k]: print(values[k][i])
            # print(len(values[0]))
            # print(i)
            # print(values[i])
            modified_df = modified_df.append({df.columns[k]: values[k][i] if values[k] == values[k] else '' for k in range(len(df.columns))}, ignore_index=True)
    # If the row has only one value, just add it to the modified dataframe
    else:
        modified_df = modified_df.append(row, ignore_index=True)

# Save the modified dataframe to a new CSV file
modified_df.to_excel("test_modified.xlsx", index=False)

########################################

df2.at[0, "OPI Süd"] = "Tag"
df2.at[0, "Unnamed: 0"] = "Datum"
df2.drop(df2.columns[[3, 5, 9, 13]], axis=1,inplace=True)
df2.columns = df2.loc[0]
df2.drop([0], axis=0, inplace=True)

df2.to_excel("test_modified2.xlsx", index=False)

