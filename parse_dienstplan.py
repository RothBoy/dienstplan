import tabula
import pandas as pd
import warnings
import datetime

warnings.filterwarnings(action='ignore', category=FutureWarning)

# filename = "res/Monat_09.22.pdf"
# filename = "res/Dienstplanentwurf Oktober 2022.pdf"
filename = "res/Dienstplanentwurf 2023-01-2023 Januar Stand 17.11.2022.pdf"

########################################

# df = tabula.read_pdf(filename, pages = "all", multiple_tables = True, stream=True, guess=False, area = [75.5, 18, 440, 701.5],
# columns=[92.5, 153.75, 211.5, 277, 333, 395.5, 457.5, 517.5, 588, 644.75])
df = tabula.read_pdf(filename, pages="1", stream=True, guess=False, area=[50, 17.5, 470, 765],
                     columns=[98.5, 165.5, 229, 300.5, 362, 431, 499, 564, 641, 704])

# df = tabula.read_pdf(filename, pages = "2", lattice=True)

########################################

# df[0].rename(columns={'Unnamed: 0':'Tag'}, inplace=True)

# df[2].rename(columns={'Unnamed: 0':'Tag'}, inplace=True)
# df[2].rename(columns={'Unnamed: 1':'Datum'}, inplace=True)
# df[2].drop(df[2].columns[[7]], axis=1,inplace=True)

########################################

# df[0].to_excel("test_0.xlsx", index=False)
# df[2].to_excel("test_2.xlsx", index=False)

########################################

# print(df[0].eq("Mohr").any(0))
# print(df[0].at[df[0].eq("Mohr").any(1), df[0].eq("Mohr").any(0)])

# print(df[0][df[0].eq("Mohr").any(axis=1)])
# print(df[0].loc[:,df[0].eq("Mohr").any(axis=0)])

employee = "Mohr"

for i in df[0][df[0].eq(employee).any(axis=1)].index:
    print(str(df[0].iloc[i, 0] + ": " + df[0].columns[df[0].loc[i].eq(employee)]))
    [day, month, year] = df[0].iloc[i, 0][3:].split(".")
    date_start = datetime.datetime(int(year), int(month), int(day))
    date_end = date_start + datetime.timedelta(days=1)
    # print(date_end.strftime("%Y-%m-%d"))

# dates = df[0].loc[:,'Datum'][df[0].eq("Mohr").any(axis=1)]
# station = df[0].columns

# df2 = df[0].drop(df[0][df[0].eq("Mohr").any(axis=1)] != "Mohr")
