import pytablewriter
import os
import re
from pytablewriter import MarkdownTableWriter
from operator import itemgetter

clientiITO = []
clientiNonITO = []
clientiITOHTML = []

rootdir = '.'
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith('.md'):
            is_main = False
            f = open(os.path.join(subdir,file), 'r')
            cliente = []
            clienteITO = False
            for _ in range(5):
                next(f)
            nome = f.readline().strip()[2:]
            cliente.append("[" + nome +"]("+os.path.join(subdir,file)+")")
            while line := f.readline():
                if "## ITO H24" in line.strip():
                    is_main = True
                    CR = ""
                    clienteITO = True
                    line = f.readline()
                    while line := f.readline():
                        if line[0:2] == "* ":
                            splitted = line[2:].split(':', 1)
                            match = re.search(r'\[.*?\]\((.*?)\)', splitted[0])
                            if match:
                                # Replace the link with the desired link
                                new_link = os.path.join(subdir, "") + match.group(1)
                                splitted[0] = splitted[0].replace(match.group(1), new_link)
                            CR += splitted[0] + " ITO H24: "+ splitted[1] + " <br/>"
                            ############################# FOR HTML FILE #####################################
                            match = re.search(r'CR\d+', splitted[0])
                            progetto = match.group() + ": " + splitted[1]
                            # print(progetto)
                            if clientiITOHTML == [] or clientiITOHTML[-1].get('nome_cliente') != nome:
                                clientiITOHTML.append({
                                    'nome_cliente': nome,
                                    'progetti': [progetto]
                                })
                            else:
                                clientiITOHTML[-1]['progetti'].append(match.group() + ": " + splitted[1])
                            #################################################################################
                            print("Il progetto "+ progetto + " del cliente "+nome+" è sotto ITO H24")
                        else:
                            break
                if "## ITO LITE" in line.strip():
                    if is_main == True:
                        CR+= ""
                    else:
                        is_main = True
                        CR = ""
                    clienteITO = True
                    line = f.readline()
                    while line := f.readline():
                        if line[0:2] == "* ":
                            splitted = line[2:].split(':', 1)
                            match = re.search(r'\[.*?\]\((.*?)\)', splitted[0])
                            if match:
                                # Replace the link with the desired link
                                new_link = os.path.join(subdir, "") + match.group(1)
                                splitted[0] = splitted[0].replace(match.group(1), new_link)
                            CR += splitted[0] + " ITO LITE: "+ splitted[1] + " <br/>"
                            print("Il progetto "+ line[2:] + " del cliente "+nome+" è sotto ITO LITE")
                        else:
                            break
                if "## Progetti senza ITO" in line.strip():
                    if is_main == True:
                        CR+= ""
                    else:
                        is_main = True
                        CR = ""
                    line = f.readline()
                    while line := f.readline():
                        if line[0:2] == "* ":
                            splitted = line[2:].split(':', 1)
                            match = re.search(r'\[.*?\]\((.*?)\)', splitted[0])
                            if match:
                                # Replace the link with the desired link
                                new_link = os.path.join(subdir, "") + match.group(1)
                                splitted[0] = splitted[0].replace(match.group(1), new_link)
                            CR += splitted[0] + " NON ITO: "+ splitted[1] + " <br/>"
                            print("Il progetto "+ line[2:] + " del cliente "+nome+" NON è sotto ITO")
                        else:
                            break
                if "## Note H24" in line.strip() and is_main == True:
                    line = f.readline()
                    if is_main == True:
                        cliente.append(CR)
                    cliente.append("[Presenti]("+os.path.join(subdir,file)+"#note-h24)")
                    if clienteITO == True:
                        clientiITO.append(cliente)
                    else:
                        clientiNonITO.append(cliente)
                    is_main = False
                    break
            if is_main == True:
                cliente.append(CR)
                if clienteITO == True:
                   clientiITO.append(cliente)
                else:
                    clientiNonITO.append(cliente)
            sezioni = 0
            cliente.clear
            CR = ""
            f.close()

writer = MarkdownTableWriter(
    table_name="ITO customers",
    headers=["Customer", "ERP", "Note"],
    value_matrix=sorted(clientiITO,key = itemgetter(0))
)

writer2 = MarkdownTableWriter(
    table_name="Non ITO customers",
    headers=["Customer", "ERP", "Note"],
    value_matrix=sorted(clientiNonITO,key = itemgetter(0))
)
with open("index.md", "w") as outfile:
    outfile.write("# Customers Overview\n\n")
    outfile.write("!!! warning\n\tDo **not edit** this page, it's auto-generated by [Github Actions](https://github.com/criticalcase/leaf-wiki/actions)\n")
    writer.stream = outfile
    writer.write_table()

    outfile.write("\n")
    writer2.stream = outfile
    writer2.write_table()

############################# FOR HTML FILE #####################################
html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Clients Table</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Fira+Sans:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');
  body {
    font-family: 'Fira Sans', sans-serif;
    margin: 0;
    padding: 0;
  }
  .table-container {
    width: 80%;
    margin: 0 auto; /* Center the container */
  }
  .table-title {
    color:#d8652b;
    margin-top: 20px;
    margin-bottom: 0;
  }
  table {
    border-collapse: collapse;
    width: 100%;
    margin: 20px auto; /* Center table on the page */
  }
  th, td {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
  }
  th {
    background-color: #f2f2f2;
  }
  tr:nth-child(even) {
    background-color: #f9f9f9;
  }
</style>
</head>
<body>

<div class="table-container">
  <h1 class="table-title">Criticalcase ITO Customers</h1>
"""
html += '<table border="1">\n'  # Start of the table, border=1 for visibility
html += '  <tr>\n    <th>Customer name</th>\n    <th>Projects</th>\n  </tr>\n'

# Loop through each client and create a row
for client in sorted(clientiITOHTML, key=lambda x: x['nome_cliente']):
    html += '  <tr>\n'
    html += '    <td>{}</td>\n'.format(client['nome_cliente'])
    # Create a string with each project separated by a <br> tag
    projects_str = '<br>'.join(client['progetti'])
    html += '    <td>{}</td>\n'.format(projects_str)
    html += '  </tr>\n'

html += '</table></div>'

# End of the HTML document
html += """
</body>
</html>
"""

# Print the HTML table
#print(html)

# To save the HTML table to a file
with open('customersito.html', 'w') as f:
    f.write(html)

#################################################################################
