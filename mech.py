import mechanize

file = "Monat_09.22.pdf"
# file = "Dienstplanentwurf Oktober 2022.pdf"

br = mechanize.Browser()
br.open("https://pdftables.com")
# for f in br.forms():
#     print(f)

br.select_form(name="order")
br.form.add_file(open(file), 'text/plain', file)
# br.form.set_all_readonly(False)
br.submit()