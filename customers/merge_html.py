import os
import glob
import re
from collections import defaultdict
import shutil

# Directory root da cui iniziare
ROOT_DIR = "."  # Cambia questo con il percorso alla directory principale

# Output directory per i file uniti
OUTPUT_DIR = "./merged_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Funzione per ottenere tutti i file HTML ricorsivamente
def get_all_html_files(root_dir):
    return glob.glob(f"{root_dir}/**/*.html", recursive=True)

# Funzione per raggruppare i file per cliente
def group_files_by_customer(files):
    customer_files = defaultdict(list)
    
    for file in files:
        # Estrai il nome del cliente dalla path
        match = re.search(r'/([^/]+-C\d+)/', file)
        if match:
            customer = match.group(1)
            customer_files[customer].append(file)
        else:
            # File non associati a un cliente specifico vanno in "others"
            customer_files["others"].append(file)
    
    return customer_files

# Funzione per unire i file HTML
def merge_html_files(files, output_file):
    merged_content = "<!DOCTYPE html>\n<html>\n<head>\n"
    merged_content += "<meta charset='UTF-8'>\n"
    merged_content += "<title>Merged Documentation</title>\n"
    merged_content += "<style>\n.file-section { margin-top: 20px; border-top: 1px solid #ccc; padding-top: 10px; }\n"
    merged_content += ".file-path { color: #666; font-style: italic; }\n</style>\n"
    merged_content += "</head>\n<body>\n"
    
    for i, file in enumerate(files):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Estrai solo il contenuto del body se possibile
                body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
                if body_match:
                    content = body_match.group(1)
                
                # Aggiungi intestazione per identificare la fonte originale
                merged_content += f"<div class='file-section'>\n"
                merged_content += f"<div class='file-path'>Source: {file}</div>\n"
                merged_content += f"{content}\n"
                merged_content += f"</div>\n"
        except Exception as e:
            print(f"Errore nel processare {file}: {e}")
    
    merged_content += "</body>\n</html>"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(merged_content)

# Funzione per creare una struttura di directory che mantenga un po' di organizzazione
def create_merged_structure(customer_files, max_files=100):
    # Decidi quanti file per cliente in base al numero target
    total_customers = len(customer_files)
    if total_customers == 0:
        return
    
    # Calcola il numero massimo di file HTML da unire in un singolo file
    total_html_files = sum(len(files) for files in customer_files.values())
    merge_factor = max(1, round(total_html_files / max_files))
    
    print(f"Totale file HTML: {total_html_files}")
    print(f"Fattore di unione: circa {merge_factor} file verranno uniti in uno")
    
    counter = 0
    for customer, files in customer_files.items():
        # Crea una directory per il cliente
        customer_dir = os.path.join(OUTPUT_DIR, customer)
        os.makedirs(customer_dir, exist_ok=True)
        
        # Dividi i file in gruppi di 'merge_factor'
        for i in range(0, len(files), merge_factor):
            group = files[i:i+merge_factor]
            output_file = os.path.join(customer_dir, f"merged_{i//merge_factor}.html")
            merge_html_files(group, output_file)
            counter += 1
            
            print(f"Creato file unito {counter}: {output_file} ({len(group)} file uniti)")
        
        # Copia anche i file non-HTML (come immagini, etc.)
        for file in files:
            dir_name = os.path.dirname(file)
            for asset in glob.glob(f"{dir_name}/**/*.*", recursive=True):
                if not asset.endswith('.html'):
                    rel_path = os.path.relpath(asset, ROOT_DIR)
                    dest_path = os.path.join(OUTPUT_DIR, rel_path)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    try:
                        shutil.copy2(asset, dest_path)
                    except Exception as e:
                        print(f"Errore nel copiare {asset}: {e}")

# Main
if __name__ == "__main__":
    all_html_files = get_all_html_files(ROOT_DIR)
    customer_files = group_files_by_customer(all_html_files)
    create_merged_structure(customer_files, max_files=100)
    
    print("\nProcesso completato!")
    print(f"I file uniti sono stati salvati nella directory: {OUTPUT_DIR}")
