# from tika import parser # pip install tika
# from tabulate import tabulate

# raw = parser.from_file('Monat_09.22.pdf')
# # print(raw['content'])

# #reads table from pdf file
# print(tabulate(raw['content']))

import camelot.io as camelot
import tabula
import os
import numpy

if os.path.exists("test2.html"):
  os.remove("test2.html")

file = "Monat_09.22.pdf"
# file = "Dienstplanentwurf Oktober 2022.pdf"

# extract all the tables in the PDF file
# abc = camelot.read_pdf(file)   #address of file location
abc = tabula.read_pdf(file, pages = "1", multiple_tables = True)
print(type(abc))
arr = numpy.array(abc)
print(type(arr))

print(arr)

# print the first table as Pandas DataFrame
# print(abc[0].df)
# print(abc[0])

# abc.export("camelot_tables.xlsx", f = "excel")

f = open("test2.html", "a")
# f.write(abc[0].df.to_string())
f.write(abc[0].to_string())
# f.write(str(arr))
f.close()

tabula.convert_into(file, "iris_first_table.csv")
