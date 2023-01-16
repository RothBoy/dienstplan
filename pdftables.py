import pdftables_api
import requests
from pprint import pprint

file = "Monat_09.22.pdf"
# file = "Dienstplanentwurf Oktober 2022.pdf"
filedata = open(file, "rb")

response = requests.post('https://pdftables.com/upload', files={'files': filedata})
print(response.status_code)
# pprint(response.json()['headers'])
# pprint(response.json())

# f = open("test2.txt", "a")
# f.write(abc[0].to_string())
# f.close()
