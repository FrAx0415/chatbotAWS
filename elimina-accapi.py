# Funzione per rimuovere gli accapi vuoti da un file
def remove_empty_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip():
                file.write(line)

# Percorso al file index.html
file_path = 'index.html'

# Rimuovi gli accapi vuoti dal file
remove_empty_lines(file_path)

print(f"Empty lines removed from {file_path}.")
