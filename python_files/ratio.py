import pandas as pd
import matplotlib.pyplot as plt
import re
import Levenshtein

###### CONSTANTES ######

# Domain = Industriel

industriel = {1:{'2016':1600, '2017': 2400, '2018': 1940, '2019': 2440, '2020': 2440, '2021': 2850, '2022': 3510, '2023': 3923}, 
              2:{'2016':1.675, '2017': 1.91875, '2018': 2.16625, '2019': 2.645, '2020': 2.93, '2021': 3.3695, '2022': 3.87, '2023': 4.26},
              3:{'2017': 20973, '2018': 23573, '2019': 25743, '2020': 25153},
              4:{'2016': 37057, '2017': 37629, '2018': 41214, '2019': 43784, '2020': 44804, '2021': 48538, '2022': 50662, '2023': 52666},
              5:{},
              6:{},
              7:{'2017': 15554, '2018': 16616},
              8:{'2016':1158, '2017': 1237, '2018': 1332, '2019': 1541, '2020': 1633, '2021': 1739, '2022': 2002}}

# Domain = Services Publics

services = {1:{'2017': 885, '2018': 598, '2019': 1323, '2020': 1593, '2021': 1188, '2022': 1285.5, '2023': 1707}, 
              2:{'2010': 1.12, '2011': 1.16, '2012': 1.2, '2017': 1.62, '2018': 1.72, '2020': 1.935},
              3:{'2017': 47822, '2018': 53051, '2020': 55481},
              4:{'2017': 31073, '2018': 34595, '2020': 35197},
              5:{},
              6:{},
              7:{'2021': 5170, '2022': 5560, '2023': 5944},
              8:{'2017': 449, '2018': 441}}

# Domain = Telecoms

telecoms = {1:{'2018': 310, '2019': 336, '2020': 276, '2021': 299, '2022': 298}, 
              2:{'2017': 2.87, '2018': 3.02, '2019': 3.17, '2020': 3.33, '2021': 3.5, '2022': 3.678},
              3:{},
              4:{},
              5:{},
              6:{},
              7:{},
              8:{}}

########################

def ratio_analysis(path, mode, domain=None):

    df = pd.read_csv(path)
    # On supprime les lignes en double
    df = df.drop_duplicates(subset='Unnamed: 0')
    # On conserve seulement les colonnes qui sont des années (exceptés la première)
    pattern = re.compile(r'^20\d{2}$')
    year_columns = [col for col in df.columns if pattern.match(col)]

    # Ajouter la première colonne à la liste des colonnes à conserver
    columns_to_keep = [df.columns[0]] + year_columns

    # Créer un nouveau DataFrame avec les colonnes sélectionnées
    df_filtered = df[columns_to_keep]
    # Supprimer les lignes dont toutes les colonnes sont à "NaN" exceptés la première
    df_filtered = df_filtered.dropna(how='all', subset=year_columns)

    if mode == 1:
        evolution_benefice_net(df, domain)
    elif mode == 2:
        evolution_div_action(df, domain)
    elif mode == 3:
        show_actifs_passifs_totaux(df, domain)
    elif mode == 4:
        show_actifs_passifs_current(df, domain)
    elif mode == 5:
        evolution_rnd(df, domain)
    else:
        evolution_div_versé(df, domain)

def evolution_benefice_net(df_filtered, domain=None):
    # Extraire les valeurs de "Bénéfice net" ou la version anglaise
    if domain is not None:
        if domain=="telecoms":

            domain_dict = telecoms
        elif domain=="services":
            domain_dict = services
        elif domain=="industriel":
            domain_dict = industriel
        mean_values = []
        if domain_dict is None:
            print("Aucun dictionnaire correspondant à 'la valeur de domain fourni n'a été trouvé.")
            return
            
    pattern = re.compile(r'Bénéfice net|Net Income|Net Earnings', re.IGNORECASE)
    benefice_net = df_filtered[df_filtered['Unnamed: 0'].str.contains(pattern, na=False)]

    # Sélectionner la ligne qui correspond le mieux au motif "Bénéfice net" ou "Net Income" ou "Net Earnings"
    best_match = None
    min_distance = float('inf')

    for index, row in benefice_net.iterrows():
        current_distance_fr = Levenshtein.distance(row['Unnamed: 0'].lower(), 'bénéfice net')
        current_distance_en = min(Levenshtein.distance(row['Unnamed: 0'].lower(), 'net earnings'), Levenshtein.distance(row['Unnamed: 0'].lower(), 'net income'))
        if current_distance_fr < min_distance or current_distance_en < min_distance:
            min_distance = min(current_distance_fr, current_distance_en)
            best_match = row

    if best_match is None:
        print("Aucune ligne correspondant à 'Bénéfice net' ou 'Net Income' n'a été trouvée. Notre algorithme n'a pas réussi à capturer les informations. Veuillez regarder dans le fichier.")
        return
    # Fonction pour nettoyer les chaînes de caractères
    def clean_string(s):
        s = s.replace('\xa0', '').replace(' ', '').replace('$', '').replace(',', '')
        return s.replace('(', '-').replace(')','')

    # Appliquer la fonction de nettoyage et convertir en float
    years = []
    values = []
    best_match_row = benefice_net.loc[best_match.name]
    best_match_df = pd.DataFrame(best_match_row).T
    for col in df_filtered.columns[1:]:
        if not pd.isna(best_match_df[col].values[0]):  # Vérifier si la colonne contient des NaN
            best_match_df[col] = best_match_df[col].apply(clean_string).astype(float)
            years.append(col)
            values.append(best_match_df[col].values[0])
            if domain is not None:
                if col not in domain_dict[1].keys():
                    print("Nous ne possédons pas de données pour les entreprise du même domaine, veuillez ne pas fournir d'argument domain.")
                    return
                mean_values.append(domain_dict[1][col])

    # Extraire les années et les valeurs dans un ordre croissant
    if domain is None:
      years, values = zip(*sorted(zip(years, values)))
    else:
        years, values, mean_values = zip(*sorted(zip(years, values, mean_values)))
        plt.plot(years, mean_values, marker='x', color='green', linestyle='--', label='valeur moyenne des entreprises du même domaine')
    plt.plot(years, values, marker='o', label='Entreprise traitée')
    plt.title('Bénéfice net en fonction de l\'année')
    plt.xlabel('Année')
    plt.ylabel('Bénéfice net (en milllions de $)')
    plt.legend()
    plt.grid(True)
    plt.show()

def evolution_div_action(df_filtered, domain=None):
    # Extraire les valeurs de "Dividendes déclarés par action"
    if domain is not None:
        if domain=="telecoms":

            domain_dict = telecoms
        elif domain=="services":
            domain_dict = services
        elif domain=="industriel":
            domain_dict = industriel
        mean_values = []
        if domain_dict is None:
            print(f"Aucun dictionnaire correspondant à 'la valeur de domain fourni n'a été trouvé.")
            return
    pattern = re.compile(r'Dividendes déclarés par action|Dividends paid per common Share|Dividends declared per share', re.IGNORECASE)
    div_action = df_filtered[df_filtered['Unnamed: 0'].str.contains(pattern, na=False)]
    # print(div_action)

    # Fonction pour nettoyer les chaînes de caractères
    # Sélectionner la ligne qui correspond le mieux au motif "Dividendes déclarés par action", "Dividends paid per common Share" ou "Dividends declared per share"
    best_match = None
    min_distance = float('inf')

    for index, row in div_action.iterrows():
        current_distance_fr = Levenshtein.distance(row['Unnamed: 0'].lower(), 'dividendes déclarés par action')
        current_distance_en = min(Levenshtein.distance(row['Unnamed: 0'].lower(), 'dividends per common share'), Levenshtein.distance(row['Unnamed: 0'].lower(), 'dividends declared per share'))
        if current_distance_fr < min_distance or current_distance_en < min_distance:
            min_distance = min(current_distance_fr, current_distance_en)
            best_match = row

    if best_match is None:
        print("Aucune ligne correspondant à 'dividendes déclarés par action' ou 'dividends paid per common share' n'a été trouvée. Notre algorithme n'a pas réussi à capturer les informations. Veuillez regarder dans le fichier.")
        return
    # Fonction pour nettoyer les chaînes de caractères
    def clean_string(s):
        s = s.replace('\xa0', '').replace(' ', '').replace('$', '')
        s = s.replace(',', '.')  # Remplacer les virgules par des points
        return s

    # Appliquer la fonction de nettoyage et convertir en float
    years = []
    values = []
    best_match_row = div_action.loc[best_match.name]
    best_match_df = pd.DataFrame(best_match_row).T
    for col in df_filtered.columns[1:]:
        if not best_match_df[col].isna().any():  # Vérifier si la colonne contient des NaN
            best_match_df[col] = best_match_df[col].apply(clean_string).astype(float)
            years.append(col)
            values.append(best_match_df[col].values[0])
            if domain is not None:
                if col not in domain_dict[2].keys():
                    print("Nous ne possédons pas de données pour les entreprise du même domaine, veuillez ne pas fournir d'argument domain.")
                    return
                mean_values.append(domain_dict[2][col])

    # Extraire les années et les valeurs dans un ordre croissant
    if domain is None:
      years, values = zip(*sorted(zip(years, values)))
    else:
        years, values, mean_values = zip(*sorted(zip(years, values, mean_values)))
        plt.plot(years, mean_values, marker='x', color='green', linestyle='--', label='valeur moyenne des entreprises du même domaine')

    # Tracer les données
    plt.plot(years, values, marker='o', label = "entreprise traitée")
    plt.title('Dividendes par actions en fonction de l\'année')
    plt.xlabel('Année')
    plt.ylabel('Dividendes par actions ($)')
    plt.legend()
    plt.grid(True)
    plt.show()


def show_actifs_passifs_totaux(df_filtered, domain=None):
    if domain is not None:
        if domain=="telecoms":

            domain_dict = telecoms
        elif domain=="services":
            domain_dict = services
        elif domain=="industriel":
            domain_dict = industriel
        mean_actifs_values = []
        mean_passifs_values = []
        ratios_values = []
        if domain_dict is None:
            print(f"Aucun dictionnaire correspondant à 'la valeur de domain fourni n'a été trouvé.")
            return

    pattern_actifs = re.compile(r'Actif Total|Total Actif|Total assets', re.IGNORECASE)
    div_actifs = df_filtered[df_filtered['Unnamed: 0'].str.contains(pattern_actifs, na=False)]
    best_match_actifs = None
    min_distance_actifs = float('inf')

    for index, row in div_actifs.iterrows():
        current_distance_fr = min(Levenshtein.distance(row['Unnamed: 0'].lower(), 'total actifs'), Levenshtein.distance(row['Unnamed: 0'].lower(), 'actifs total'))
        current_distance_en = Levenshtein.distance(row['Unnamed: 0'].lower(), 'total assets')
        if current_distance_fr < min_distance_actifs or current_distance_en < min_distance_actifs:
            min_distance_actifs = min(current_distance_fr, current_distance_en)
            best_match_actifs = row

    if best_match_actifs is None:
        print("Aucune ligne correspondant à 'total actifs' ou 'total assets' n'a été trouvée. Notre algorithme n'a pas réussi à capturer les informations. Veuillez regarder dans le fichier.")
        return
    pattern_passifs = re.compile(r'Passif Total|Passifs total|Total liabilities', re.IGNORECASE)
    div_passifs = df_filtered[df_filtered['Unnamed: 0'].str.contains(pattern_passifs, na=False)]
    best_match_passifs = None
    min_distance_passifs = float('inf')

    for index, row in div_passifs.iterrows():
        current_distance_fr = min(Levenshtein.distance(row['Unnamed: 0'].lower(), 'total passifs'), Levenshtein.distance(row['Unnamed: 0'].lower(), 'passifs total'))
        current_distance_en = Levenshtein.distance(row['Unnamed: 0'].lower(), 'total liabilities')
        if current_distance_fr < min_distance_passifs or current_distance_en < min_distance_passifs:
            min_distance_passifs = min(current_distance_fr, current_distance_en)
            best_match_passifs = row

    if best_match_passifs is None:
        print("Aucune ligne correspondant à 'total passifs' ou 'total liabilities' n'a été trouvée. Notre algorithme n'a pas réussi à capturer les informations. Veuillez regarder dans le fichier.")
        return

    def clean_string(s):
        s = s.replace('\xa0', '').replace(' ', '').replace('$', '')
        s = s.replace(',', '')  # Remplacer les virgules par des points
        return s
    
    best_actifs_row = div_actifs.loc[best_match_actifs.name]
    best_actifs_df = pd.DataFrame(best_actifs_row).T

    best_passifs_row = div_passifs.loc[best_match_passifs.name]
    best_passifs_df = pd.DataFrame(best_passifs_row).T

    years = []
    values_actifs = []
    values_passifs = []
    values = []
    for col in df_filtered.columns[1:]:
        if not best_actifs_df[col].isna().any() and not best_passifs_df[col].isna().any():
            best_actifs_df[col] = best_actifs_df[col].apply(clean_string).astype(float)
            best_passifs_df[col] = best_passifs_df[col].apply(clean_string).astype(float)
            years.append(col)
            values_actifs.append(best_actifs_df[col].values[0])
            values_passifs.append(best_passifs_df[col].values[0])
            values.append(best_passifs_df[col].values[0]/best_actifs_df[col].values[0])
            if domain is not None:
                if col in domain_dict[3].keys:
                    mean_actifs_values.append(domain_dict[3][col])
                else:
                    print("Notre algorithme n'est pas en mesure de calculer la valeur moyenne dans l'industrie. Veuillez retirer l'argument domain.")
                    return
                if col in domain_dict[4].keys:
                    mean_actifs_values.append(domain_dict[4][col])
                else:
                    print("Notre algorithme n'est pas en mesure de calculer la valeur moyenne dans l'industrie. Veuillez retirer l'argument domain.")
                    return
                ratios_values.append(domain_dict[4][col]/ domain_dict[3][col])

    fig, ax1 = plt.subplots(figsize=(10,5))
    if domain is None:
       years, values, values_actifs, values_passifs = zip(*sorted(zip(years, values, values_actifs, values_passifs)))
    else:
       years, values, values_actifs, values_passifs, mean_actifs_values, mean_passifs_values, ratios_values = zip(*sorted(zip(years, values, values_actifs, values_passifs, mean_actifs_values, mean_passifs_values, ratios_values)))
       ax1.plot(years, mean_actifs_values, color='orange', linestyle='--', label='Actifs totaux des entreprises du même domaine')
       ax1.plot(years, mean_actifs_values, color='red', linestyle='--', label='Passifs totaux des entreprises du même domaine')

    ax1.plot(years, values_actifs, marker='x', color='cyan', label='actifs totaux')
    ax1.plot(years, values_passifs, marker='x', color='blue', label='passifs totaux')
    ax1.set_xlabel('Année')
    ax1.set_ylabel('Millions de $', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.grid(True)
    ax2 = ax1.twinx()
    ax2.plot(years, values, marker='x', color='green', label='Ratio d\'endettemment')
    if domain is not None:
        ax2.plot(years, mean_actifs_values, color='yellow', linestyle='--', label='Ratio d\'endettemment des entreprises du même domaine')
    ax2.set_ylabel("Ratio d'endettemment")
    ax2.tick_params(axis='y', labelcolor='g')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.title('Actifs et passifs totaux ainsi que le ratio d\'endettement en fonction de l\'année')
    plt.show()

def show_actifs_passifs_current(df_filtered, domain=None):
    if domain is not None:
        if domain=="telecoms":

            domain_dict = telecoms
        elif domain=="services":
            domain_dict = services
        elif domain=="industriel":
            domain_dict = industriel
        mean_actifs_values = []
        mean_passifs_values = []
        ratios_values = []
        if domain_dict is None:
            print(f"Aucun dictionnaire correspondant à 'la valeur de domain fourni n'a été trouvé.")
            return
    pattern_actifs = re.compile(r'Actif court terme|Current assets', re.IGNORECASE)
    div_actifs = df_filtered[df_filtered['Unnamed: 0'].str.contains(pattern_actifs, na=False)]

    best_match_actifs = None
    min_distance_actifs = float('inf')

    for index, row in div_actifs.iterrows():
        current_distance_fr = Levenshtein.distance(row['Unnamed: 0'].lower(), 'actifs court terme')
        current_distance_en = Levenshtein.distance(row['Unnamed: 0'].lower(), 'current assets')
        if current_distance_fr < min_distance_actifs or current_distance_en < min_distance_actifs:
            min_distance_actifs = min(current_distance_fr, current_distance_en)
            best_match_actifs = row

    if best_match_actifs is None:
        print("Aucune ligne correspondant à 'actifs à court terme' ou 'current assets' n'a été trouvée. Notre algorithme n'a pas réussi à capturer les informations. Veuillez regarder dans le fichier.")
        return
    pattern_passifs = re.compile(r'Passifs court terme|current liabilities', re.IGNORECASE)
    div_passifs = df_filtered[df_filtered['Unnamed: 0'].str.contains(pattern_passifs, na=False)]

    best_match_passifs = None
    min_distance_passifs = float('inf')

    for index, row in div_passifs.iterrows():
        current_distance_fr = Levenshtein.distance(row['Unnamed: 0'].lower(), 'passifs à court terme')
        current_distance_en = Levenshtein.distance(row['Unnamed: 0'].lower(), 'current liabilities')
        if current_distance_fr < min_distance_passifs or current_distance_en < min_distance_passifs:
            min_distance_passifs = min(current_distance_fr, current_distance_en)
            best_match_passifs = row

    if best_match_passifs is None:
        print("Aucune ligne correspondant à 'passifs à court terme' ou 'current liabilities' n'a été trouvée. Notre algorithme n'a pas réussi à capturer les informations. Veuillez regarder dans le fichier.")
        return
    def clean_string(s):
        s = s.replace('\xa0', '').replace(' ', '').replace('$', '').replace('(', '').replace(')','')
        s = s.replace(',', '')
        return s
    
    best_actifs_row = div_actifs.loc[best_match_actifs.name]
    best_actifs_df = pd.DataFrame(best_actifs_row).T

    best_passifs_row = div_passifs.loc[best_match_passifs.name]
    best_passifs_df = pd.DataFrame(best_passifs_row).T

    years = []
    values_actifs = []
    values_passifs = []
    values = []
    for col in df_filtered.columns[1:]:
        if not best_actifs_df[col].isna().any() and not best_passifs_df[col].isna().any():
            best_actifs_df[col] = best_actifs_df[col].apply(clean_string).astype(float)
            best_passifs_df[col] = best_passifs_df[col].apply(clean_string).astype(float)
            years.append(col)
            values_actifs.append(best_actifs_df[col].values[0])
            values_passifs.append(best_passifs_df[col].values[0])
            values.append(best_actifs_df[col].values[0]/best_passifs_df[col].values[0])
            if domain is not None:
                if col in domain_dict[5].keys:
                    mean_actifs_values.append(domain_dict[3][col])
                else:
                    print("Notre algorithme n'est pas en mesure de calculer la valeur moyenne dans l'industrie. Veuillez retirer l'argument domain.")
                    return
                if col in domain_dict[6].keys:
                    mean_actifs_values.append(domain_dict[4][col])
                else:
                    print("Notre algorithme n'est pas en mesure de calculer la valeur moyenne dans l'industrie. Veuillez retirer l'argument domain.")
                    return
                ratios_values.append(domain_dict[5][col]/ domain_dict[6][col])

    fig, ax1 = plt.subplots(figsize=(10,5))
    if domain is None:
       years, values, values_actifs, values_passifs = zip(*sorted(zip(years, values, values_actifs, values_passifs)))
    else:
       years, values, values_actifs, values_passifs, mean_actifs_values, mean_passifs_values, ratios_values = zip(*sorted(zip(years, values, values_actifs, values_passifs, mean_actifs_values, mean_passifs_values, ratios_values)))
       ax1.plot(years, mean_actifs_values, color='orange', linestyle='--', label='Actifs courants des entreprises du même domaine')
       ax1.plot(years, mean_actifs_values, color='red', linestyle='--', label='Passifs courants des entreprises du même domaine')

    ax1.plot(years, values_actifs, marker='x', color='cyan', label='actifs courants')
    ax1.plot(years, values_passifs, marker='x', color='blue', label='passifs courants')
    ax1.set_xlabel('Année')
    ax1.set_ylabel('Millions de $', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.grid(True)
    ax2 = ax1.twinx()
    ax2.plot(years, values, marker='x', color='green', label='Liquidité courante')
    if domain is not None:
        ax2.plot(years, mean_actifs_values, color='yellow', linestyle='--', label='Ratio de liquidité courante des entreprises du même domaine')
    ax2.set_ylabel("Ratio de liquidité courante")
    ax2.tick_params(axis='y', labelcolor='g')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.title('Actifs et passifs courant ainsi que le ratio de liquidité courante de l\'année')
    plt.show()

def evolution_rnd(df_filtered, domain=None):
    if domain is not None:
        if domain=="telecoms":

            domain_dict = telecoms
        elif domain=="services":
            domain_dict = services
        elif domain=="industriel":
            domain_dict = industriel
        mean_values = []
        if domain_dict is None:
            print(f"Aucun dictionnaire correspondant à 'la valeur de domain fourni n'a été trouvé.")
            return

    pattern = re.compile(r'Bénéfices non répartis|Retained Earnings', re.IGNORECASE)
    div_rnd = df_filtered[df_filtered['Unnamed: 0'].str.contains(pattern, na=False)]

    best_match = None
    min_distance = float('inf')

    for index, row in div_rnd.iterrows():
        current_distance_fr = Levenshtein.distance(row['Unnamed: 0'].lower(), 'Bénéfices non répartis')
        current_distance_en = Levenshtein.distance(row['Unnamed: 0'].lower(), 'Retained Earnings')
        if current_distance_fr < min_distance or current_distance_en < min_distance:
            min_distance = min(current_distance_fr, current_distance_en)
            best_match = row

    if best_match is None:
        print("Aucune ligne correspondant à 'béfénices non réparties' ou 'retained earnings' n'a été trouvée. Notre algorithme n'a pas réussi à capturer les informations. Veuillez regarder dans le fichier.")
        return
    def clean_string(s):
        s = s.replace('\xa0', '').replace('$', '')
        s = s.replace(',', ' ').replace(' ', '')
        return s

    years = []
    values = []
    best_match_row = div_rnd.loc[best_match.name]
    best_match_df = pd.DataFrame(best_match_row).T
    for col in df_filtered.columns[1:]:
        if not best_match_df[col].isna().any():
            best_match_df[col] = best_match_df[col].apply(clean_string).astype(float)
            years.append(col)
            values.append(best_match_df[col].values[0])
            if domain is not None:
                if col not in domain_dict[7].keys():
                    
                    print("Nous ne possédons pas de données pour les entreprise du même domaine, veuillez ne pas fournir d'argument domain.")
                    return
                mean_values.append(domain_dict[7][col])

    if domain is None:
      years, values = zip(*sorted(zip(years, values)))
    else:
        years, values, mean_values = zip(*sorted(zip(years, values, mean_values)))
        plt.plot(years, mean_values, marker='x', color='green', linestyle='--', label='valeur moyenne des entreprises du même domaine')

    plt.plot(years, values, marker='x', label = "entreprise traitée")
    plt.title('Béfénices non réparties en fonction de l\'année')
    plt.xlabel('Année')
    plt.ylabel('Béfénices non réparties (en million de $)')
    plt.grid(True)
    plt.legend()
    plt.show()

def evolution_div_versé(df_filtered, domain=None):

    if domain is not None:
        if domain=="telecoms":

            domain_dict = telecoms
        elif domain=="services":
            domain_dict = services
        elif domain=="industriel":
            domain_dict = industriel
        mean_values = []
        if domain_dict is None:
            print(f"Aucun dictionnaire correspondant à 'la valeur de domain fourni n'a été trouvé.")
            return

    pattern = re.compile(r'Dividendes versés|Dividends', re.IGNORECASE)
    div_verse = df_filtered[df_filtered['Unnamed: 0'].str.contains(pattern, na=False)]

    best_match = None
    min_distance = float('inf')

    for index, row in div_verse.iterrows():
        current_distance_fr = Levenshtein.distance(row['Unnamed: 0'].lower(), 'Dividendes versés')
        current_distance_en = Levenshtein.distance(row['Unnamed: 0'].lower(), 'Dividends')
        if current_distance_fr < min_distance or current_distance_en < min_distance:
            min_distance = min(current_distance_fr, current_distance_en)
            best_match = row

    if best_match is None:
        print("Aucune ligne correspondant à 'dividendes versés' ou 'dividends' n'a été trouvée. Notre algorithme n'a pas réussi à capturer les informations. Veuillez regarder dans le fichier.")
        return
    def clean_string(s):
        s = s.replace('\xa0', '').replace('(', '').replace(')', '').replace(' ', '').replace('\$', '')
        s = s.replace(',', '').replace('$\n', '').replace('\n$', '')
        return s

    years = []
    values = []
    best_match_row = div_verse.loc[best_match.name]
    best_match_df = pd.DataFrame(best_match_row).T
    for col in df_filtered.columns[1:]:
        if not best_match_df[col].isna().any(): 
            best_match_df[col] = best_match_df[col].apply(clean_string).astype(float)
            years.append(col)
            values.append(best_match_df[col].values[0])
            if domain is not None:
                if col not in domain_dict[8].keys():
                    print("Nous ne possédons pas de données pour les entreprise du même domaine, veuillez ne pas fournir d'argument domain.")
                    return
                    
                mean_values.append(domain_dict[8][col])

    if domain is None:
      years, values = zip(*sorted(zip(years, values)))
    else:
        years, values, mean_values = zip(*sorted(zip(years, values, mean_values)))
        plt.plot(years, mean_values, marker='x', color='green', linestyle='--', label='valeur moyenne des entreprises du même domaine')

    plt.plot(years, values, marker='o',label="entreprise traitée")
    plt.title('Dividendes versées en fonction de l\'année')
    plt.xlabel('Année')
    plt.ylabel('Dividendes versés (en million de $)')
    plt.grid(True)
    plt.legend()
    plt.show()