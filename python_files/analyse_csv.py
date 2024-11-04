import pandas as pd
import unidecode
import re
import os


def load_csv_with_year_as_header(file_path):
    # Lire le fichier CSV sans spécifier les noms de colonnes
    df = pd.read_csv(file_path, header=None)

    # Identifier la première ligne contenant une année (par exemple 2016, 2017, etc.)
    year_pattern = r'^(20\d{2})$'   # Regex pour les années de 2000 à 2099
    mask = df.apply(lambda row: (row.astype(str).str.match(year_pattern)).sum() >= 2, axis=1)
    if not mask.any():
        return pd.DataFrame()
    
    header_row_index = mask.idxmax()
    # Définir la ligne trouvée comme les nouveaux noms de colonnes
    new_header = df.iloc[header_row_index].tolist()
    
    # Vérifier si `new_header` contient des éléments non uniques
    if len(new_header) != len(set(new_header)):
        
        return pd.DataFrame()  # Retourner un DataFrame vide si des éléments sont dupliqués


    df.columns = new_header

    # Supprimer toutes les lignes avant la ligne d'en-tête
    df = df[header_row_index + 1:]

    # Réinitialiser les index
    df.reset_index(drop=True, inplace=True)

    # Renommer la première colonne
    
    df.rename(columns={df.columns[0]: ''}, inplace=True)
    
    # Garder seulement les colonnes dont le nom est une année, et la première colonne
    year_columns = df.columns[df.columns.str.contains(year_pattern) | (df.columns == '')]

    df = df[year_columns]

    
    return df

def normalize_keywords(keywords):
    normalized = []
    for keyword in keywords:
        # Enlever les accents et ajouter flexibilité pour le "s" final
        normalized_keyword = unidecode.unidecode(keyword.lower())
        # Créer une regex qui accepte le "s" final optionnel
        pattern = re.sub(r'\b(\w+)', r'\1s?', normalized_keyword)
        normalized.append(pattern)
    return normalized

def consolidate_financial_reports(file_paths, keywords,output_folder):
    """
    Consolidate multiple CSVs with financial data into a single summary CSV.
    
    - file_paths: list of CSV file paths
    - keywords: list of keywords to filter rows of interest
    """
    # Crée un DataFrame vide pour stocker toutes les données consolidées
    list_dict_csv = []

    consolidated_data = pd.DataFrame()

    for file_path in file_paths:
        # Charge chaque fichier CSV
        df = load_csv_with_year_as_header(file_path)
        
        # Cherche les lignes pertinentes
        pattern = '|'.join(normalize_keywords(keywords))
        mask = df.apply(lambda row: row.astype(str).str.contains(pattern, case=False, regex=True).any(), axis=1)
        relevant_rows = df[mask]
        
        # Normalise les colonnes pour unifier les noms
        relevant_rows.columns = [col.lower().strip() for col in relevant_rows.columns if not pd.isna(col)]
        

        # Combine avec le DataFrame consolidé, en ajoutant de nouvelles lignes ou colonnes si nécessaire
        consolidated_data = pd.concat([consolidated_data, relevant_rows], ignore_index=True)

    # Sauvegarde le fichier consolidé final
    consolidated_data.to_csv(os.path.join(output_folder, f"consolidated_report.csv"), index=False)
    return
    


