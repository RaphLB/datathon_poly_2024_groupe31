
import re
import pdfplumber
import camelot
import base64
import os

def extract_text_from_pdf(pdf_path, limit = None):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''

        if limit == None :
            for page in pdf.pages:   
                text += page.extract_text()      
        else :
            for page in pdf.pages[:limit]:   
                text += page.extract_text()   
    return text


def contains_table(text, window_size=50, threshold=0.25):
    """
    Vérifie si une page contient un tableau en analysant la densité de nombres dans des segments de texte.
    
    - window_size: taille de la fenêtre glissante (nombre de mots par segment)
    - threshold: densité minimale de nombres pour considérer qu'une fenêtre contient un tableau
    """
    words = text.split()
    total_words = len(words)
    
    if total_words == 0:
        return False

    # Fenêtre glissante pour analyser la densité de nombres
    for i in range(0, total_words - min(window_size,total_words) + 1):
        window = words[i:i + window_size]
        window = [word.replace("$", " ") for word in window]
        
        # Compte le nombre de mots qui sont des nombres
        numbers_in_window = sum(1 for word in window if re.match(r'^\d+(\.\d+)?$', word))
        #window_size = sum(len(word) if re.match(r'^\d+(\.\d+)?$', word) else 1 for word in window)
        
        # Calcul de la densité de nombres dans la fenêtre
        density = numbers_in_window / window_size

        # Si la densité dépasse le seuil, on identifie la page comme ayant un tableau
        if density > threshold:
            return True
    return False

def extract_text_from_pdf_and_test_table(pdf_path):
    pages_with_table_list = []
    with pdfplumber.open(pdf_path) as pdf:
        text = ''

        for page_number, page in enumerate(pdf.pages):
            page_text = page.extract_text() or ''
            text += page_text
            
            # Vérifie si la page contient un tableau
            if contains_table(page_text):
                #print(f"Page {page_number + 1} identifiée comme ayant un tableau.")
                pages_with_table_list.append(page_number+1)
                #print(page_text)  # Affiche le texte de la page

    return pages_with_table_list


def convert_pdf_table_to_csv(file_name,list_of_pages,name_folder):
        # Define the folder path where you want to save the CSV files
    output_folder = name_folder

    # Create the folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    comma_separated_string_of_pages = ', '.join(str(i) for i in list_of_pages)
    list_dict_csv = []
    tables = camelot.read_pdf(file_name, pages=comma_separated_string_of_pages, flavor='stream', row_tol=10, column_tol=10)


    filtered_tables = [table for table in tables ]   #if table.shape[0] >= 2 and table.shape[1] >= 3

    for i, table in enumerate(filtered_tables):
        table.to_csv(os.path.join(output_folder, f"filtered_table_{i}.csv"), index=False)
        # Open the CSV file and read its contents
        number = str(i)
        with open(os.path.join(output_folder, f"filtered_table_{i}.csv"), "r",encoding='utf-8') as csv_file:
            csv_content = csv_file.read()

        # Encode the CSV content to base64
        csv_base64 = base64.b64encode(csv_content.encode()).decode()
        list_dict_csv.append({"name":"filtered_table_{i}.csv","content":csv_base64})
        
    return list_dict_csv

def generate_csv_tables(pdf_file_path,folder_name):
    list_of_pages = extract_text_from_pdf_and_test_table(pdf_file_path)
    list_of_dict_tables_csv = convert_pdf_table_to_csv(pdf_file_path,list_of_pages,folder_name)
    return list_of_dict_tables_csv

